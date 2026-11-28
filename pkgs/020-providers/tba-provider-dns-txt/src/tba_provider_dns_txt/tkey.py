"""Compatibility import for tba_codec_dns.tkey."""

import sys

from tba_codec_dns import tkey as _implementation

sys.modules[__name__] = _implementation
