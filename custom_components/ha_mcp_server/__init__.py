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
SERVICE_READ_CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required("filename"): cv.string,
    }
)

SERVICE_WRITE_CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required("filename"): cv.string,
        vol.Required("content"): vol.Any(dict, str),
    }
)

SERVICE_LIST_CONFIGS_SCHEMA = vol.Schema({})

SERVICE_GET_CONFIG_VALUE_SCHEMA = vol.Schema(
    {
        vol.Required("filename"): cv.string,
        vol.Required("key_path"): cv.string,
    }
)

SERVICE_SET_CONFIG_VALUE_SCHEMA = vol.Schema(
    {
        vol.Required("filename"): cv.string,
        vol.Required("key_path"): cv.string,
        vol.Required("value"): vol.Any(str, int, float, bool, dict, list),
    }
)

# New service schemas for HA data access
SERVICE_LIST_USERS_SCHEMA = vol.Schema({})

SERVICE_GET_USER_SCHEMA = vol.Schema(
    {
        vol.Required("user_id"): cv.string,
    }
)

SERVICE_LIST_INTEGRATIONS_SCHEMA = vol.Schema({})

SERVICE_GET_INTEGRATION_SCHEMA = vol.Schema(
    {
        vol.Required("entry_id"): cv.string,
    }
)

SERVICE_LIST_DEVICES_SCHEMA = vol.Schema(
    {
        vol.Optional("domain"): cv.string,
    }
)

SERVICE_GET_DEVICE_SCHEMA = vol.Schema(
    {
        vol.Required("device_id"): cv.string,
    }
)

SERVICE_LIST_ENTITIES_SCHEMA = vol.Schema(
    {
        vol.Optional("domain"): cv.string,
    }
)

SERVICE_GET_ENTITY_SCHEMA = vol.Schema(
    {
        vol.Required("entity_id"): cv.entity_id,
    }
)

SERVICE_UPDATE_ENTITY_STATE_SCHEMA = vol.Schema(
    {
        vol.Required("entity_id"): cv.entity_id,
        vol.Required("state"): cv.string,
        vol.Optional("attributes"): dict,
    }
)

