export interface HttpTransportOptions {
  baseUrl: string;
  fetcher?: typeof fetch;
  headers?: Record<string, string>;
}

export interface HttpRequestOptions<TBody = unknown> {
  body?: TBody;
  headers?: Record<string, string>;
  method?: "DELETE" | "GET" | "PATCH" | "POST" | "PUT";
  signal?: AbortSignal;
}

export interface SurfaceBoundary {
  backendApp: string;
  allowedPathPrefixes: string[];
  forbiddenPathPrefixes: string[];
}

