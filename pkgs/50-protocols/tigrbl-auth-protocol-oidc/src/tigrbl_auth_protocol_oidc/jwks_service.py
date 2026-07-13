"""OIDC JWKS publication helpers for the release path."""

from __future__ import annotations


async def build_jwks_document() -> dict:
    from tigrbl_identity_jose.jwks_publication import build_combined_jwks_document

    return await build_combined_jwks_document()


__all__ = ["build_jwks_document"]
