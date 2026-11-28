"""Compatibility import for tba_provider_dns_resolver.system_resolver."""

import sys

from tba_provider_dns_resolver import system_resolver as _implementation

sys.modules[__name__] = _implementation
