"""Compatibility import for tba_primitives_dns_name.name."""

import sys

from tba_primitives_dns_name import name as _implementation

sys.modules[__name__] = _implementation
