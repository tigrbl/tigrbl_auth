import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";

import { Layout } from "../components/Layout";
import { ConsentPage } from "./ConsentPage";
import { ForgotPasswordPage } from "./ForgotPasswordPage";
import { LoginPage } from "./LoginPage";
import { ProfilePage } from "./ProfilePage";
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

  it("does not render raw backend diagnostics on the login page", () => {
    const markup = renderToStaticMarkup(
      <LoginPage
        onLogin={() => undefined}
        isLoading={false}
        error={"<class 'sqlalchemy.exc.StatementError'>: (builtins.AttributeError) 'str' object has no attribute 'hex' [SQL: SELECT users.id FROM users]"}
      />,
    );

    expect(markup).toContain("The identity provider returned an internal error.");
    expect(markup).not.toContain("AttributeError");
    expect(markup).not.toContain("SELECT");
    expect(markup).not.toContain("sqlalchemy");
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

  it("renders structured OIDC context without synthetic issuer metadata", () => {
    const markup = renderToStaticMarkup(
      <ProfilePage
        user={{
          id: "user-1",
          email: "user@example.com",
          name: "User One",
          provider: "generic",
          isEmailVerified: true,
          mfaEnabled: false,
          oidcContext: {
            id_token: {
              iss: "http://localhost:18081",
              sub: "user-1",
              aud: "tigrbl-auth-public-uix",
              nonce: "nonce-1",
              auth_time: 1781567454,
              sid: "session-1",
            },
            access_token: {
              scope: "openid profile email",
            },
            userinfo: {
              sub: "user-1",
              email: "user@example.com",
              name: "User One",
              email_verified: true,
            },
            client: {
              provider: "generic",
              client_id: "tigrbl-auth-public-uix",
              issuer: "http://localhost:18081",
              scope: "openid profile email",
              token_type: "bearer",
            },
            authorization_request: {
              nonce: "nonce-1",
              redirect_uri: "http://localhost:18081/callback",
            },
          },
        }}
      />,
    );

    expect(markup).toContain("&quot;id_token&quot;");
    expect(markup).toContain("&quot;userinfo&quot;");
    expect(markup).toContain("&quot;client&quot;");
    expect(markup).toContain("Issuer");
    expect(markup).toContain("ID token");
    expect(markup).toContain("Subject");
    expect(markup).toContain("UserInfo");
    expect(markup).toContain("Scope");
    expect(markup).toContain("Access token");
    expect(markup).toContain("Token Type");
    expect(markup).toContain("Token response");
    expect(markup).toContain("http://localhost:18081");
    expect(markup).toContain("user@example.com");
    expect(markup).not.toContain("&quot;iss&quot;: &quot;tigrbl_auth&quot;");
  });
});
