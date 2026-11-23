"""Compatibility import for tba_codec_dns.wire."""

import sys

from tba_codec_dns import wire as _implementation

sys.modules[__name__] = _implementation
