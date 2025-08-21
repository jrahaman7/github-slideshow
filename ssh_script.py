# -*- coding: utf-8 -*-
"""
Created on Thu Aug 21 13:04:14 2025

@author: Jules

This script connects to multiple Linux servers using SSH and executes a series of commands.
The first five commands are executed sequentially, and the last two are executed in parallel.

Prerequisites:
- Python 3.x
- The `paramiko` library. You can install it using pip:
  pip install paramiko

Usage:
1. Update the `SERVERS` list with your server details (hostname, port, username, and password).
2. Update the `COMMANDS` list with the commands you want to execute.
3. Run the script from your terminal:
   python ssh_script.py
"""
import paramiko
import threading

# Placeholder for server details
# The user should replace these with their actual server information
SERVERS = [
    {
        'hostname': 'server1.example.com',
        'port': 22,
        'username': 'user',
        'password': 'password1'
    },
    {
        'hostname': 'server2.example.com',
        'port': 22,
        'username': 'user',
        'password': 'password2'
    },
    # Add more servers as needed
]

# Placeholder for commands
# The first five commands will be run sequentially, the last two in parallel
COMMANDS = [
    'echo "First command"',
    'ls -l',
    'uname -a',
    'df -h',
    'uptime',
    'echo "Sixth command (parallel)"',
    'echo "Seventh command (parallel)"',
]

def connect_to_server(server):
    """Establishes an SSH connection to a server and returns the client object."""
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(
            hostname=server['hostname'],
            port=server['port'],
            username=server['username'],
            password=server['password']
        )
        print(f"Successfully connected to {server['hostname']}")
        return ssh_client
    except Exception as e:
        print(f"Failed to connect to {server['hostname']}: {e}")
        return None

def execute_commands_sequentially(ssh_client, commands):
    """Executes a list of commands sequentially on a server."""
    for command in commands:
        try:
            print(f"Executing command: {command}")
            stdin, stdout, stderr = ssh_client.exec_command(command)
            print(stdout.read().decode())
            print(stderr.read().decode())
        except Exception as e:
            print(f"Failed to execute command '{command}': {e}")

def execute_command_in_thread(ssh_client, command):
    """Executes a single command in a thread."""
    try:
        print(f"Executing command in parallel: {command}")
        stdin, stdout, stderr = ssh_client.exec_command(command)
        print(stdout.read().decode())
        print(stderr.read().decode())
    except Exception as e:
        print(f"Failed to execute command '{command}' in parallel: {e}")

def execute_commands_in_parallel(ssh_client, commands):
    """Executes a list of commands in parallel on a server."""
    threads = []
    for command in commands:
        thread = threading.Thread(target=execute_command_in_thread, args=(ssh_client, command))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def main():
    """The main function of the script."""
    for server in SERVERS:
        ssh_client = connect_to_server(server)
        if ssh_client:
            # Execute the first five commands sequentially
            execute_commands_sequentially(ssh_client, COMMANDS[:5])

            # Execute the last two commands in parallel
            execute_commands_in_parallel(ssh_client, COMMANDS[5:])

            ssh_client.close()
            print(f"Connection to {server['hostname']} closed.")

if __name__ == "__main__":
    main()
