# Repo spec: specs/openapi/profiles/hardening/tigrbl_auth.public.json

{
  "openapi": "3.1.0",
  "info": {
    "title": "tigrbl_auth public auth server",
    "version": "0.3.2.dev13",
    "description": "Generated public contract filtered by the effective deployment boundary."
  },
  "servers": [
    {
      "url": "https://authn.example.com"
    }
  ],
  "paths": {
    "/login": {
      "post": {
        "summary": "Password login helper",
        "responses": {
          "200": {
            "description": "Success"
          }
        },
        "tags": [
          "auth"
        ]
      }
    },
    "/authorize": {
      "get": {
        "summary": "Authorization endpoint",
        "responses": {
          "200": {
            "description": "Success"
          }
        },
        "tags": [
          "oauth2",
          "oidc"
        ]
      }
    },
    "/token": {
      "post": {
        "summary": "Token endpoint",
        "responses": {
          "200": {
            "description": "Success"
          }
        },
        "tags": [
          "oauth2"
        ]
      }
    },
    "/userinfo": {
      "get": {
        "summary": "OIDC UserInfo endpoint",
        "responses": {
          "200": {
            "description": "Success"
          }
        },
        "tags": [
          "oidc"
        ]
      }
    },
    "/.well-known/openid-configuration": {
      "get": {
        "summary": "OIDC discovery document",
        "responses": {
          "200": {
            "description": "Success"
          }
        },
        "tags": [
          ".well-known"
        ]
      }
    },
    "/.well-known/oauth-authorization-server": {
      "get": {
        "summary": "OAuth authorization server metadata",
        "responses": {
          "200": {
            "description": "Success"
          }
        },
        "tags": [
          ".well-known"
        ]
      }
    },
    "/.well-known/oauth-protected-resource": {
      "get": {
        "summary": "OAuth protected resource metadata",
        "responses": {
          "200": {
            "description": "Success"
          }
        },
        "tags": [
          ".well-known"
        ]
      }
    },
    "/.well-known/jwks.json": {
      "get": {
        "summary": "JSON Web Key Set",
        "responses": {
          "200": {
            "description": "Success"
          }
        },
        "tags": [
          ".well-known"
        ]
      }
    }
  },
  "components": {
    "securitySchemes": {
      "bearerAuth": {
        "type": "http",
        "scheme": "bearer"
      },
      "oauth2": {
        "type": "oauth2",
        "flows": {
          "authorizationCode": {
            "authorizationUrl": "https://authn.example.com/authorize",
            "tokenUrl": "https://authn.example.com/token",
            "scopes": {
              "openid": "OpenID Connect scope"
            }
          }
        }
      },
      "openIdConnect": {
        "type": "openIdConnect",
        "openIdConnectUrl": "https://authn.example.com/.well-known/openid-configuration"
      }
    }
  },
  "x-tigrbl-auth": {
    "profile": "hardening",
    "plugin_mode": "mixed",
    "runtime_style": "standalone",
    "surface_sets": [
      "public-rest",
      "admin-rpc",
      "diagnostics"
    ],
    "protocol_slices": [
      "device",
      "dpop"
    ],
    "extensions": [],
    "active_targets": [
      "RFC 6749",
      "RFC 6750",
      "RFC 7636",
      "RFC 8414",
      "RFC 8615",
      "RFC 7515",
      "RFC 7516",
      "RFC 7517",
      "RFC 7518",
      "RFC 7519",
      "RFC 8252",
      "RFC 8628",
      "RFC 9449",
      "RFC 9728",
      "OIDC Core 1.0",
      "OIDC Discovery 1.0",
      "OIDC UserInfo",
      "OpenAPI 3.1 / 3.2 compatible public contract",
      "OpenRPC 1.4.x admin/control-plane contract"
    ],
    "strict_boundary_enforcement": true
  }
}
