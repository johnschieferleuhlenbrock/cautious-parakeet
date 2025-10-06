# Home Assistant MCP Server

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

This integration provides a Model Context Protocol (MCP) server for Home Assistant, enabling AI assistants and other tools to read and edit Home Assistant configuration files through a standardized interface.

## Features

- **Read Configuration Files**: Access Home Assistant YAML, JSON, and text configuration files
- **Edit Configuration Files**: Modify configuration values programmatically
- **Secure Access**: File access is restricted to the Home Assistant configuration directory
- **MCP Protocol**: Implements the Model Context Protocol for standardized AI integration
- **Easy Installation**: Install through HACS (Home Assistant Community Store)

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
11. Configure the integration

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

Once installed, the MCP server provides the following capabilities:

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

## Security

- File access is restricted to the Home Assistant configuration directory
- Path traversal attempts are blocked
- Only common configuration file types are accessible (.yaml, .yml, .json, .conf, .txt)

## Support

For issues, feature requests, or contributions, please visit the [GitHub repository](https://github.com/johnschieferleuhlenbrock/cautious-parakeet).

## License

This project is open source and available under the MIT License.
