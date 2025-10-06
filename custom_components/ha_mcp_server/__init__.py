"""Home Assistant MCP Server Integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .mcp_server import MCPConfigServer

_LOGGER = logging.getLogger(__name__)

DOMAIN = "ha_mcp_server"
PLATFORMS: list[Platform] = []


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
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    _LOGGER.info("Home Assistant MCP Server setup complete")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.info("Unloading Home Assistant MCP Server")
    
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok


async def async_setup(hass: HomeAssistant, config: dict[str, Any]) -> bool:
    """Set up the Home Assistant MCP Server component."""
    hass.data.setdefault(DOMAIN, {})
    return True
