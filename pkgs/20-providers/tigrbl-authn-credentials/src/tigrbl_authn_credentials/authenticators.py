"""Removed runtime composition surface.

HTTP dependency injection, database-session ownership, and request composition
belong to ``tigrbl_identity_server.security.auth`` in layer 60. The layer-20
package retains only credential verification providers in ``backends``.
"""

__all__: list[str] = []
