"""Compatibility import for tba_provider_dns_resolver.transport."""

import sys

from tba_provider_dns_resolver import transport as _implementation

sys.modules[__name__] = _implementation
