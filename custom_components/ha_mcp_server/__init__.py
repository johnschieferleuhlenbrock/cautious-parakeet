"""Home Assistant MCP Server Integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
import homeassistant.helpers.config_validation as cv

from .mcp_server import MCPConfigServer

_LOGGER = logging.getLogger(__name__)

DOMAIN = "ha_mcp_server"
PLATFORMS: list[Platform] = []

# Service schemas
SERVICE_READ_CONFIG_SCHEMA = vol.Schema({
    vol.Required("filename"): cv.string,
})

SERVICE_WRITE_CONFIG_SCHEMA = vol.Schema({
    vol.Required("filename"): cv.string,
    vol.Required("content"): vol.Any(dict, str),
})

SERVICE_LIST_CONFIGS_SCHEMA = vol.Schema({})

SERVICE_GET_CONFIG_VALUE_SCHEMA = vol.Schema({
    vol.Required("filename"): cv.string,
    vol.Required("key_path"): cv.string,
})

SERVICE_SET_CONFIG_VALUE_SCHEMA = vol.Schema({
    vol.Required("filename"): cv.string,
    vol.Required("key_path"): cv.string,
    vol.Required("value"): vol.Any(str, int, float, bool, dict, list),
})


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Home Assistant MCP Server from a config entry."""
    _LOGGER.info("Setting up Home Assistant MCP Server")
    
    # Store the MCP server instance
    hass.data.setdefault(DOMAIN, {})
    
    # Initialize MCP server
    config_path = hass.config.path()
    mcp_server = MCPConfigServer(config_path)
    
    hass.data[DOMAIN][entry.entry_id] = {
        "server": mcp_server,
    }
    
    # Register services
    async def handle_read_config(call: ServiceCall) -> None:
        """Handle read_config service call."""
        filename = call.data["filename"]
        result = await mcp_server.read_config_file(filename)
        _LOGGER.info(f"Read config file {filename}")
        return result

    async def handle_write_config(call: ServiceCall) -> None:
        """Handle write_config service call."""
        filename = call.data["filename"]
        content = call.data["content"]
        await mcp_server.write_config_file(filename, content)
        _LOGGER.info(f"Wrote config file {filename}")

    async def handle_list_configs(call: ServiceCall) -> None:
        """Handle list_configs service call."""
        result = await mcp_server.list_config_files()
        _LOGGER.info(f"Listed {len(result)} config files")
        return result

    async def handle_get_config_value(call: ServiceCall) -> None:
        """Handle get_config_value service call."""
        filename = call.data["filename"]
        key_path = call.data["key_path"]
        result = await mcp_server.get_config_value(filename, key_path)
        _LOGGER.info(f"Got config value {key_path} from {filename}")
        return result

    async def handle_set_config_value(call: ServiceCall) -> None:
        """Handle set_config_value service call."""
        filename = call.data["filename"]
        key_path = call.data["key_path"]
        value = call.data["value"]
        await mcp_server.set_config_value(filename, key_path, value)
        _LOGGER.info(f"Set config value {key_path} in {filename}")

    hass.services.async_register(
        DOMAIN, "read_config", handle_read_config, schema=SERVICE_READ_CONFIG_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, "write_config", handle_write_config, schema=SERVICE_WRITE_CONFIG_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, "list_configs", handle_list_configs, schema=SERVICE_LIST_CONFIGS_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, "get_config_value", handle_get_config_value, schema=SERVICE_GET_CONFIG_VALUE_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, "set_config_value", handle_set_config_value, schema=SERVICE_SET_CONFIG_VALUE_SCHEMA
    )
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    _LOGGER.info("Home Assistant MCP Server setup complete")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.info("Unloading Home Assistant MCP Server")
    
    # Unregister services
    hass.services.async_remove(DOMAIN, "read_config")
    hass.services.async_remove(DOMAIN, "write_config")
    hass.services.async_remove(DOMAIN, "list_configs")
    hass.services.async_remove(DOMAIN, "get_config_value")
    hass.services.async_remove(DOMAIN, "set_config_value")
    
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok


async def async_setup(hass: HomeAssistant, config: dict[str, Any]) -> bool:
    """Set up the Home Assistant MCP Server component."""
    hass.data.setdefault(DOMAIN, {})
    return True
