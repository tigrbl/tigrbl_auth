import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { AuthShell } from "../layout/AuthShell";
import { Card } from "./Card";
import { Checkbox } from "./Checkbox";
import { FormError, FormField, ValidationMessage } from "./FormField";
import { SocialButton } from "./SocialButton";
import { SubmitButton } from "./SubmitButton";

describe("public-style UIX primitives", () => {
  it("renders the centered auth shell with brand and product copy", () => {
    const html = renderToStaticMarkup(
      <AuthShell backendApp="test-backend" subtitle="Identity product copy" title="Sign in">
        <Card>Form</Card>
      </AuthShell>
    );

    expect(html).toContain("tigrbl-auth-shell");
    expect(html).toContain("Tigrbl Auth");
    expect(html).toContain("test-backend");
    expect(html).toContain("Identity product copy");
  });

  it("renders shared form and action primitives with validation classes", () => {
    const html = renderToStaticMarkup(
      <Card tone="hero">
        <FormError>Invalid session</FormError>
        <FormField error="Required" label="Email" value="" readOnly />
        <ValidationMessage>Bad value</ValidationMessage>
        <Checkbox checked readOnly label="Remember this device" />
        <SubmitButton loading loadingLabel="Signing in">Sign in</SubmitButton>
        <SocialButton label="Example" />
      </Card>
    );

    expect(html).toContain("tigrbl-card-hero");
    expect(html).toContain("tigrbl-form-error");
    expect(html).toContain("aria-invalid=\"true\"");
    expect(html).toContain("tigrbl-checkbox");
    expect(html).toContain("Signing in");
    expect(html).toContain("Continue with Example");
  });
});
