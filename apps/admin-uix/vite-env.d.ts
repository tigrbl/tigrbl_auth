/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_TIGRBL_AUTH_ADMIN_RPC_URL?: string;
  readonly VITE_TIGRBL_AUTH_DEV_ADMIN_API_KEY?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
