"""Canonical identity and authorization contract types."""

from __future__ import annotations

from .models import *
from .planes import *
from .authentication import *
from .authenticators import *
from .authority import *
from .applications import *
from .credentials import *
from .delegation import *
from .federation import *
from .principals import *
from .principal_authentication import *
from .protocols import *
from .oauth import *
from .oidc import *
from .rp import *
from .resource_server import *
from .resource_validation_metadata import *
from .tokens import *
from .admin import *
from .admin_services import *
from .adaptive_access import *
from .assurance import *
from .authorization_scopes import *
from .claims import *
from .capabilities import *
from .subject_identifiers import *
from .shared_secrets import *
from .credential_artifacts import *
from .attestation import *
from .workload_identity import *
from .decentralized import *
from .policy_interop import *
from .correctness import *
from .admin_resources import *
from .governance import *
from .gnap import *
from .invariants import *
from .jose import *
from .liveness import *
from .replay import *
from .residency import *
from .topology import *

__all__ = [name for name in globals() if not name.startswith("_")]

# Transitional migration compatibility shims.
# These legacy package-level imports are kept as a narrow deprecation bridge
# while downstream consumers migrate to canonical contract package names.
try:  # pragma: no cover - exercised via consumer migration checks
    from tigrbl_administration_contracts import *  # noqa: F401,F403
    from tigrbl_authorization_contracts import *  # noqa: F401,F403
    from tigrbl_audit_contracts import *  # noqa: F401,F403
    from tigrbl_delegation_contracts import *  # noqa: F401,F403
    from tigrbl_governance_contracts import *  # noqa: F401,F403
except ModuleNotFoundError:
    # Canonical contracts are optional during rollout; keep the legacy package
    # importable even when only the legacy monolith is installed.
    pass
