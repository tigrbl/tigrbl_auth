"""Deprecated compatibility imports for canonical SPIFFE contracts."""

from __future__ import annotations

from .workloads import SpiffeId, Svid, SvidFormat, SvidProviderPort

WorkloadIdentityProvider = SvidProviderPort


__all__ = ["SpiffeId", "Svid", "SvidFormat", "WorkloadIdentityProvider"]
