# Architecture

## Overview

The Home Assistant MCP Server provides a Model Context Protocol (MCP) interface for managing Home Assistant configuration files. This document explains the architecture and design decisions.

## Components

### 1. MCP Server Core (`mcp_server.py`)

The core server implementation provides:

- **File Operations**: Read, write, list configuration files
- **Value Operations**: Get and set specific configuration values
- **Security Layer**: Path validation and file type filtering
- **Format Support**: YAML, JSON, and text file handling

```
┌─────────────────────────────────────┐
│      MCPConfigServer                │
│                                     │
│  - read_config_file()               │
│  - write_config_file()              │
│  - list_config_files()              │
│  - get_config_value()               │
│  - set_config_value()               │
│  - _is_safe_path()                  │
└─────────────────────────────────────┘
```

### 2. Home Assistant Integration (`__init__.py`)

Bridges the MCP server with Home Assistant:

- **Service Registration**: Exposes MCP operations as HA services
- **Lifecycle Management**: Setup and teardown
- **Error Handling**: Proper error propagation to HA

```
┌─────────────────────────────────────┐
│   Home Assistant Integration        │
│                                     │
│  Services:                          │
│  - ha_mcp_server.read_config        │
│  - ha_mcp_server.write_config       │
│  - ha_mcp_server.list_configs       │
│  - ha_mcp_server.get_config_value   │
│  - ha_mcp_server.set_config_value   │
└─────────────────────────────────────┘
```

### 3. Configuration Flow (`config_flow.py`)

Provides UI-based configuration:

- **User Interface**: Simple configuration dialog
- **Validation**: Port number validation
- **Unique ID**: Prevents duplicate installations

### 4. Service Definitions (`services.yaml`)

Defines service schemas for Home Assistant:

- **Field Validation**: Input validation
- **Documentation**: Service descriptions
- **UI Generation**: Automatic service UI in HA

## Data Flow

### Reading a Configuration File

```
User/AI Agent
     │
     ├─> Home Assistant Service Call
     │         │
     │         ├─> Integration Layer
     │         │         │
     │         │         ├─> MCP Server
     │         │         │       │
     │         │         │       ├─> Security Check
     │         │         │       │
     │         │         │       ├─> Read File
     │         │         │       │
     │         │         │       ├─> Parse (YAML/JSON)
     │         │         │       │
     │         │         │       └─> Return Data
     │         │         │
     │         │         └─> Return to Service
     │         │
     │         └─> Return to User
     │
     └─> Receive Configuration Data
```

### Writing a Configuration File

```
User/AI Agent
     │
     ├─> Home Assistant Service Call
     │         │
     │         ├─> Integration Layer
     │         │         │
     │         │         ├─> MCP Server
     │         │         │       │
     │         │         │       ├─> Security Check
     │         │         │       │
     │         │         │       ├─> Format Data (YAML/JSON)
     │         │         │       │
     │         │         │       ├─> Write File
     │         │         │       │
     │         │         │       └─> Return Success
     │         │         │
     │         │         └─> Return to Service
     │         │
     │         └─> Confirm to User
     │
     └─> Operation Complete
```

## Security Architecture

### Path Validation

```python
def _is_safe_path(self, path: Path) -> bool:
    """
    Ensures the requested path is within the config directory.
    Prevents path traversal attacks like ../../../etc/passwd
    """
    try:
        path.resolve().relative_to(self.config_path.resolve())
        return True
    except ValueError:
        return False
```

### File Type Filtering

Only allows specific file extensions:
- `.yaml` - YAML configuration files
- `.yml` - YAML configuration files (alternate extension)
- `.json` - JSON configuration files
- `.conf` - Configuration files
- `.txt` - Text files

### Access Control

- **Directory Restriction**: All operations restricted to HA config directory
- **No Elevation**: Runs with same privileges as Home Assistant
- **Input Validation**: All inputs validated before processing

## File Format Handling

### YAML Files

- Parsed using `yaml.safe_load()` for security
- Written using `yaml.dump()` with proper formatting
- Preserves structure and comments where possible

### JSON Files

- Parsed using `json.loads()`
- Written using `json.dumps()` with indentation
- Proper error handling for malformed JSON

### Text Files

- Read and written as plain text
- Returned in `{"content": "..."}` format
- No parsing applied

## Error Handling

### File Not Found
- Returns `FileNotFoundError` with descriptive message
- Logged at INFO level

### Permission Denied
- Returns `PermissionError` with descriptive message
- Logged at ERROR level

### Invalid Path
- Returns `ValueError` with security message
- Logged at WARNING level

### Parse Errors
- Returns format-specific errors (YAML/JSON)
- Logged at ERROR level with details

## Extension Points

The architecture supports future extensions:

1. **Additional File Formats**: Add parsers for new formats
2. **Remote Access**: Add network protocol support
3. **Backup/Restore**: Implement versioning
4. **Change Validation**: Validate config before writing
5. **Audit Logging**: Track all changes

## Performance Considerations

- **Async I/O**: All file operations are asynchronous using `aiofiles`
- **Lazy Loading**: Files only loaded when requested
- **No Caching**: Always reads from disk for consistency
- **Minimal Memory**: Streams large files when possible

## Testing Strategy

### Unit Tests
- Path validation
- File operations (read/write)
- Format parsing
- Security checks

### Integration Tests
- Service registration
- End-to-end operations
- Error scenarios

### Security Tests
- Path traversal prevention
- Permission boundaries
- Input validation

## Deployment

### HACS Installation
- Standard HACS custom integration format
- Automatic updates through HACS
- Version management via `manifest.json`

### Manual Installation
- Copy to `custom_components` directory
- Restart Home Assistant
- Configure through UI

## Future Roadmap

1. **Real MCP Protocol**: Implement full MCP specification
2. **WebSocket Support**: Real-time config updates
3. **Diff/Merge**: Advanced configuration merging
4. **Templates**: Configuration templates
5. **Validation**: Pre-write configuration validation
