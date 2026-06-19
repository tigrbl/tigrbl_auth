import { ApiError } from "./errors";
import type { ApiClientOptions, ApiRequestOptions, SurfaceBoundary } from "./types";
import { createSurfaceUrl } from "./surfaceBoundary";

export class ApiClient {
  readonly baseUrl: string;
  readonly boundary?: SurfaceBoundary;
  private readonly fetcher: typeof fetch;
  private readonly headers: Record<string, string>;

  constructor(options: ApiClientOptions & { boundary?: SurfaceBoundary }) {
    this.baseUrl = options.baseUrl.replace(/\/+$/, "");
    this.boundary = options.boundary;
    this.fetcher = options.fetcher ?? globalThis.fetch.bind(globalThis);
    this.headers = options.headers ?? {};
  }

  async request<TResponse, TBody = unknown>(path: string, options: ApiRequestOptions<TBody> = {}): Promise<TResponse> {
    const url = this.boundary ? createSurfaceUrl(this.baseUrl, path, this.boundary) : new URL(path, `${this.baseUrl}/`);
    const response = await this.fetcher(url, {
      method: options.method ?? "GET",
      headers: {
        ...this.headers,
        ...(options.body === undefined ? {} : { "content-type": "application/json" }),
        ...options.headers
      },
      body: options.body === undefined ? undefined : JSON.stringify(options.body),
      signal: options.signal
    });

    const contentType = response.headers.get("content-type") ?? "";
    const payload = contentType.includes("application/json") ? await response.json() : await response.text();
    if (!response.ok) {
      throw new ApiError(`Request failed with ${response.status}`, response.status, payload);
    }
    return payload as TResponse;
  }
}

