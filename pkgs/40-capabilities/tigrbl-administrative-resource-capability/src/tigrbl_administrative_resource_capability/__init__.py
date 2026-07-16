"""Generic administrative-resource capability."""

from .capability import *
from .capability import __all__ as _capability_exports
from .models import *
from .models import __all__ as _model_exports

__all__ = [*_capability_exports, *_model_exports]
