import { describe, expect, it } from "vitest";
import { BACKEND_APP, PRODUCT_SURFACE } from "../defaults";

describe("my account surface metadata", () => {
  it("names the My Account product API and UIX package", () => {
    expect(BACKEND_APP).toBe("tba-app-backend-my-account");
    expect(PRODUCT_SURFACE).toBe("@tba/ui-my-account");
  });
});
