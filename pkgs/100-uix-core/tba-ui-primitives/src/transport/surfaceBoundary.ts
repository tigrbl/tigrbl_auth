import type { SurfaceBoundary } from "./types";

function matchesPrefix(path: string, prefix: string): boolean {
  return path === prefix || path.startsWith(`${prefix}/`);
}

export function assertSurfacePath(path: string, boundary: SurfaceBoundary): void {
  if (!path.startsWith("/")) {
    throw new Error(`Transport paths must be absolute: ${path}`);
  }
  if (boundary.forbiddenPathPrefixes.some((prefix) => matchesPrefix(path, prefix))) {
    throw new Error(`Path is outside ${boundary.backendApp}: ${path}`);
  }
  if (!boundary.allowedPathPrefixes.some((prefix) => matchesPrefix(path, prefix))) {
    throw new Error(`Path is not part of ${boundary.backendApp}: ${path}`);
  }
}

export function createSurfaceUrl(baseUrl: string, path: string, boundary: SurfaceBoundary): URL {
  assertSurfacePath(path, boundary);
  return new URL(path, `${baseUrl.replace(/\/+$/, "")}/`);
}

