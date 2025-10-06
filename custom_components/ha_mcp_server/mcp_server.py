"""MCP Server for Home Assistant Configuration Management."""
from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any

import aiofiles
import yaml

_LOGGER = logging.getLogger(__name__)


class MCPConfigServer:
    """MCP Server for managing Home Assistant configuration files."""

    def __init__(self, config_path: str):
        """Initialize the MCP Config Server.
        
        Args:
            config_path: Path to Home Assistant configuration directory
        """
        self.config_path = Path(config_path)
        _LOGGER.info(f"Initialized MCP Server with config path: {self.config_path}")

    async def read_config_file(self, filename: str) -> dict[str, Any]:
        """Read a configuration file.
        
        Args:
            filename: Name of the configuration file to read
            
        Returns:
            Dictionary containing the file contents
        """
        file_path = self.config_path / filename
        
        # Security check: ensure file is within config directory
        if not self._is_safe_path(file_path):
            raise ValueError(f"Access to {filename} is not allowed")
        
        if not file_path.exists():
            raise FileNotFoundError(f"File {filename} not found")
        
        async with aiofiles.open(file_path, 'r') as f:
            content = await f.read()
        
        # Parse based on file extension
        if filename.endswith('.yaml') or filename.endswith('.yml'):
            return yaml.safe_load(content) or {}
        elif filename.endswith('.json'):
            return json.loads(content)
        else:
            return {"content": content}

    async def write_config_file(self, filename: str, content: dict[str, Any] | str) -> bool:
        """Write to a configuration file.
        
        Args:
            filename: Name of the configuration file to write
            content: Content to write (dict for YAML/JSON, str for text)
            
        Returns:
            True if successful
        """
        file_path = self.config_path / filename
        
        # Security check: ensure file is within config directory
        if not self._is_safe_path(file_path):
            raise ValueError(f"Access to {filename} is not allowed")
        
        # Format content based on file extension
        if filename.endswith('.yaml') or filename.endswith('.yml'):
            if isinstance(content, str):
                formatted_content = content
            else:
                formatted_content = yaml.dump(content, default_flow_style=False)
        elif filename.endswith('.json'):
            if isinstance(content, str):
                formatted_content = content
            else:
                formatted_content = json.dumps(content, indent=2)
        else:
            formatted_content = content if isinstance(content, str) else str(content)
        
        async with aiofiles.open(file_path, 'w') as f:
            await f.write(formatted_content)
        
        _LOGGER.info(f"Successfully wrote to {filename}")
        return True

    async def list_config_files(self) -> list[str]:
        """List all configuration files in the config directory.
        
        Returns:
            List of configuration file names
        """
        config_files = []
        
        for file_path in self.config_path.iterdir():
            if file_path.is_file():
                # Filter for common config file extensions
                if file_path.suffix in ['.yaml', '.yml', '.json', '.conf', '.txt']:
                    config_files.append(file_path.name)
        
        return sorted(config_files)

    async def get_config_value(self, filename: str, key_path: str) -> Any:
        """Get a specific value from a configuration file.
        
        Args:
            filename: Name of the configuration file
            key_path: Dot-separated path to the configuration key (e.g., 'homeassistant.name')
            
        Returns:
            The value at the specified key path
        """
        config = await self.read_config_file(filename)
        
        keys = key_path.split('.')
        value = config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                raise KeyError(f"Key path {key_path} not found in {filename}")
        
        return value

    async def set_config_value(self, filename: str, key_path: str, value: Any) -> bool:
        """Set a specific value in a configuration file.
        
        Args:
            filename: Name of the configuration file
            key_path: Dot-separated path to the configuration key
            value: Value to set
            
        Returns:
            True if successful
        """
        config = await self.read_config_file(filename)
        
        keys = key_path.split('.')
        current = config
        
        # Navigate to the parent of the target key
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        # Set the value
        current[keys[-1]] = value
        
        return await self.write_config_file(filename, config)

    def _is_safe_path(self, path: Path) -> bool:
        """Check if the path is safe (within config directory).
        
        Args:
            path: Path to check
            
        Returns:
            True if path is safe
        """
        try:
            path.resolve().relative_to(self.config_path.resolve())
            return True
        except ValueError:
            return False
