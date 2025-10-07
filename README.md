# Home Assistant MCP Server

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

A Model Context Protocol (MCP) server integration for Home Assistant that enables AI assistants and other tools to read and edit Home Assistant configuration files through a standardized interface.

## Features

- 🔍 **Read Configuration Files**: Access Home Assistant YAML, JSON, and text configuration files
- ✏️ **Edit Configuration Files**: Modify configuration values programmatically
- 👥 **User Management**: List and view Home Assistant users
- 🔌 **Integration Access**: View all configured integrations and their details
- 🖥️ **Device Management**: List and inspect devices
- 🏠 **Entity Operations**: Access, monitor, and control all entities
- 📊 **Entity History**: Retrieve historical state data for entities
- 🔒 **Secure Access**: File access is restricted to the Home Assistant configuration directory
- 🤖 **MCP Protocol**: Implements the Model Context Protocol for standardized AI integration
- 📦 **Easy Installation**: Install through HACS (Home Assistant Community Store)

## Installation

### HACS Installation (Recommended)

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add `https://github.com/johnschieferleuhlenbrock/cautious-parakeet` as an integration
6. Click "Install"
7. Restart Home Assistant
8. Go to Configuration > Integrations
9. Click "+ Add Integration"
10. Search for "Home Assistant MCP Server"

### Manual Installation

1. Copy the `custom_components/ha_mcp_server` directory to your Home Assistant's `custom_components` directory
2. Restart Home Assistant
3. Add the integration through the UI

## Configuration

The integration can be configured through the Home Assistant UI:

1. Go to Configuration > Integrations
2. Click "+ Add Integration"
3. Search for "Home Assistant MCP Server"
4. Configure the MCP server port (default: 3000)

## Usage

The MCP server provides the following capabilities through both Python API and Home Assistant services:

### Home Assistant Services

Once installed, you can use the following services in Home Assistant:

#### `ha_mcp_server.read_config`
Read a configuration file.

```yaml
service: ha_mcp_server.read_config
data:
  filename: "configuration.yaml"
```

#### `ha_mcp_server.write_config`
Write to a configuration file.

```yaml
service: ha_mcp_server.write_config
data:
  filename: "automations.yaml"
  content:
    automation: []
```

#### `ha_mcp_server.list_configs`
List all configuration files.

```yaml
service: ha_mcp_server.list_configs
```

#### `ha_mcp_server.get_config_value`
Get a specific value from a configuration file.

```yaml
service: ha_mcp_server.get_config_value
data:
  filename: "configuration.yaml"
  key_path: "homeassistant.name"
```

#### `ha_mcp_server.set_config_value`
Set a specific value in a configuration file.

```yaml
service: ha_mcp_server.set_config_value
data:
  filename: "configuration.yaml"
  key_path: "homeassistant.name"
  value: "My Smart Home"
```

#### `ha_mcp_server.list_users`
List all Home Assistant users.

```yaml
service: ha_mcp_server.list_users
```

#### `ha_mcp_server.get_user`
Get details of a specific user.

```yaml
service: ha_mcp_server.get_user
data:
  user_id: "1234567890abcdef"
```

#### `ha_mcp_server.list_integrations`
List all configured integrations.

```yaml
service: ha_mcp_server.list_integrations
```

#### `ha_mcp_server.get_integration`
Get details of a specific integration.

```yaml
service: ha_mcp_server.get_integration
data:
  entry_id: "1234567890abcdef"
```

#### `ha_mcp_server.list_devices`
List all devices or filter by domain.

```yaml
service: ha_mcp_server.list_devices
data:
  domain: "light"  # Optional
```

#### `ha_mcp_server.get_device`
Get details of a specific device.

```yaml
service: ha_mcp_server.get_device
data:
  device_id: "1234567890abcdef"
```

#### `ha_mcp_server.list_entities`
List all entities or filter by domain.

```yaml
service: ha_mcp_server.list_entities
data:
  domain: "light"  # Optional
```

#### `ha_mcp_server.get_entity`
Get details and current state of an entity.

```yaml
service: ha_mcp_server.get_entity
data:
  entity_id: "light.living_room"
```

#### `ha_mcp_server.update_entity_state`
Update the state of an entity.

```yaml
service: ha_mcp_server.update_entity_state
data:
  entity_id: "light.living_room"
  state: "on"
  attributes:  # Optional
    brightness: 255
```

#### `ha_mcp_server.get_entity_history`
Get historical state data for an entity.

```yaml
service: ha_mcp_server.get_entity_history
data:
  entity_id: "sensor.temperature"
  start_time: "2024-01-01T00:00:00+00:00"  # Optional, defaults to 24 hours ago
  end_time: "2024-01-02T00:00:00+00:00"  # Optional, defaults to now
```

### Python API

### Reading Configuration Files

```python
# List all configuration files
files = await mcp_server.list_config_files()

# Read a complete configuration file
config = await mcp_server.read_config_file("configuration.yaml")

# Get a specific configuration value
value = await mcp_server.get_config_value("configuration.yaml", "homeassistant.name")
```

### Editing Configuration Files

```python
# Write a complete configuration file
await mcp_server.write_config_file("automations.yaml", {"automation": []})

# Set a specific configuration value
await mcp_server.set_config_value("configuration.yaml", "homeassistant.name", "My Home")
```

## API Reference

### Configuration File Services

- `read_config_file(filename)`: Read a configuration file
- `write_config_file(filename, content)`: Write to a configuration file
- `list_config_files()`: List all configuration files
- `get_config_value(filename, key_path)`: Get a specific value from a config file
- `set_config_value(filename, key_path, value)`: Set a specific value in a config file

### Home Assistant Data Services

- `list_users()`: List all Home Assistant users
- `get_user(user_id)`: Get details of a specific user
- `list_integrations()`: List all configured integrations
- `get_integration(entry_id)`: Get details of a specific integration
- `list_devices(domain=None)`: List all devices, optionally filtered by domain
- `get_device(device_id)`: Get details of a specific device
- `list_entities(domain=None)`: List all entities, optionally filtered by domain
- `get_entity(entity_id)`: Get details and current state of an entity
- `update_entity_state(entity_id, state, attributes=None)`: Update the state of an entity
- `get_entity_history(entity_id, start_time=None, end_time=None)`: Get historical state data

## Security

- ✅ File access is restricted to the Home Assistant configuration directory
- ✅ Path traversal attempts are blocked
- ✅ Only common configuration file types are accessible (.yaml, .yml, .json, .conf, .txt)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, feature requests, or contributions, please visit the [GitHub repository](https://github.com/johnschieferleuhlenbrock/cautious-parakeet/issues).

## License

This project is open source and available under the MIT License.