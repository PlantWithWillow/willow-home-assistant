from __future__ import annotations

from unittest.mock import Mock

from aiohttp import ClientResponseError, RequestInfo
import pytest

from custom_components.willow.client import WillowClient
from custom_components.willow.const import GET_DEVICES_URL, GET_PROFILE_URL
from custom_components.willow.exceptions import WillowAuthError


class MockResponse:
    def __init__(self, data: object) -> None:
        self._data = data

    async def __aenter__(self) -> MockResponse:
        return self

    async def __aexit__(self, *args: object) -> None:
        return None

    async def json(self) -> object:
        return self._data


class MockErrorResponse:
    def __init__(self, error: Exception) -> None:
        self._error = error

    async def __aenter__(self) -> MockErrorResponse:
        raise self._error

    async def __aexit__(self, *args: object) -> None:
        return None


@pytest.mark.asyncio
async def test_get_profile_uses_bearer_token() -> None:
    session = Mock()
    session.request.return_value = MockResponse({"id": 1, "username": "willow"})
    client = WillowClient(session, "token-1")

    assert await client.get_profile() == {"id": 1, "username": "willow"}
    session.request.assert_called_once_with(
        "GET",
        GET_PROFILE_URL,
        headers={"Authorization": "Bearer token-1"},
        raise_for_status=True,
    )


@pytest.mark.asyncio
async def test_get_devices_uses_updated_token() -> None:
    session = Mock()
    session.request.return_value = MockResponse([])
    client = WillowClient(session, "token-1")

    client.update_token("token-2")

    assert await client.get_devices() == []
    session.request.assert_called_once_with(
        "GET",
        GET_DEVICES_URL,
        headers={"Authorization": "Bearer token-2"},
        raise_for_status=True,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("status", [401, 403])
async def test_auth_errors_raise_willow_auth_error(status: int) -> None:
    request_info = Mock(spec=RequestInfo)
    session = Mock()
    session.request.return_value = MockErrorResponse(
        ClientResponseError(
            request_info=request_info,
            history=(),
            status=status,
        )
    )
    client = WillowClient(session, "token")

    with pytest.raises(WillowAuthError):
        await client.get_profile()
