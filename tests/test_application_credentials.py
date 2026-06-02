from __future__ import annotations

from custom_components.willow.application_credentials import (
    DEFAULT_EXPIRES_IN,
    WillowOAuth2Implementation,
)


def test_normalize_token_adds_default_expiry() -> None:
    implementation = object.__new__(WillowOAuth2Implementation)
    token = {"access_token": "access-token"}

    assert implementation._normalize_token(token) == {
        "access_token": "access-token",
        "expires_in": DEFAULT_EXPIRES_IN,
    }


def test_normalize_token_preserves_existing_expiry() -> None:
    implementation = object.__new__(WillowOAuth2Implementation)
    token = {"access_token": "access-token", "expires_in": 3600}

    assert implementation._normalize_token(token) == token
