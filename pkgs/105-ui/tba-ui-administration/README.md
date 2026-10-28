# tba_auth Admin UIX

Adapted from source repo path `authnz_ctrl_plane/admin_client` on 2026-05-05.

This app is a first-class `tba_auth` admin UIX workspace. The copied source is adapted to the `tba_auth` SSOT registry and generated OpenRPC admin/control-plane contract. The OpenRPC document and runtime `/rpc` surface are authoritative; source control-plane assumptions are not.

Runtime configuration:

- `VITE_TBA_AUTH_ADMIN_RPC_URL`, default `/rpc`
- `VITE_TBA_AUTH_ADMIN_OPENRPC_URL`, default `/openrpc.json`

No admin API key is embedded into built assets. Local development may provide a temporary runtime value through `sessionStorage` or `localStorage` under `tba_auth_admin_api_key`.
