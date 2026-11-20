"""Compatibility import for tba_codec_dns.svcb."""

import sys

from tba_codec_dns import svcb as _implementation

sys.modules[__name__] = _implementation
