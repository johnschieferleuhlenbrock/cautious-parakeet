# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-XX

### Added
- Initial release of Home Assistant MCP Server
- MCP server implementation for configuration file access
- Read configuration files (YAML, JSON, text)
- Write configuration files
- List configuration files in Home Assistant config directory
- Get specific configuration values using dot-notation key paths
- Set specific configuration values
- Home Assistant service integration
  - `read_config` service
  - `write_config` service
  - `list_configs` service
  - `get_config_value` service
  - `set_config_value` service
- HACS integration support
- Config flow for easy setup through Home Assistant UI
- Security features:
  - Path traversal protection
  - File access restricted to HA config directory
  - File type validation
- Complete documentation and examples
- Example usage script

### Security
- Implemented path traversal prevention
- Restricted file access to Home Assistant configuration directory only
- Added file extension validation

[1.0.0]: https://github.com/johnschieferleuhlenbrock/cautious-parakeet/releases/tag/v1.0.0