SERVICE_GET_ENTITY_HISTORY_SCHEMA = vol.Schema(
    {
        vol.Required("entity_id"): cv.entity_id,
        vol.Optional("start_time"): cv.string,
        vol.Optional("end_time"): cv.string,
    }
)


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

    async def handle_list_users(call: ServiceCall) -> None:
        """Handle list_users service call."""
        from homeassistant.auth.models import User

        users = []
        for user in hass.auth.async_get_users():
            users.append(
                {
                    "id": user.id,
                    "name": user.name,
                    "is_owner": user.is_owner,
                    "is_active": user.is_active,
                    "system_generated": user.system_generated,
                    "local_only": user.local_only,
                }
            )
        _LOGGER.info(f"Listed {len(users)} users")
        return {"users": users}

    async def handle_get_user(call: ServiceCall) -> None:
        """Handle get_user service call."""
        user_id = call.data["user_id"]
        user = await hass.auth.async_get_user(user_id)
        if user:
            result = {
                "id": user.id,
                "name": user.name,
                "is_owner": user.is_owner,
                "is_active": user.is_active,
                "system_generated": user.system_generated,
                "local_only": user.local_only,
                "groups": [{"id": g.id, "name": g.name} for g in user.groups],
            }
            _LOGGER.info(f"Got user {user_id}")
            return result
        else:
            raise ValueError(f"User {user_id} not found")

    async def handle_list_integrations(call: ServiceCall) -> None:
        """Handle list_integrations service call."""
        entries = []
        for entry in hass.config_entries.async_entries():
            entries.append(
                {
                    "entry_id": entry.entry_id,
                    "domain": entry.domain,
                    "title": entry.title,
                    "state": entry.state.name,
                    "source": entry.source,
                }
            )
        _LOGGER.info(f"Listed {len(entries)} integrations")
        return {"integrations": entries}

    async def handle_get_integration(call: ServiceCall) -> None:
        """Handle get_integration service call."""
        entry_id = call.data["entry_id"]
        entry = hass.config_entries.async_get_entry(entry_id)
        if entry:
            result = {
                "entry_id": entry.entry_id,
                "domain": entry.domain,
                "title": entry.title,
                "state": entry.state.name,
                "source": entry.source,
                "data": dict(entry.data),
                "options": dict(entry.options),
            }
            _LOGGER.info(f"Got integration {entry_id}")
            return result
        else:
            raise ValueError(f"Integration {entry_id} not found")

    async def handle_list_devices(call: ServiceCall) -> None:
        """Handle list_devices service call."""
        import homeassistant.helpers.device_registry as dr

        device_registry = dr.async_get(hass)
        domain = call.data.get("domain")

        devices = []
        for device in device_registry.devices.values():
            if domain is None or any(
                entry[0] == domain for entry in device.config_entries
            ):
                devices.append(
                    {
                        "id": device.id,
                        "name": device.name or device.name_by_user,
                        "manufacturer": device.manufacturer,
                        "model": device.model,
                        "sw_version": device.sw_version,
                        "identifiers": list(device.identifiers),
                        "connections": list(device.connections),
                    }
                )
        _LOGGER.info(f"Listed {len(devices)} devices")
        return {"devices": devices}

    async def handle_get_device(call: ServiceCall) -> None:
        """Handle get_device service call."""
        import homeassistant.helpers.device_registry as dr

        device_registry = dr.async_get(hass)
        device_id = call.data["device_id"]
        device = device_registry.async_get(device_id)

        if device:
            result = {
                "id": device.id,
                "name": device.name or device.name_by_user,
                "manufacturer": device.manufacturer,
                "model": device.model,
                "sw_version": device.sw_version,
                "hw_version": device.hw_version,
                "identifiers": list(device.identifiers),
                "connections": list(device.connections),
                "config_entries": list(device.config_entries),
                "area_id": device.area_id,
                "disabled_by": device.disabled_by,
            }
            _LOGGER.info(f"Got device {device_id}")
            return result
        else:
            raise ValueError(f"Device {device_id} not found")

    async def handle_list_entities(call: ServiceCall) -> None:
        """Handle list_entities service call."""
        import homeassistant.helpers.entity_registry as er

        entity_registry = er.async_get(hass)
        domain = call.data.get("domain")

        entities = []
        for entity in entity_registry.entities.values():
            if domain is None or entity.domain == domain:
                state = hass.states.get(entity.entity_id)
                entities.append(
                    {
                        "entity_id": entity.entity_id,
                        "name": entity.name or entity.original_name,
                        "platform": entity.platform,
                        "domain": entity.domain,
                        "device_id": entity.device_id,
                        "area_id": entity.area_id,
                        "disabled_by": entity.disabled_by,
                        "state": state.state if state else None,
                    }
                )
        _LOGGER.info(f"Listed {len(entities)} entities")
        return {"entities": entities}

    async def handle_get_entity(call: ServiceCall) -> None:
        """Handle get_entity service call."""
        import homeassistant.helpers.entity_registry as er

        entity_registry = er.async_get(hass)
        entity_id = call.data["entity_id"]

        entity = entity_registry.async_get(entity_id)
        state = hass.states.get(entity_id)

        result = {}
        if entity:
            result.update(
                {
                    "entity_id": entity.entity_id,
                    "name": entity.name or entity.original_name,
                    "platform": entity.platform,
                    "domain": entity.domain,
                    "device_id": entity.device_id,
                    "area_id": entity.area_id,
                    "disabled_by": entity.disabled_by,
                    "unique_id": entity.unique_id,
                    "capabilities": entity.capabilities,
                    "supported_features": entity.supported_features,
                    "device_class": entity.device_class,
                    "unit_of_measurement": entity.unit_of_measurement,
                }
            )

        if state:
            result.update(
                {
                    "state": state.state,
                    "attributes": dict(state.attributes),
                    "last_changed": state.last_changed.isoformat(),
                    "last_updated": state.last_updated.isoformat(),
                }
            )

        if not entity and not state:
            raise ValueError(f"Entity {entity_id} not found")

        _LOGGER.info(f"Got entity {entity_id}")
        return result

    async def handle_update_entity_state(call: ServiceCall) -> None:
        """Handle update_entity_state service call."""
        entity_id = call.data["entity_id"]
        state = call.data["state"]
        attributes = call.data.get("attributes", {})

        hass.states.async_set(entity_id, state, attributes)
        _LOGGER.info(f"Updated entity state {entity_id} to {state}")

    async def handle_get_entity_history(call: ServiceCall) -> None:
        """Handle get_entity_history service call."""
        from homeassistant.components import history
        from datetime import datetime, timedelta
        import homeassistant.util.dt as dt_util

        entity_id = call.data["entity_id"]
        start_time_str = call.data.get("start_time")
        end_time_str = call.data.get("end_time")

        # Parse time strings or use defaults
        if start_time_str:
            start_time = dt_util.parse_datetime(start_time_str)
        else:
            start_time = dt_util.now() - timedelta(hours=24)

        if end_time_str:
            end_time = dt_util.parse_datetime(end_time_str)
        else:
            end_time = dt_util.now()

        # Get history
        history_list = await hass.async_add_executor_job(
            history.state_changes_during_period, hass, start_time, end_time, entity_id
        )

        result = []
        if entity_id in history_list:
            for state in history_list[entity_id]:
                result.append(
                    {
                        "state": state.state,
                        "attributes": dict(state.attributes),
                        "last_changed": state.last_changed.isoformat(),
                        "last_updated": state.last_updated.isoformat(),
                    }
                )

        _LOGGER.info(f"Got {len(result)} history entries for {entity_id}")
        return {"history": result}

    # Register config file services
    # Register config file services
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
        DOMAIN,
        "get_config_value",
        handle_get_config_value,
        schema=SERVICE_GET_CONFIG_VALUE_SCHEMA,
    )
    hass.services.async_register(
        DOMAIN,
        "set_config_value",
        handle_set_config_value,
        schema=SERVICE_SET_CONFIG_VALUE_SCHEMA,
    )

    # Register HA data access services
    hass.services.async_register(
        DOMAIN, "list_users", handle_list_users, schema=SERVICE_LIST_USERS_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, "get_user", handle_get_user, schema=SERVICE_GET_USER_SCHEMA
    )
    hass.services.async_register(
        DOMAIN,
        "list_integrations",
        handle_list_integrations,
        schema=SERVICE_LIST_INTEGRATIONS_SCHEMA,
    )
    hass.services.async_register(
        DOMAIN,
        "get_integration",
        handle_get_integration,
        schema=SERVICE_GET_INTEGRATION_SCHEMA,
    )
    hass.services.async_register(
        DOMAIN, "list_devices", handle_list_devices, schema=SERVICE_LIST_DEVICES_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, "get_device", handle_get_device, schema=SERVICE_GET_DEVICE_SCHEMA
    )
    hass.services.async_register(
        DOMAIN,
        "list_entities",
        handle_list_entities,
        schema=SERVICE_LIST_ENTITIES_SCHEMA,
    )
    hass.services.async_register(
        DOMAIN, "get_entity", handle_get_entity, schema=SERVICE_GET_ENTITY_SCHEMA
    )
    hass.services.async_register(
        DOMAIN,
        "update_entity_state",
        handle_update_entity_state,
        schema=SERVICE_UPDATE_ENTITY_STATE_SCHEMA,
    )
    hass.services.async_register(
        DOMAIN,
        "get_entity_history",
        handle_get_entity_history,
        schema=SERVICE_GET_ENTITY_HISTORY_SCHEMA,
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    _LOGGER.info("Home Assistant MCP Server setup complete")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.info("Unloading Home Assistant MCP Server")

    # Unregister config file services
    hass.services.async_remove(DOMAIN, "read_config")
    hass.services.async_remove(DOMAIN, "write_config")
    hass.services.async_remove(DOMAIN, "list_configs")
    hass.services.async_remove(DOMAIN, "get_config_value")
    hass.services.async_remove(DOMAIN, "set_config_value")

    # Unregister HA data access services
    hass.services.async_remove(DOMAIN, "list_users")
    hass.services.async_remove(DOMAIN, "get_user")
    hass.services.async_remove(DOMAIN, "list_integrations")
    hass.services.async_remove(DOMAIN, "get_integration")
    hass.services.async_remove(DOMAIN, "list_devices")
    hass.services.async_remove(DOMAIN, "get_device")
    hass.services.async_remove(DOMAIN, "list_entities")
    hass.services.async_remove(DOMAIN, "get_entity")
    hass.services.async_remove(DOMAIN, "update_entity_state")
    hass.services.async_remove(DOMAIN, "get_entity_history")

    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_setup(hass: HomeAssistant, config: dict[str, Any]) -> bool:
    """Set up the Home Assistant MCP Server component."""
    hass.data.setdefault(DOMAIN, {})
    return True
