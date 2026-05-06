# Unresolved Security Contract Issues

This report captures the issues still observable against a service built on
`tigrbl==0.4.0`.

The examples are intentionally small. They do not depend on local application
internals, Docker layout, or repository-specific terminology. They only require
an HTTP service exposing:

- `/openapi.json`
- `/openrpc.json`
- `/tenant`
- `/rpc`

## Runtime Under Test

Observed package versions in the running service:

```text
tigrbl 0.4.0
tigrbl_runtime 0.1.12.dev1
```

## Issue 1: OpenAPI Does Not Declare Authentication

### Why this matters

OpenAPI clients and operators cannot tell which operations require
authentication. The generated OpenAPI document does not define any security
scheme, and no operation declares a security requirement.

### Minimal proof

```bash
python - <<'PY'
import json
import urllib.request

spec = json.load(urllib.request.urlopen("http://localhost:8000/openapi.json"))

operations_with_security = sum(
    1
    for path_item in spec.get("paths", {}).values()
    for operation in path_item.values()
    if isinstance(operation, dict) and operation.get("security")
)

print("securitySchemes =", spec.get("components", {}).get("securitySchemes"))
print("operations_with_security =", operations_with_security)
PY
```

### Observed result

```text
securitySchemes = None
operations_with_security = 0
```

### Expected behavior

If generated CRUD operations are protected, the OpenAPI document should include
a security scheme such as bearer token, API key, OAuth2, or OpenID Connect, and
protected operations should declare their security requirement.

If some operations are intentionally public, that public status should be
explicit and limited to those operations.

## Issue 2: OpenRPC Does Not Declare Authentication

### Why this matters

JSON-RPC clients cannot discover whether methods require authentication. The
generated OpenRPC document has no usable security scheme and no method-level
security requirements.

### Minimal proof

```bash
python - <<'PY'
import json
import urllib.request

spec = json.load(urllib.request.urlopen("http://localhost:8000/openrpc.json"))

methods_with_security = sum(
    1 for method in spec.get("methods", []) if method.get("security")
)

print("securitySchemes =", spec.get("components", {}).get("securitySchemes"))
print("methods_with_security =", methods_with_security)
PY
```

### Observed result

```text
securitySchemes = {}
methods_with_security = 0
```

### Expected behavior

If generated JSON-RPC methods are protected, the OpenRPC document should include
the security scheme and each protected method should declare the requirement.

## Issue 3: Generated REST Read Is Accessible Without Credentials

### Why this matters

A generated table read endpoint returns data without an `Authorization` header.
That means the generated route is not only missing documentation of auth; it is
also not enforcing an authentication gate for this request.

### Minimal proof

```bash
curl -i http://localhost:8000/tenant
```

### Observed result

```http
HTTP/1.1 200 OK
content-type: application/json
```

The response body contains tenant records.

### Expected behavior

If generated CRUD routes are intended to be protected by default, an
unauthenticated request should return `401 Unauthorized` or `403 Forbidden`.

If generated CRUD routes are intentionally public by default, that should be
explicit in the generated contract.

## Issue 4: Generated JSON-RPC Read Is Accessible Without Credentials

### Why this matters

A generated JSON-RPC read method returns data without an `Authorization` header.
As with REST, this means auth is not being enforced for this request and the
contract does not advertise any auth requirement.

### Minimal proof

```bash
python - <<'PY'
import json
import urllib.request

payload = {
    "jsonrpc": "2.0",
    "method": "Tenant.list",
    "params": {},
    "id": 1,
}

request = urllib.request.Request(
    "http://localhost:8000/rpc",
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json"},
    method="POST",
)

with urllib.request.urlopen(request) as response:
    print(response.status)
    print(response.read().decode())
PY
```

### Observed result

```text
200
{"jsonrpc":"2.0","result":[...],"id":1}
```

### Expected behavior

If generated JSON-RPC methods are intended to be protected by default, an
unauthenticated call should return an authentication or authorization error.

If generated JSON-RPC methods are intentionally public by default, that should
be explicit in OpenRPC.

## Suggested Fix Direction

The framework should expose one clear policy for generated operations:

1. Protected by default: generated REST and JSON-RPC operations enforce auth and
   emit matching OpenAPI/OpenRPC security metadata.
2. Public by default: generated REST and JSON-RPC operations remain open, but the
   generated contracts clearly identify them as unauthenticated/public.
3. Per-operation policy: generated operation metadata controls both runtime auth
   enforcement and generated contract security declarations from the same source.

The important invariant is that runtime behavior and generated API contracts
must agree.
