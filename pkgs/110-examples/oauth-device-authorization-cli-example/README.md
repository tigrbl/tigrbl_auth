# OAuth Device Authorization CLI Example

`oauth-device-authorization-cli-example` is a runnable consumer example for OAuth 2.0 Device
Authorization Grant usage against a Tigrbl Auth deployment. It discovers the
issuer metadata, starts a device ceremony, polls the token endpoint, and stores
the resulting tokens for the example CLI.

## Run

Install the workspace example extra and invoke the command:

```shell
uv sync --extra examples
uv run oauth-device-login login --issuer https://issuer.example --client-id CLIENT_ID
```

## Ownership

This package belongs to terminal layer `110-examples`. It demonstrates public
protocol and API behavior; it does not own OAuth semantics, production runtime
composition, persistence, or reusable test helpers.
