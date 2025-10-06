"""Test the HA data access services."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timezone


@pytest.fixture
def mock_hass():
    """Create a mock Home Assistant instance."""
    hass = MagicMock()

    # Mock auth
    hass.auth = MagicMock()
    mock_user = MagicMock()
    mock_user.id = "test_user_id"
    mock_user.name = "Test User"
    mock_user.is_owner = True
    mock_user.is_active = True
    mock_user.system_generated = False
    mock_user.local_only = False
    mock_user.groups = []

    hass.auth.async_get_users = MagicMock(return_value=[mock_user])
    hass.auth.async_get_user = AsyncMock(return_value=mock_user)

    # Mock config entries
    hass.config_entries = MagicMock()
    mock_entry = MagicMock()
    mock_entry.entry_id = "test_entry_id"
    mock_entry.domain = "test_domain"
    mock_entry.title = "Test Integration"
    mock_entry.state = MagicMock()
    mock_entry.state.name = "loaded"
    mock_entry.source = "user"
    mock_entry.data = {}
    mock_entry.options = {}

    hass.config_entries.async_entries = MagicMock(return_value=[mock_entry])
    hass.config_entries.async_get_entry = MagicMock(return_value=mock_entry)

    # Mock states
    hass.states = MagicMock()
    mock_state = MagicMock()
    mock_state.entity_id = "light.test"
    mock_state.state = "on"
    mock_state.attributes = {"brightness": 255}
    mock_state.last_changed = datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    mock_state.last_updated = datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

    hass.states.get = MagicMock(return_value=mock_state)
    hass.states.async_set = AsyncMock()

    return hass


def test_mock_hass_fixture(mock_hass):
    """Test that the mock hass fixture works correctly."""
    assert mock_hass is not None
    assert mock_hass.auth is not None
    assert len(mock_hass.auth.async_get_users()) == 1
    assert mock_hass.auth.async_get_users()[0].name == "Test User"


@pytest.mark.asyncio
async def test_list_users(mock_hass):
    """Test listing users."""
    users = []
    for user in mock_hass.auth.async_get_users():
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

    assert len(users) == 1
    assert users[0]["id"] == "test_user_id"
    assert users[0]["name"] == "Test User"
    assert users[0]["is_owner"] is True


@pytest.mark.asyncio
async def test_get_user(mock_hass):
    """Test getting a specific user."""
    user = await mock_hass.auth.async_get_user("test_user_id")

    assert user is not None
    assert user.id == "test_user_id"
    assert user.name == "Test User"


@pytest.mark.asyncio
async def test_list_integrations(mock_hass):
    """Test listing integrations."""
    entries = []
    for entry in mock_hass.config_entries.async_entries():
        entries.append(
            {
                "entry_id": entry.entry_id,
                "domain": entry.domain,
                "title": entry.title,
                "state": entry.state.name,
                "source": entry.source,
            }
        )

    assert len(entries) == 1
    assert entries[0]["entry_id"] == "test_entry_id"
    assert entries[0]["domain"] == "test_domain"
    assert entries[0]["title"] == "Test Integration"


@pytest.mark.asyncio
async def test_get_integration(mock_hass):
    """Test getting a specific integration."""
    entry = mock_hass.config_entries.async_get_entry("test_entry_id")

    assert entry is not None
    assert entry.entry_id == "test_entry_id"
    assert entry.domain == "test_domain"


@pytest.mark.asyncio
async def test_get_entity_state(mock_hass):
    """Test getting entity state."""
    state = mock_hass.states.get("light.test")

    assert state is not None
    assert state.entity_id == "light.test"
    assert state.state == "on"
    assert state.attributes["brightness"] == 255


@pytest.mark.asyncio
async def test_update_entity_state(mock_hass):
    """Test updating entity state."""
    entity_id = "light.test"
    new_state = "off"
    attributes = {"brightness": 0}

    mock_hass.states.async_set(entity_id, new_state, attributes)

    mock_hass.states.async_set.assert_called_once_with(entity_id, new_state, attributes)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
