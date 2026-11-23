"""Compatibility import for tba_codec_dns.edns."""

import sys

from tba_codec_dns import edns as _implementation

sys.modules[__name__] = _implementation
