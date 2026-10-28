/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_TBA_AUTH_PUBLIC_BASE_URL?: string;
  readonly VITE_TBA_AUTH_POST_LOGIN_REDIRECT?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
