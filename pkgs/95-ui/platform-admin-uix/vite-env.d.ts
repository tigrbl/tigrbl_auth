/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_TIGRBL_AUTH_PLATFORM_ADMIN_API_BASE_URL?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
