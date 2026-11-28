export class RelyingPartySessionClient {
  constructor(private readonly fetcher: typeof fetch = fetch) {}
  begin(baseUrl = "") { window.location.assign(`${baseUrl}/v1/rp/login`); }
  async current(baseUrl = "") { const response = await this.fetcher(`${baseUrl}/v1/rp/session`, { credentials: "include" }); if (!response.ok) throw new Error("session unavailable"); return response.json(); }
  async logout(baseUrl = "") { return this.fetcher(`${baseUrl}/v1/rp/logout`, { method: "POST", credentials: "include" }); }
}
