"""Test fixtures and conformance helpers for the TBA identity package suite."""

from __future__ import annotations

from warnings import warn as _warn


from .cross_cutting import (
    AuthorizationCode,
    FakeIdentityProvider,
    FakeRelyingParty,
    FakeResourceServer,
    MatrixCellStatus,
    PackageMatrixCell,
    PackageMatrixHarness,
    SeededClient,
    SeededTenant,
    SeededUser,
    TestkitError,
    TestkitProviderRuntimeProfile,
    TestkitSeedSet,
    TokenResponse,
    build_fake_flow,
    cross_language_vectors,
    default_seed_set,
    pkce_s256,
    provider_runtime_profile,
)

_warn(
    "tba-testkit-identity is deprecated. Install tba-tests-identity and import "
    "tba_tests_identity instead.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = [
    "AuthorizationCode",
    "FakeIdentityProvider",
    "FakeRelyingParty",
    "FakeResourceServer",
    "MatrixCellStatus",
    "PackageMatrixCell",
    "PackageMatrixHarness",
    "SeededClient",
    "SeededTenant",
    "SeededUser",
    "TestkitError",
    "TestkitProviderRuntimeProfile",
    "TestkitSeedSet",
    "TokenResponse",
    "build_fake_flow",
    "cross_language_vectors",
    "default_seed_set",
    "pkce_s256",
    "provider_runtime_profile",
]
