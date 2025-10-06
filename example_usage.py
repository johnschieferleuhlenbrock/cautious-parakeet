"""Example usage of the Home Assistant MCP Server."""
import asyncio
from pathlib import Path

from custom_components.ha_mcp_server.mcp_server import MCPConfigServer


async def main():
    """Run example operations with the MCP server."""
    # Initialize the MCP server with a config path
    # In production, this would be the Home Assistant config directory
    config_path = "/config"  # Home Assistant config directory
    mcp_server = MCPConfigServer(config_path)
    
    print("Home Assistant MCP Server - Example Usage\n")
    
    # Example 1: List configuration files
    print("1. Listing configuration files:")
    try:
        files = await mcp_server.list_config_files()
        for file in files:
            print(f"   - {file}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n2. Reading configuration.yaml:")
    try:
        config = await mcp_server.read_config_file("configuration.yaml")
        print(f"   Home Assistant name: {config.get('homeassistant', {}).get('name', 'Not set')}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n3. Getting a specific configuration value:")
    try:
        name = await mcp_server.get_config_value("configuration.yaml", "homeassistant.name")
        print(f"   Value: {name}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n4. Setting a configuration value:")
    try:
        await mcp_server.set_config_value(
            "configuration.yaml",
            "homeassistant.name",
            "My Smart Home"
        )
        print("   Successfully updated homeassistant.name")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n5. Writing a new automation file:")
    try:
        automation_config = {
            "automation": [
                {
                    "alias": "Example Automation",
                    "trigger": {
                        "platform": "state",
                        "entity_id": "sun.sun",
                        "to": "below_horizon"
                    },
                    "action": {
                        "service": "light.turn_on",
                        "target": {
                            "entity_id": "light.living_room"
                        }
                    }
                }
            ]
        }
        await mcp_server.write_config_file("example_automation.yaml", automation_config)
        print("   Successfully created example_automation.yaml")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\nExample complete!")


if __name__ == "__main__":
    asyncio.run(main())
