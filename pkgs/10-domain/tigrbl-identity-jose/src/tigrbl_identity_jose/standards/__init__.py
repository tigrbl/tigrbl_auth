"""JOSE standards package.

This package intentionally avoids eager star-imports so focused helpers such as
RFC 7516 JWE policy or RFC 7519 JWT helpers can be imported in dependency-light
contract, governance, and evidence workflows without initializing the full
runtime stack.
"""

__all__: list[str] = []
