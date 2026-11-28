"""Compatibility import for tba_codec_dns.record_formats."""

import sys

from tba_codec_dns import record_formats as _implementation

sys.modules[__name__] = _implementation
