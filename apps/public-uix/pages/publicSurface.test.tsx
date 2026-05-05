import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";

import { Layout } from "../components/Layout";
import { ConsentPage } from "./ConsentPage";
import { ForgotPasswordPage } from "./ForgotPasswordPage";
import { LoginPage } from "./LoginPage";
import { RegisterPage } from "./RegisterPage";

describe("public UIX surface pages", () => {
  it("renders the public shell for unauthenticated users", () => {
    const markup = renderToStaticMarkup(
      <Layout>
        <div>Public content</div>
      </Layout>,
    );

    expect(markup).toContain("Sign In");
    expect(markup).toContain("Join");
    expect(markup).toContain("Terms of Service");
  });

  it("renders authenticated shell actions including logout", () => {
    const markup = renderToStaticMarkup(
      <Layout
        user={{
          id: "user-1",
          email: "user@example.com",
          name: "User One",
          picture: "https://images.example.com/u.png",
          provider: "generic",
          isEmailVerified: true,
          mfaEnabled: false,
        }}
      >
        <div>Authenticated content</div>
      </Layout>,
    );

    expect(markup).toContain("Sign Out");
    expect(markup).toContain("User One");
  });

  it("renders login, registration, and recovery entry points", () => {
    const loginMarkup = renderToStaticMarkup(
      <LoginPage onLogin={() => undefined} isLoading={false} error={null} />,
    );
    const registerMarkup = renderToStaticMarkup(
      <RegisterPage onRegister={async () => undefined} isLoading={false} error={null} />,
    );
    const recoveryMarkup = renderToStaticMarkup(
      <ForgotPasswordPage onRequestReset={async () => undefined} isLoading={false} />,
    );

    expect(loginMarkup).toContain("Authorize Session");
    expect(registerMarkup).toContain("Join Platform");
    expect(recoveryMarkup).toContain("Send Reset Link");
  });

  it("renders the consent view as a governed public route", () => {
    const markup = renderToStaticMarkup(
      <ConsentPage
        approveTarget="#/profile"
        cancelTarget="#/login"
        clientName="Example Portal"
        scopes={["openid", "email", "profile"]}
      />,
    );

    expect(markup).toContain("Review consent");
    expect(markup).toContain("Example Portal");
    expect(markup).toContain("openid");
    expect(markup).toContain("Approve access");
  });
});
