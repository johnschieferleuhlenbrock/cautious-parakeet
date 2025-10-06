"""Example usage of the Home Assistant MCP Server - HA Data Access."""
import asyncio


async def main():
    """Run example operations with the MCP server HA data access services."""
    print("Home Assistant MCP Server - HA Data Access Examples\n")
    print("=" * 60)
    
    print("\n📋 Configuration File Services")
    print("-" * 60)
    print("""
1. Read Configuration File:
   service: ha_mcp_server.read_config
   data:
     filename: "configuration.yaml"

2. List Configuration Files:
   service: ha_mcp_server.list_configs
""")
    
    print("\n👥 User Management Services")
    print("-" * 60)
    print("""
1. List All Users:
   service: ha_mcp_server.list_users
   
   Returns:
   - User IDs
   - User names
   - Owner status
   - Active status
   - System generated flag

2. Get Specific User:
   service: ha_mcp_server.get_user
   data:
     user_id: "your-user-id-here"
   
   Returns detailed user information including groups
""")
    
    print("\n🔌 Integration Management Services")
    print("-" * 60)
    print("""
1. List All Integrations:
   service: ha_mcp_server.list_integrations
   
   Returns:
   - Entry IDs
   - Domain names
   - Titles
   - States (loaded, setup_error, etc.)
   - Sources (user, import, etc.)

2. Get Specific Integration:
   service: ha_mcp_server.get_integration
   data:
     entry_id: "your-entry-id-here"
   
   Returns detailed integration configuration and options
""")
    
    print("\n🖥️ Device Management Services")
    print("-" * 60)
    print("""
1. List All Devices:
   service: ha_mcp_server.list_devices
   
   Returns device information for all devices

2. List Devices by Domain:
   service: ha_mcp_server.list_devices
   data:
     domain: "light"
   
   Returns only devices from the specified domain

3. Get Specific Device:
   service: ha_mcp_server.get_device
   data:
     device_id: "your-device-id-here"
   
   Returns:
   - Device name
   - Manufacturer
   - Model
   - Software version
   - Identifiers
   - Connections
   - Area assignment
   - Disabled status
""")
    
    print("\n🏠 Entity Management Services")
    print("-" * 60)
    print("""
1. List All Entities:
   service: ha_mcp_server.list_entities
   
   Returns all entities with their current states

2. List Entities by Domain:
   service: ha_mcp_server.list_entities
   data:
     domain: "sensor"
   
   Returns only entities from the specified domain

3. Get Specific Entity:
   service: ha_mcp_server.get_entity
   data:
     entity_id: "light.living_room"
   
   Returns:
   - Entity metadata (name, domain, platform)
   - Current state
   - All attributes
   - Device and area associations
   - Capabilities and features
   - Last changed/updated timestamps

4. Update Entity State:
   service: ha_mcp_server.update_entity_state
   data:
     entity_id: "light.living_room"
     state: "on"
     attributes:
       brightness: 255
       color_temp: 370
   
   Updates the state and attributes of an entity
   (Useful for virtual entities or testing)

5. Get Entity History:
   service: ha_mcp_server.get_entity_history
   data:
     entity_id: "sensor.temperature"
     start_time: "2024-01-01T00:00:00+00:00"  # Optional
     end_time: "2024-01-02T00:00:00+00:00"    # Optional
   
   Returns:
   - Historical states
   - Attributes at each state change
   - Timestamps for all changes
   
   Defaults to last 24 hours if times not specified
""")
    
    print("\n💡 Use Cases")
    print("-" * 60)
    print("""
1. System Monitoring:
   - List all entities to check system health
   - Get entity history to analyze trends
   - Monitor integration status

2. Device Management:
   - Discover all devices in your system
   - Find devices by manufacturer or model
   - Check device firmware versions

3. Automation Development:
   - List available entities for automation triggers
   - Test entity state changes
   - Validate automation configurations

4. Data Analysis:
   - Export entity history for analysis
   - Track user activity
   - Monitor integration performance

5. System Administration:
   - Audit user accounts
   - Review integration configurations
   - Manage entity states
""")
    
    print("\n" + "=" * 60)
    print("For more information, visit:")
    print("https://github.com/johnschieferleuhlenbrock/cautious-parakeet")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
