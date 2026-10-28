export function encodeCursorParams(cursor?: string | null, limit?: number): URLSearchParams {
  const params = new URLSearchParams();
  if (cursor) params.set("cursor", cursor);
  if (limit !== undefined) params.set("limit", String(limit));
  return params;
}

