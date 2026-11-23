"""Compatibility import for tba_codec_dns.node."""

import sys

from tba_codec_dns import node as _implementation

sys.modules[__name__] = _implementation
