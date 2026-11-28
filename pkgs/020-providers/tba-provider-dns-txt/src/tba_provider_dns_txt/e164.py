"""Compatibility import for tba_primitives_dns_name.e164."""

import sys

from tba_primitives_dns_name import e164 as _implementation

sys.modules[__name__] = _implementation
