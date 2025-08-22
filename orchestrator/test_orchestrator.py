import unittest
from unittest.mock import patch, MagicMock, call
import sys
import os

# Add project root to path to allow importing from orchestrator package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from orchestrator import orchestrator

class TestOrchestrator(unittest.TestCase):

    def setUp(self):
        """Set up a test config and mock loading it."""
        self.test_config = {
            'hosts': [
                {'name': 'host1', 'config': {'host': 'localhost1', 'user': 'user1'}},
                {'name': 'host2', 'config': {'host': 'localhost2', 'user': 'user2'}},
            ],
            'command_sequences': {
                'seq_test': [
                    {
                        'name': 'Sequential Step',
                        'hosts': ['host1', 'host2'],
                        'parallel': False,
                        'commands': ['cmd1', 'cmd2']
                    }
                ],
                'para_test': [
                    {
                        'name': 'Parallel Step',
                        'hosts': ['host1', 'host2'],
                        'parallel': True,
                        'commands': ['cmd3']
                    }
                ]
            }
        }
        # Patch yaml.safe_load in the orchestrator.orchestrator module
        self.mock_load_config = patch('orchestrator.orchestrator.load_config', return_value=self.test_config)
        self.mock_load_config.start()
        self.addCleanup(self.mock_load_config.stop)

    @patch('orchestrator.orchestrator.Connection')
    def test_sequential_execution(self, mock_connection_class):
        """Test that sequential commands are run in the correct order."""
        mock_conn_instance = MagicMock()
        mock_connection_class.return_value.__enter__.return_value = mock_conn_instance

        orchestrator.run_sequence(self.test_config, 'seq_test')

        # Check that Connection was called for each command execution
        call_list = mock_connection_class.call_args_list
        self.assertEqual(len(call_list), 4)
        self.assertEqual(call_list[0], call(**self.test_config['hosts'][0]['config']))
        self.assertEqual(call_list[1], call(**self.test_config['hosts'][0]['config']))
        self.assertEqual(call_list[2], call(**self.test_config['hosts'][1]['config']))
        self.assertEqual(call_list[3], call(**self.test_config['hosts'][1]['config']))

        # Check that run was called with the correct commands in order
        run_calls = mock_conn_instance.run.call_args_list
        self.assertEqual(len(run_calls), 4)
        self.assertEqual(run_calls[0], call('cmd1', hide=True))
        self.assertEqual(run_calls[1], call('cmd2', hide=True))
        self.assertEqual(run_calls[2], call('cmd1', hide=True))
        self.assertEqual(run_calls[3], call('cmd2', hide=True))

    @patch('orchestrator.orchestrator.Pool')
    @patch('orchestrator.orchestrator.run_command')
    def test_parallel_execution(self, mock_run_command, mock_pool_class):
        """Test that parallel commands use a process pool."""
        mock_pool_instance = MagicMock()
        mock_pool_class.return_value.__enter__.return_value = mock_pool_instance

        orchestrator.run_sequence(self.test_config, 'para_test')

        # Check that Pool was called with the number of commands to run
        mock_pool_class.assert_called_once_with(processes=2)

        # Check that starmap was called with the correct arguments
        host1_def = self.test_config['hosts'][0]
        host2_def = self.test_config['hosts'][1]
        expected_starmap_args = [
            (host1_def, 'cmd3'),
            (host2_def, 'cmd3'),
        ]
        mock_pool_instance.starmap.assert_called_once_with(orchestrator.run_command, expected_starmap_args)

    def test_get_host_def(self):
        """Test the get_host_def helper function."""
        host1 = orchestrator.get_host_def(self.test_config, 'host1')
        self.assertEqual(host1['name'], 'host1')
        with self.assertRaises(ValueError):
            orchestrator.get_host_def(self.test_config, 'non_existent_host')

if __name__ == '__main__':
    unittest.main()
