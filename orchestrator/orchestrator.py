import yaml
import argparse
from fabric import Connection
from invoke.exceptions import UnexpectedExit
from multiprocessing import Pool

def load_config(config_path='orchestrator/config.yml'):
    """Loads the YAML configuration file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def get_host_def(config, name):
    """Gets a host definition from the config by name."""
    for host in config['hosts']:
        if host['name'] == name:
            return host
    raise ValueError(f"Host '{name}' not found in config")

def run_command(host_def, command):
    """Runs a single command on a single host."""
    host_config = host_def['config']
    try:
        with Connection(**host_config) as c:
            print(f"[{c.host}] Running command: {command}")
            result = c.run(command, hide=True)
            print(f"[{c.host}] STDOUT: {result.stdout.strip()}")
            if result.stderr:
                print(f"[{c.host}] STDERR: {result.stderr.strip()}")
            return result
    except Exception as e:
        print(f"[{host_config.get('host', 'unknown')}] Error running command: {e}")
        return None

def execute_step(config, step):
    """Executes a single step from a command sequence."""
    print(f"\n--- Running Step: {step['name']} ---")

    hosts_to_run = [get_host_def(config, name) for name in step['hosts']]
    commands = step['commands']

    if step['parallel']:
        # Parallel execution
        pool_args = []
        for host_def in hosts_to_run:
            for command in commands:
                pool_args.append((host_def, command))

        with Pool(processes=len(pool_args)) as pool:
            pool.starmap(run_command, pool_args)
    else:
        # Sequential execution
        for host_def in hosts_to_run:
            for command in commands:
                run_command(host_def, command)

def run_sequence(config, sequence_name):
    """Runs a complete command sequence."""
    if sequence_name not in config['command_sequences']:
        print(f"Error: Command sequence '{sequence_name}' not found in config.")
        print("Available sequences:", ", ".join(config['command_sequences'].keys()))
        return

    sequence = config['command_sequences'][sequence_name]

    print(f"Executing sequence: {sequence_name}")
    for step in sequence:
        execute_step(config, step)
    print("\nSequence finished.")


def main():
    """Main function to run the orchestrator."""
    parser = argparse.ArgumentParser(description="Orchestrator for remote command execution.")
    parser.add_argument('sequence', help="The command sequence to execute (e.g., 'start_oracle').")
    parser.add_argument('--config', default='orchestrator/config.yml', help="Path to the configuration file.")

    args = parser.parse_args()

    try:
        config = load_config(args.config)
    except FileNotFoundError:
        print(f"Error: Configuration file not found at '{args.config}'")
        return

    run_sequence(config, args.sequence)


if __name__ == "__main__":
    main()
