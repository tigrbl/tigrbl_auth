"""Compatibility import for tba_codec_dns.rrset."""

import sys

from tba_codec_dns import rrset as _implementation

sys.modules[__name__] = _implementation
