import { describe, expect, it, vi } from "vitest";

import { BaseAdapter } from "./BaseAdapter";
import type { OidcConfig, User } from "../../types";

class TestAdapter extends BaseAdapter {
  async authorize(): Promise<void> {
    this.performRedirect("https://auth.example.com/authorize");
  }

  async handleCallback(): Promise<User> {
    throw new Error("not implemented");
  }
}

const config: OidcConfig = {
  authority: "https://auth.example.com",
  clientId: "client-1",
  redirectUri: "https://app.example.com/callback",
};

describe("BaseAdapter", () => {
  it("T1 uses same-window navigation for deterministic OIDC login", async () => {
    const assign = vi.fn();
    const open = vi.fn();
    vi.stubGlobal("window", {
      location: {
        assign,
        href: "https://app.example.com/#/login",
      },
      open,
    });

    await new TestAdapter(config).authorize();

    expect(assign).toHaveBeenCalledWith("https://auth.example.com/authorize");
    expect(open).not.toHaveBeenCalled();
  });
});
