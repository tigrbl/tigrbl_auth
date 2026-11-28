"""Compatibility import for tba_provider_dns_resolver.tsig."""

import sys

from tba_provider_dns_resolver import tsig as _implementation

sys.modules[__name__] = _implementation
