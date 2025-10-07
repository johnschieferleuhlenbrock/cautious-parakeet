# Quick Start Guide

This guide will help you quickly set up and start using the Home Assistant MCP Server.

## Prerequisites

- Home Assistant installed and running
- HACS (Home Assistant Community Store) installed
- Basic understanding of Home Assistant configuration

## Installation Steps

### 1. Add Custom Repository to HACS

1. Open Home Assistant
2. Navigate to HACS (sidebar menu)
3. Click on "Integrations"
4. Click the three dots (⋮) in the top right corner
5. Select "Custom repositories"
6. Add the following:
   - **Repository URL**: `https://github.com/johnschieferleuhlenbrock/cautious-parakeet`
   - **Category**: Integration
7. Click "Add"

### 2. Install the Integration

1. In HACS, search for "Home Assistant MCP Server"
2. Click on the integration
3. Click "Download"
4. Restart Home Assistant

### 3. Configure the Integration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "Home Assistant MCP Server"
4. Click to add it
5. Configure the server port (default: 3000)
6. Click **Submit**

## First Steps

### Using Services

Once installed, you can use the MCP Server services from the Developer Tools:

1. Go to **Developer Tools** → **Services**
2. Search for services starting with `ha_mcp_server.`

### Example: Read Configuration

```yaml
service: ha_mcp_server.read_config
data:
  filename: "configuration.yaml"
```

### Example: List Configuration Files

```yaml
service: ha_mcp_server.list_configs
```

### Example: Get a Configuration Value

```yaml
service: ha_mcp_server.get_config_value
data:
  filename: "configuration.yaml"
  key_path: "homeassistant.name"
```

### Example: Set a Configuration Value

```yaml
service: ha_mcp_server.set_config_value
data:
  filename: "configuration.yaml"
  key_path: "homeassistant.name"
  value: "My Smart Home"
```

### Example: List All Users

```yaml
service: ha_mcp_server.list_users
```

### Example: List All Entities

```yaml
service: ha_mcp_server.list_entities
```

### Example: Get Entity Details

```yaml
service: ha_mcp_server.get_entity
data:
  entity_id: "light.living_room"
```

### Example: List Devices by Domain

```yaml
service: ha_mcp_server.list_devices
data:
  domain: "light"
```

## Common Use Cases

### 1. Backup Configuration Before Editing

```yaml
service: ha_mcp_server.read_config
data:
  filename: "automations.yaml"
```

### 2. Update Home Name Programmatically

```yaml
service: ha_mcp_server.set_config_value
data:
  filename: "configuration.yaml"
  key_path: "homeassistant.name"
  value: "New Home Name"
```

### 3. Create New Automation File

```yaml
service: ha_mcp_server.write_config
data:
  filename: "new_automations.yaml"
  content:
    automation:
      - alias: "Example"
        trigger:
          platform: state
          entity_id: sun.sun
        action:
          service: light.turn_on
```

### 4. Monitor Entity State Changes

```yaml
service: ha_mcp_server.get_entity_history
data:
  entity_id: "sensor.temperature"
  start_time: "2024-01-01T00:00:00+00:00"
```

### 5. Audit System Configuration

```yaml
# List all integrations
service: ha_mcp_server.list_integrations

# List all users
service: ha_mcp_server.list_users

# List all devices
service: ha_mcp_server.list_devices
```

### 6. Find Entities by Domain

```yaml
service: ha_mcp_server.list_entities
data:
  domain: "sensor"
```

## Security Best Practices

1. **Restrict Access**: Only trusted users should have access to these services
2. **Backup First**: Always backup your configuration before making changes
3. **Test Changes**: Test configuration changes in a development environment first
4. **Monitor Logs**: Check Home Assistant logs for any errors

## Troubleshooting

### Service Not Available

- Ensure the integration is properly installed
- Restart Home Assistant
- Check the logs for errors

### File Not Found

- Verify the filename is correct
- Check that the file exists in your config directory
- Ensure proper file extensions (.yaml, .json, etc.)

### Permission Denied

- Check file permissions in your config directory
- Ensure Home Assistant has write access

## Next Steps

- Explore the [full documentation](README.md)
- Check out the [example usage script](example_usage.py)
- Read about [contributing](CONTRIBUTING.md)

## Support

For issues or questions:
- Open an issue on [GitHub](https://github.com/johnschieferleuhlenbrock/cautious-parakeet/issues)
- Check the [discussions](https://github.com/johnschieferleuhlenbrock/cautious-parakeet/discussions)
