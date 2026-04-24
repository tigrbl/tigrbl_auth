# Issue Draft: Tigrbl mounts generated CRUD REST routes at both root and `/api`

## Title

Generated model CRUD routes are mounted twice: once at root and once under `/api`

## Summary

When a `TigrblApi` is used as a router-style surface and models are included with `include_model()` or `include_models()` without an explicit prefix, generated CRUD REST routes are exposed twice:

- root form, for example `/widget`
- `/api` form, for example `/api/widget`

The duplication appears to come from `TigrblApi` itself. The model router is first mounted at the default prefix, which currently resolves to the application/router root, and then `TigrblApi.include_model(s)` mounts the same generated router again under `self.rest_prefix`, whose default is `/api`.

## Expected Behavior

Each generated model CRUD REST route should be mounted once for a given API surface.

For the default `TigrblApi` behavior, either:

- expose only `/api/<resource>` when `REST_PREFIX = "/api"` is intended to be canonical, or
- expose only `/<resource>` when the root mount is intended to be canonical.

The framework should not expose both route families for the same model unless the caller explicitly requests both.

## Actual Behavior

A single model inclusion produces both route families. For a `Widget` model, the route table contains entries equivalent to:

```text
/widget
/widget/{item_id}
/api/widget
/api/widget/{item_id}
```

with the same CRUD operation names repeated across both route families.

## Minimal Reproduction

This demonstration uses only `tigrbl` and a single model. It inspects the in-memory route table; it does not need a running server.

```python
from tigrbl import Base, TigrblApi
from tigrbl.column.shortcuts import ColumnSpec, F, IO, S, acol
from tigrbl.orm.mixins import GUIDPk
from tigrbl.types import Mapped, String


class Widget(Base, GUIDPk):
    __tablename__ = "widgets"

    name: Mapped[str] = acol(
        spec=ColumnSpec(
            storage=S(String(120), nullable=False),
            field=F(required_in=("create",)),
            io=IO(
                in_verbs=("create", "update", "replace"),
                out_verbs=("read", "list"),
                filter_ops=("eq",),
                sortable=True,
            ),
        )
    )


api = TigrblApi()
api.include_model(Widget)

for route in sorted(
    (
        getattr(route, "path", ""),
        ",".join(sorted(getattr(route, "methods", []) or [])),
        getattr(route, "name", ""),
    )
    for route in getattr(api, "routes", [])
    if getattr(route, "path", "")
):
    print(route)
```

Observed route rows include both route families:

```text
/api/widget Widget.clear
/api/widget Widget.create
/api/widget Widget.list
/api/widget/{item_id} Widget.delete
/api/widget/{item_id} Widget.read
/api/widget/{item_id} Widget.replace
/api/widget/{item_id} Widget.update
/widget Widget.clear
/widget Widget.create
/widget Widget.list
/widget/{item_id} Widget.delete
/widget/{item_id} Widget.read
/widget/{item_id} Widget.replace
/widget/{item_id} Widget.update
```

If `TigrblApp` is the preferred maintainer-facing reproduction surface, the same behavior can be observed by including a `TigrblApi` into a `TigrblApp` after the model has been included:

```python
from tigrbl import TigrblApp

app = TigrblApp()
app.include_router(api)

for route in sorted(
    (
        getattr(route, "path", ""),
        ",".join(sorted(getattr(route, "methods", []) or [])),
        getattr(route, "name", ""),
    )
    for route in getattr(app, "routes", [])
    if getattr(route, "path", "")
):
    print(route)
```

## Why This Looks Upstream

The behavior follows from the current upstream mounting flow:

1. `TigrblApi.REST_PREFIX` defaults to `/api`.
2. `TigrblApi.include_model()` delegates to the lower-level include helper.
3. The lower-level include helper mounts the generated model router at the default model prefix.
4. The default model prefix currently returns `""`, meaning the router is mounted at root.
5. After that helper returns, `TigrblApi.include_model()` mounts the same router again with `prefix=self.rest_prefix`.

The same pattern exists in `include_models()`: each generated model router is mounted during lower-level inclusion, then all returned routers are mounted again under `self.rest_prefix` when `base_prefix is None`.

## Suspected Fix Direction

`TigrblApi.include_model()` and `TigrblApi.include_models()` should mount each generated model router only once.

Possible fixes:

- have the lower-level include helper bind and attach namespaces without mounting when called from `TigrblApi.include_model(s)`, then let `TigrblApi` perform the single canonical mount under `self.rest_prefix`;
- or remove the additional `self.include_router(router, prefix=self.rest_prefix)` pass when the lower-level helper has already mounted the router;
- or make root mounting versus `/api` mounting explicit through a single option, rather than doing both by default.

## Acceptance Criteria

- Including one model with default `TigrblApi()` settings exposes one canonical REST route family.
- The route table does not contain both `/<resource>` and `/api/<resource>` for the same generated CRUD operations unless explicitly configured.
- Existing explicit prefix behavior remains deterministic.
- A regression test covers both `include_model()` and `include_models()`.
