import { readFileSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, it } from "vitest";

const appSource = (): string => readFileSync(join(process.cwd(), "App.tsx"), "utf8");
const baseAdapterSource = (): string =>
  readFileSync(join(process.cwd(), "services", "oidc", "BaseAdapter.ts"), "utf8");

describe("public UIX routing boundary", () => {
  it("T2 keeps route rendering free of location hash mutation", () => {
    const source = appSource();
    const renderContent = source.slice(source.indexOf("const renderContent = () => {"));

    expect(renderContent).not.toContain("window.location.hash =");
  });

  it("T1 initializes route state from callback-aware routing policy", () => {
    const source = appSource();

    expect(source).toContain("resolveInitialPublicHash(");
    expect(source).toContain("resolvePublicRedirect({");
    expect(source).toContain("shouldNormalizeCallbackLocation(");
  });

  it("T2 keeps default OIDC login on deterministic same-window navigation", () => {
    const source = baseAdapterSource();
    const performRedirect = source.slice(source.indexOf("protected performRedirect"));

    expect(performRedirect).toContain("window.location.assign(url)");
    expect(performRedirect).not.toContain("openAuthPopup(");
    expect(performRedirect).not.toContain("window.open(");
  });
});
