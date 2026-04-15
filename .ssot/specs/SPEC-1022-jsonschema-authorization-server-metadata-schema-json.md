# Repo spec: specs/jsonschema/authorization-server-metadata.schema.json

{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://authn.example.com/schemas/authorization-server-metadata.schema.json",
  "type": "object",
  "required": [
    "issuer",
    "authorization_endpoint",
    "token_endpoint"
  ],
  "properties": {
    "issuer": {
      "type": "string",
      "format": "uri"
    },
    "authorization_endpoint": {
      "type": "string",
      "format": "uri"
    },
    "token_endpoint": {
      "type": "string",
      "format": "uri"
    },
    "jwks_uri": {
      "type": "string",
      "format": "uri"
    }
  },
  "additionalProperties": true
}
