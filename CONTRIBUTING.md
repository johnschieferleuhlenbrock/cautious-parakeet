# Contributing to Home Assistant MCP Server

Thank you for your interest in contributing to the Home Assistant MCP Server! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/cautious-parakeet.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`

## Development Setup

### Prerequisites

- Python 3.11 or higher
- Home Assistant (for testing)
- Basic understanding of Home Assistant custom components

### Installation for Development

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy the `custom_components/ha_mcp_server` directory to your Home Assistant's `custom_components` directory

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to all functions and classes
- Keep functions focused and small

## Testing

Before submitting a pull request:

1. Test the integration in a Home Assistant development environment
2. Verify all JSON files are valid
3. Check Python syntax: `python3 -m py_compile custom_components/ha_mcp_server/*.py`
4. Ensure no security vulnerabilities are introduced

## Submitting Changes

1. Commit your changes with clear, descriptive commit messages
2. Push to your fork
3. Create a Pull Request with:
   - Clear description of the changes
   - Reference to any related issues
   - Screenshots if UI changes are involved

## Reporting Issues

When reporting issues, please include:

- Home Assistant version
- Integration version
- Steps to reproduce
- Expected vs actual behavior
- Relevant logs

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person

## Questions?

Feel free to open an issue for questions or discussions.

Thank you for contributing!
