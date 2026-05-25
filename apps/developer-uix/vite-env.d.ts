/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_TIGRBL_AUTH_DEVELOPER_API_BASE_URL?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
