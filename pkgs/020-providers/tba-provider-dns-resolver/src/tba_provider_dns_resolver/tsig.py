"""Compatibility import for the DNS codec TSIG implementation."""

import sys

from tba_codec_dns import tsig as _implementation

sys.modules[__name__] = _implementation
