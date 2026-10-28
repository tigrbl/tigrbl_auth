"""OAuth2 standards package.

This package intentionally avoids eager star-imports so that governance,
contract-generation, and profile-resolution tooling can import individual
modules (for example RFC 9700 runtime policy helpers) without initializing the
full runtime stack.
"""

__all__: list[str] = []
