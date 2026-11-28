"""Compatibility import for tba_provider_dns_resolver.async_transport."""

import sys

from tba_provider_dns_resolver import async_transport as _implementation

sys.modules[__name__] = _implementation
