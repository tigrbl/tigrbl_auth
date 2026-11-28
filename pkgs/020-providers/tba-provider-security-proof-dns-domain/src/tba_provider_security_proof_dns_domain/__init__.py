"""DNS ownership verification against an explicitly configured HTTPS resolver."""

import json
from urllib.parse import urlsplit

import httpx


class DomainProofUnavailable(Exception):
    """The configured DNS resolver did not return usable evidence."""


class DnsDomainOwnershipVerifier:
    def __init__(self, resolver_url: str, *, transport: httpx.BaseTransport | None = None):
        url = urlsplit(resolver_url)
        if url.scheme != "https" or not url.hostname or url.username or url.password or url.query or url.fragment:
            raise ValueError("Configure a trusted HTTPS DNS JSON resolver URL.")
        self._url = resolver_url
        self._transport = transport

    def verify(self, *, hostname: str, record_name: str, proof: str, cname_target: str) -> bool:
        with httpx.Client(timeout=4, transport=self._transport, trust_env=False) as client:
            txt = self._answers(client, record_name, "TXT", 16)
            if json.dumps(proof, ensure_ascii=True) not in txt:
                return False
            cname = self._answers(client, hostname, "CNAME", 5)
            return [item.rstrip(".").lower() for item in cname] == [cname_target.rstrip(".").lower()]

    def _answers(self, client: httpx.Client, owner: str, record_type: str, code: int) -> list[str]:
        try:
            reply = client.get(self._url, params={"name": owner, "type": record_type},
                               headers={"Accept": "application/dns-json"})
            reply.raise_for_status()
            result = reply.json()
            status = result["Status"]
            if status == 3:
                return []
            if status != 0 or result.get("TC", False):
                raise DomainProofUnavailable("DNS ownership evidence is unavailable.")
            return [row["data"] for row in result.get("Answer", [])
                    if row["type"] == code and row["name"].rstrip(".").lower() == owner.rstrip(".").lower()
                    and isinstance(row["data"], str)]
        except (httpx.HTTPError, KeyError, ValueError, TypeError, AttributeError) as failure:
            raise DomainProofUnavailable("DNS ownership evidence is unavailable.") from failure


__all__ = ["DnsDomainOwnershipVerifier", "DomainProofUnavailable"]
