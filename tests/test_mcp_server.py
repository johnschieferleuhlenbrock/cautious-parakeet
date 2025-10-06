"""Test the MCP Server functionality."""
import sys
import tempfile
from pathlib import Path

import pytest

# Add the parent directory to the path first
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import only the mcp_server module directly
import importlib.util

spec = importlib.util.spec_from_file_location(
    "mcp_server",
    Path(__file__).parent.parent / "custom_components" / "ha_mcp_server" / "mcp_server.py"
)
mcp_server_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mcp_server_module)

MCPConfigServer = mcp_server_module.MCPConfigServer


@pytest.fixture
def temp_config_dir():
    """Create a temporary config directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def mcp_server(temp_config_dir):
    """Create an MCP server instance."""
    return MCPConfigServer(temp_config_dir)


@pytest.mark.asyncio
async def test_write_and_read_yaml(mcp_server, temp_config_dir):
    """Test writing and reading a YAML file."""
    test_config = {
        "homeassistant": {
            "name": "Test Home",
            "latitude": 51.5074,
            "longitude": -0.1278,
        }
    }
    
    # Write the config
    await mcp_server.write_config_file("test.yaml", test_config)
    
    # Read it back
    result = await mcp_server.read_config_file("test.yaml")
    
    assert result == test_config
    assert result["homeassistant"]["name"] == "Test Home"


@pytest.mark.asyncio
async def test_write_and_read_json(mcp_server, temp_config_dir):
    """Test writing and reading a JSON file."""
    test_config = {
        "setting1": "value1",
        "setting2": 42,
    }
    
    # Write the config
    await mcp_server.write_config_file("test.json", test_config)
    
    # Read it back
    result = await mcp_server.read_config_file("test.json")
    
    assert result == test_config


@pytest.mark.asyncio
async def test_list_config_files(mcp_server, temp_config_dir):
    """Test listing configuration files."""
    # Create some test files
    await mcp_server.write_config_file("config1.yaml", {"test": 1})
    await mcp_server.write_config_file("config2.json", {"test": 2})
    await mcp_server.write_config_file("config3.txt", "test content")
    
    # List files
    files = await mcp_server.list_config_files()
    
    assert "config1.yaml" in files
    assert "config2.json" in files
    assert "config3.txt" in files


@pytest.mark.asyncio
async def test_get_config_value(mcp_server, temp_config_dir):
    """Test getting a specific config value."""
    test_config = {
        "homeassistant": {
            "name": "Test Home",
            "unit_system": "metric",
        }
    }
    
    await mcp_server.write_config_file("test.yaml", test_config)
    
    # Get a nested value
    name = await mcp_server.get_config_value("test.yaml", "homeassistant.name")
    assert name == "Test Home"
    
    unit_system = await mcp_server.get_config_value("test.yaml", "homeassistant.unit_system")
    assert unit_system == "metric"


@pytest.mark.asyncio
async def test_set_config_value(mcp_server, temp_config_dir):
    """Test setting a specific config value."""
    test_config = {
        "homeassistant": {
            "name": "Old Name",
        }
    }
    
    await mcp_server.write_config_file("test.yaml", test_config)
    
    # Set a new value
    await mcp_server.set_config_value("test.yaml", "homeassistant.name", "New Name")
    
    # Verify the change
    result = await mcp_server.read_config_file("test.yaml")
    assert result["homeassistant"]["name"] == "New Name"


@pytest.mark.asyncio
async def test_set_config_value_creates_path(mcp_server, temp_config_dir):
    """Test that set_config_value creates missing keys."""
    await mcp_server.write_config_file("test.yaml", {})
    
    # Set a nested value that doesn't exist
    await mcp_server.set_config_value("test.yaml", "new.nested.value", "test")
    
    # Verify it was created
    result = await mcp_server.read_config_file("test.yaml")
    assert result["new"]["nested"]["value"] == "test"


@pytest.mark.asyncio
async def test_security_path_traversal(mcp_server, temp_config_dir):
    """Test that path traversal is blocked."""
    with pytest.raises(ValueError):
        await mcp_server.read_config_file("../etc/passwd")
    
    with pytest.raises(ValueError):
        await mcp_server.write_config_file("../etc/passwd", "malicious content")


@pytest.mark.asyncio
async def test_file_not_found(mcp_server, temp_config_dir):
    """Test handling of non-existent files."""
    with pytest.raises(FileNotFoundError):
        await mcp_server.read_config_file("nonexistent.yaml")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
