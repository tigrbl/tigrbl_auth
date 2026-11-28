import { describe, expect, it } from "vitest";

import { decodeBase64Url, encodeBase64Url } from "./base64url";

describe("WebAuthn base64url transport", () => {
  it("round trips arbitrary credential bytes without padding", () => {
    const value = Uint8Array.from([0, 1, 2, 127, 128, 255]).buffer;
    const encoded = encodeBase64Url(value);
    expect(encoded).not.toContain("=");
    expect(Array.from(new Uint8Array(decodeBase64Url(encoded)))).toEqual([0, 1, 2, 127, 128, 255]);
  });
});
