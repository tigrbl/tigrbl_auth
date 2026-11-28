"""Compatibility import for tba_primitives_dns_name.names."""

import sys

from tba_primitives_dns_name import names as _implementation

sys.modules[__name__] = _implementation
