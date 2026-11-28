"""Compatibility import for tba_codec_dns.rdataset."""

import sys

from tba_codec_dns import rdataset as _implementation

sys.modules[__name__] = _implementation
