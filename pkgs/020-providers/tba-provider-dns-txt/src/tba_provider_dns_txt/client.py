"""Compatibility import for tba_provider_dns_resolver.client."""

import sys

from tba_provider_dns_resolver import client as _implementation

sys.modules[__name__] = _implementation
