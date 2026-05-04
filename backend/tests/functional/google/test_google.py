"""Rotas /google/* (OAuth e status)."""
from unittest.mock import patch, MagicMock

import pytest


def test_google_status_unauthorized(client):
    r = client.get("/google/status")
    assert r.status_code == 401


def test_google_status_not_connected(client, admin_token_headers):
    r = client.get("/google/status", headers=admin_token_headers)
    assert r.status_code == 200
    assert r.json() == {"connected": False}


def test_google_connect_unauthorized(client):
    r = client.get("/google/connect")
    assert r.status_code == 401


def test_google_connect_depends_on_env(client, admin_token_headers):
    """Com credenciais no .env retorna JSON com auth_url; sem credenciais retorna 500."""
    r = client.get("/google/connect", headers=admin_token_headers)
    assert r.status_code in (200, 500)
    if r.status_code == 200:
        assert "auth_url" in r.json()
    else:
        assert "configured" in (r.json().get("detail") or "").lower()


@patch("app.routers.google.Flow")
def test_google_connect_returns_auth_url(mock_flow_cls, client, admin_token_headers, monkeypatch):
    """Ensure OAuth config exists: get_settings is lru_cached and Depends() keeps the real callable, so env + cache_clear is reliable in CI."""
    from app.config import get_settings

    monkeypatch.setenv("GOOGLE_CLIENT_ID", "test-client-id.apps.googleusercontent.com")
    monkeypatch.setenv("GOOGLE_CLIENT_SECRET", "test-secret")
    monkeypatch.setenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/google/callback")
    get_settings.cache_clear()

    flow = MagicMock()
    flow.authorization_url.return_value = ("https://accounts.google.com/o/oauth2/auth?test=1", "state-xyz")
    mock_flow_cls.from_client_config.return_value = flow

    r = client.get("/google/connect", headers=admin_token_headers)
    assert r.status_code == 200
    data = r.json()
    assert "auth_url" in data
    assert "accounts.google.com" in data["auth_url"]


def test_google_callback_invalid_session(client):
    r = client.get("/google/callback?state=x&code=y")
    assert r.status_code == 400
