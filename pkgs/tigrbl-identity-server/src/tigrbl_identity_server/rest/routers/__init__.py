from warnings import warn

warn(
    "tigrbl_identity_server.rest.routers is deprecated; import route surfaces "
    "from tigrbl_identity_storage.tables.* instead.",
    DeprecationWarning,
    stacklevel=2,
)

from .authorize import *
from .device_authorization import *
from .login import *
from .logout import *
from .par import *
from .register import *
from .revoke import *
from .token import *
