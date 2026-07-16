"""Deprecated compatibility imports for canonical SPIFFE contracts."""

from __future__ import annotations

from tigrbl_workload_identity_contracts import SpiffeId, Svid, SvidFormat, SvidProviderPort

WorkloadIdentityProvider = SvidProviderPort


__all__ = ["SpiffeId", "Svid", "SvidFormat", "WorkloadIdentityProvider"]
