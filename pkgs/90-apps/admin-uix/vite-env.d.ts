/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_TIGRBL_AUTH_ADMIN_RPC_URL?: string;
  readonly VITE_TIGRBL_AUTH_ADMIN_OPENRPC_URL?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
