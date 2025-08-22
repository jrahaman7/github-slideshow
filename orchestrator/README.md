# Simple SSH Orchestrator

This tool allows you to run sequences of commands on multiple remote hosts via SSH. It is configured using a YAML file (`config.yml`) and can execute commands both sequentially and in parallel.

## Configuration

The orchestrator is configured using the `config.yml` file. This file defines the hosts you want to connect to and the command sequences you want to run.

### `hosts`

The `hosts` section is a list of host definitions. Each host has a unique `name` and a `config` block that is passed directly to Fabric's `Connection` class.

**Example:**
```yaml
hosts:
  - name: db_server
    config:
      host: 192.168.1.100
      user: oracle
      connect_kwargs:
        password: "your_password" # For testing; key-based auth is recommended
  - name: app_server_1
    config:
      host: 192.168.1.101
      user: weblogic
      connect_kwargs:
        key_filename: "/path/to/your/private/key"
```

### `command_sequences`

The `command_sequences` section defines named workflows. Each sequence is a list of steps. Each step specifies:
- `name`: A descriptive name for the step (used for logging).
- `hosts`: A list of host `name`s (from the `hosts` section) on which to run the commands.
- `parallel`: `true` to run the commands on all specified hosts at the same time, `false` to run them one by one.
- `commands`: A list of shell commands to execute on the hosts.

**Example:**
```yaml
command_sequences:
  start_services:
    - name: "Start Database"
      hosts: [db_server]
      parallel: false
      commands:
        - "start_db_service.sh"
    - name: "Start Web Servers"
      hosts: [app_server_1, app_server_2]
      parallel: true
      commands:
        - "start_web_server.sh"
```

## Usage

To run a command sequence, execute the `orchestrator.py` script, passing the name of the sequence as an argument.

```bash
python3 orchestrator/orchestrator.py <sequence_name>
```

### Example

To run the `start_services` sequence defined above:
```bash
python3 orchestrator/orchestrator.py start_services
```

You can also specify a different configuration file using the `--config` flag:
```bash
python3 orchestrator/orchestrator.py start_services --config my_custom_config.yml
```
