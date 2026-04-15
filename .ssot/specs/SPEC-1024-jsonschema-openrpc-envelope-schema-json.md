# Repo spec: specs/jsonschema/openrpc-envelope.schema.json

{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://authn.example.com/schemas/openrpc-envelope.schema.json",
  "type": "object",
  "required": [
    "openrpc",
    "info",
    "methods"
  ],
  "properties": {
    "openrpc": {
      "type": "string"
    },
    "info": {
      "type": "object"
    },
    "methods": {
      "type": "array",
      "items": {
        "type": "object"
      }
    }
  },
  "additionalProperties": true
}
