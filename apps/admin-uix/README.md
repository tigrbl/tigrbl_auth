# tigrbl_auth Admin UIX

Adapted from source repo path `authnz_ctrl_plane/admin_client` on 2026-05-05.

This app is a first-class `tigrbl_auth` admin UIX workspace. The copied source is adapted to the `tigrbl_auth` SSOT registry and generated OpenRPC admin/control-plane contract. The OpenRPC document and runtime `/rpc` surface are authoritative; source control-plane assumptions are not.

Runtime configuration:

- `VITE_TIGRBL_AUTH_ADMIN_RPC_URL`, default `/rpc`
- `VITE_TIGRBL_AUTH_DEV_ADMIN_API_KEY`, optional local-development credential only

No admin API key is embedded by default.
