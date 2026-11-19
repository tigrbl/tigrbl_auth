from warnings import warn as _warn


from .vectors import ArtifactVector, VECTORS

_warn(
    "tba-testkit-workload-credential-conformance is deprecated. "
    "Install tba-tests-workload-credential-conformance and import "
    "tba_tests_workload_credential_conformance instead.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ["ArtifactVector", "VECTORS"]
