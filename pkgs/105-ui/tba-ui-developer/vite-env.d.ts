/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_TBA_AUTH_DEVELOPER_BACKEND_APP_BASE_URL?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
