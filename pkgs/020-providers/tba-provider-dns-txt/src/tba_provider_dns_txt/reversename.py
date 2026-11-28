"""Compatibility import for tba_primitives_dns_name.reversename."""

import sys

from tba_primitives_dns_name import reversename as _implementation

sys.modules[__name__] = _implementation
