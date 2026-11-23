"""Compatibility import for tba_codec_dns.rdata."""

import sys

from tba_codec_dns import rdata as _implementation

sys.modules[__name__] = _implementation
