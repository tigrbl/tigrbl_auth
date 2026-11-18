from .validation import OPTIONAL_BINDING_CLAIMS, REQUIRED_WPT_CLAIMS, validate_wpt
from .versions import CURRENT_VERSION, VERSION_HISTORY, WptVersion

__all__ = [
    "CURRENT_VERSION",
    "OPTIONAL_BINDING_CLAIMS",
    "REQUIRED_WPT_CLAIMS",
    "VERSION_HISTORY",
    "WptVersion",
    "validate_wpt",
]

from .verification import verify_wpt, authenticate_wpt_request
from .presentation import present_wit
from .verifier import WptProofVerifier
from .issuance import WptProofIssuer, issue_wpt
from .verification import _target_audience as normalize_wpt_audience

__all__ += ["verify_wpt", "authenticate_wpt_request", "present_wit", "WptProofVerifier"]
__all__ += ["WptProofIssuer", "issue_wpt", "normalize_wpt_audience"]
