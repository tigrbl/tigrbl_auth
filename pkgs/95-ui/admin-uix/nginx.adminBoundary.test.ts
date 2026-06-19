import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

import { describe, expect, it } from 'vitest';

const here = dirname(fileURLToPath(import.meta.url));
const template = readFileSync(join(here, 'nginx.conf.template'), 'utf8');

function locationBlock(path: string): string {
  const escaped = path.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  return template.match(new RegExp(`location ${escaped} \\{[\\s\\S]*?\\n  \\}`))?.[0] ?? '';
}

describe('admin UIX nginx backend boundary', () => {
  it('proxies tenant discovery and JWKS routes to the backend', () => {
    const block = locationBlock('/tenants/');

    expect(block).toContain('proxy_pass ${TIGRBL_AUTH_BACKEND_UPSTREAM}');
    expect(block).toContain('proxy_set_header Host $host');
    expect(block).toContain('proxy_set_header X-Forwarded-Proto $scheme');
  });

  it('keeps the SPA fallback after backend proxy routes', () => {
    expect(template.indexOf('location /tenants/')).toBeGreaterThan(-1);
    expect(template.indexOf('location / {\n    try_files $uri /index.html;')).toBeGreaterThan(template.indexOf('location /tenants/'));
  });
});
