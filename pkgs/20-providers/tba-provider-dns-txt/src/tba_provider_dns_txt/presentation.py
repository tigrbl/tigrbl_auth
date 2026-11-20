"""Compatibility import for tba_codec_dns.presentation."""

import sys

from tba_codec_dns import presentation as _implementation

sys.modules[__name__] = _implementation
