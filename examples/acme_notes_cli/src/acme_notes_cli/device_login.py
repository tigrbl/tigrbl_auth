from __future__ import annotations

import asyncio
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx


DEVICE_CODE_GRANT_TYPE = "urn:ietf:params:oauth:grant-type:device_code"


class DeviceLoginError(RuntimeError):
    """Raised when the device login flow cannot complete."""


@dataclass(slots=True)
class DeviceAuthorizationPayload:
    device_code: str
    user_code: str
    verification_uri: str
    verification_uri_complete: str
    expires_in: int
    interval: int


class DeviceLoginClient:
    """Minimal client-side wrapper for RFC 8628 device authorization."""

    def __init__(
        self,
        *,
        issuer: str,
        client_id: str,
        scope: str = "openid profile email",
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self.issuer = issuer.rstrip("/")
        self.client_id = client_id
        self.scope = scope
        self._http_client = http_client

    async def discover(self) -> dict[str, Any]:
        client = self._http_client or httpx.AsyncClient()
        close_client = self._http_client is None
        try:
            response = await client.get(f"{self.issuer}/.well-known/oauth-authorization-server")
            response.raise_for_status()
            return response.json()
        finally:
            if close_client:
                await client.aclose()

    def _resolve_device_authorization_endpoints(self, metadata: dict[str, Any]) -> list[str]:
        endpoints: list[str] = []
        endpoint = str(metadata.get("device_authorization_endpoint") or "").strip()
        if endpoint:
            endpoints.append(endpoint)
        for candidate in (
            f"{self.issuer}/device_authorization",
            f"{self.issuer}/device_codes/device_authorization",
        ):
            if candidate not in endpoints:
                endpoints.append(candidate)
        return endpoints

    def _resolve_token_endpoint(self, metadata: dict[str, Any]) -> str:
        endpoint = str(metadata.get("token_endpoint") or "").strip()
        if endpoint:
            return endpoint
        return f"{self.issuer}/token"

    async def start(self) -> DeviceAuthorizationPayload:
        metadata = await self.discover()
        endpoints = self._resolve_device_authorization_endpoints(metadata)
        client = self._http_client or httpx.AsyncClient()
        close_client = self._http_client is None
        try:
            last_response: httpx.Response | None = None
            for endpoint in endpoints:
                response = await client.post(
                    str(endpoint),
                    data={"client_id": self.client_id, "scope": self.scope},
                )
                if response.status_code == 404:
                    last_response = response
                    continue
                response.raise_for_status()
                return DeviceAuthorizationPayload(**response.json())
            if last_response is not None:
                last_response.raise_for_status()
            raise DeviceLoginError("device authorization endpoint unavailable")
        finally:
            if close_client:
                await client.aclose()

    async def poll_for_tokens(
        self,
        device_code: str,
        *,
        interval: int,
        expires_in: int,
    ) -> dict[str, Any]:
        metadata = await self.discover()
        token_endpoint = self._resolve_token_endpoint(metadata)
        client = self._http_client or httpx.AsyncClient()
        close_client = self._http_client is None
        started = time.monotonic()
        poll_interval = max(int(interval), 1)
        try:
            while True:
                if time.monotonic() - started > int(expires_in):
                    raise DeviceLoginError("device authorization expired before approval")
                response = await client.post(
                    str(token_endpoint),
                    data={
                        "grant_type": DEVICE_CODE_GRANT_TYPE,
                        "device_code": device_code,
                        "client_id": self.client_id,
                    },
                )
                payload = response.json()
                if response.status_code == 200:
                    return payload
                error = payload.get("error")
                if error == "authorization_pending":
                    await asyncio.sleep(poll_interval)
                    continue
                if error == "slow_down":
                    poll_interval += 5
                    await asyncio.sleep(poll_interval)
                    continue
                raise DeviceLoginError(f"device login failed: {error or 'unknown_error'}")
        finally:
            if close_client:
                await client.aclose()

    async def login(self) -> tuple[DeviceAuthorizationPayload, dict[str, Any]]:
        device = await self.start()
        tokens = await self.poll_for_tokens(
            device.device_code,
            interval=device.interval,
            expires_in=device.expires_in,
        )
        return device, tokens


def persist_tokens(path: Path, tokens: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(tokens, indent=2), encoding="utf-8")
