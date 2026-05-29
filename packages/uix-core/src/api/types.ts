export interface ApiClientOptions {
  baseUrl: string;
  fetcher?: typeof fetch;
  headers?: Record<string, string>;
}

export interface ApiRequestOptions<TBody = unknown> {
  body?: TBody;
  headers?: Record<string, string>;
  method?: "DELETE" | "GET" | "PATCH" | "POST" | "PUT";
  signal?: AbortSignal;
}

export interface SurfaceBoundary {
  productApi: string;
  allowedPathPrefixes: string[];
  forbiddenPathPrefixes: string[];
}

