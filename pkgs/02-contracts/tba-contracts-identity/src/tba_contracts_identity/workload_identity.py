"""Deprecated compatibility imports for canonical SPIFFE contracts."""

from __future__ import annotations

from tba_contracts_workload_identity import SpiffeId, Svid, SvidFormat, SvidProviderPort

WorkloadIdentityProvider = SvidProviderPort


__all__ = ["SpiffeId", "Svid", "SvidFormat", "WorkloadIdentityProvider"]
