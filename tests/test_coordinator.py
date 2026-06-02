from __future__ import annotations

from unittest.mock import AsyncMock, Mock

from homeassistant.const import CONF_ACCESS_TOKEN
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import UpdateFailed
import pytest

from custom_components.willow.coordinator import WillowDataUpdateCoordinator
from custom_components.willow.exceptions import WillowAuthError


@pytest.mark.asyncio
async def test_update_data_filters_devices_without_sensor_id(hass) -> None:
    oauth_session = Mock()
    oauth_session.token = {CONF_ACCESS_TOKEN: "new-token"}
    oauth_session.async_ensure_token_valid = AsyncMock()
    client = Mock()
    client.update_token = Mock()
    client.get_profile = AsyncMock(return_value={"id": 1, "username": "willow"})
    client.get_devices = AsyncMock(
        return_value=[
            {"sensor_id": "sensor-1", "user_plant": {"name": "Fern"}},
            {"sensor_id": ""},
            "not-a-device",
        ]
    )
    coordinator = WillowDataUpdateCoordinator(hass, Mock(), client, oauth_session)

    data = await coordinator._async_update_data()

    oauth_session.async_ensure_token_valid.assert_awaited_once()
    client.update_token.assert_called_once_with("new-token")
    assert coordinator.profile == {"id": 1, "username": "willow"}
    assert data == {"sensor-1": {"sensor_id": "sensor-1", "user_plant": {"name": "Fern"}}}


@pytest.mark.asyncio
async def test_update_data_raises_config_entry_auth_failed(hass) -> None:
    oauth_session = Mock()
    oauth_session.token = {CONF_ACCESS_TOKEN: "token"}
    oauth_session.async_ensure_token_valid = AsyncMock()
    client = Mock()
    client.update_token = Mock()
    client.get_profile = AsyncMock(side_effect=WillowAuthError)
    coordinator = WillowDataUpdateCoordinator(hass, Mock(), client, oauth_session)

    with pytest.raises(ConfigEntryAuthFailed):
        await coordinator._async_update_data()


@pytest.mark.asyncio
async def test_update_data_wraps_unknown_errors(hass) -> None:
    oauth_session = Mock()
    oauth_session.async_ensure_token_valid = AsyncMock(side_effect=RuntimeError("boom"))
    client = Mock()
    coordinator = WillowDataUpdateCoordinator(hass, Mock(), client, oauth_session)

    with pytest.raises(UpdateFailed, match="Unable to fetch Willow data: boom"):
        await coordinator._async_update_data()
