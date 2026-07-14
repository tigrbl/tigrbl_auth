# tigrbl-auth-api-oauth-device-authorization

HTTP carrier binding for the RFC 8628 device authorization endpoint.

This package owns POST route mounting and dependency materialization. Protocol
validation, device/user-code generation, resource selection, durable records,
audit, deployment policy, and runtime observation are injected downstream.
