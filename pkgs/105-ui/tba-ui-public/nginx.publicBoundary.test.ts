import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

describe("public UIX nginx boundary", () => {
  it("proxies only governed public routes and blocks control-plane paths", () => {
    const config = readFileSync(resolve(process.cwd(), "nginx.conf.template"), "utf8");

    expect(config).toContain("location /admin");
    expect(config).toContain("return 404;");
    expect(config).toContain("location /rpc");
    expect(config).toContain("location = /callback");
    expect(config).toContain("#/callback$is_args$args");
    expect(config).toContain("location /.well-known/");
    expect(config).toContain("location /authorize");
    expect(config).toContain("location /login");
    expect(config).toContain("location /token");
    expect(config).toContain("location /userinfo");
    expect(config).toContain("location /logout");
    expect(config).toContain("location /register");
    expect(config).toContain("location /recovery");
    expect(config).toContain("location /verify-email");
    expect(config).toContain("location /mfa");
    expect(config).toContain("location /consent");
  });
});
