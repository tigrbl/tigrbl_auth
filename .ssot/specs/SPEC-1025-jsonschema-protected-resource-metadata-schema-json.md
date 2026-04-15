# Repo spec: specs/jsonschema/protected-resource-metadata.schema.json

{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://authn.example.com/schemas/protected-resource-metadata.schema.json",
  "type": "object",
  "required": [
    "resource",
    "authorization_servers"
  ],
  "properties": {
    "resource": {
      "type": "string",
      "format": "uri"
    },
    "authorization_servers": {
      "type": "array",
      "items": {
        "type": "string",
        "format": "uri"
      }
    },
    "jwks_uri": {
      "type": "string",
      "format": "uri"
    }
  },
  "additionalProperties": true
}
