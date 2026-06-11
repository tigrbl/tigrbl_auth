def resolve_deployment(
    settings_obj: object | None = None,
    *,
    profile: str | None = None,
    surface_sets: tuple[str, ...] | list[str] | str | None = None,
    protocol_slices: tuple[str, ...] | list[str] | str | None = None,
    extensions: tuple[str, ...] | list[str] | str | None = None,
    plugin_mode: str | None = None,
    runtime_style: str | None = None,
    product_surface: str | None = None,
    flag_overrides: dict[str, Any] | None = None,
    profile_source: dict[str, Any] | None = None,
) -> ResolvedDeployment:
    raw = _settings_dict(settings_obj)
    if flag_overrides:
        raw.update(flag_overrides)

    profile_name = _valid_or_default(
        profile or str(raw.get("deployment_profile", "baseline")),
        VALID_PROFILES,
        "baseline",
    )
    raw.update(PROFILE_DEFAULT_OVERRIDES.get(profile_name, {}))
    plugin_mode_name = _valid_or_default(
        plugin_mode or str(raw.get("surface_plugin_mode", "mixed")),
        VALID_PLUGIN_MODES,
        "mixed",
    )
    runtime_style_name = _valid_or_default(
        runtime_style or str(raw.get("runtime_style", "standalone")),
        VALID_RUNTIME_STYLES,
        "standalone",
    )
    if plugin_mode is not None:
        raw["surface_plugin_mode"] = plugin_mode_name

    allowed_profile_flags = set(flags_for_profile(profile_name))
    requested_surface_sets = _csv_items(
        surface_sets if surface_sets is not None else raw.get("active_surface_sets")
    )
    requested_protocol_slices = _csv_items(
        protocol_slices
        if protocol_slices is not None
        else raw.get("active_protocol_slices")
    )
    requested_extensions = _csv_items(
        extensions if extensions is not None else raw.get("active_extensions")
    )

    product_surface_name = product_surface or next(
        (name for name in requested_surface_sets if name in PRODUCT_SURFACE_REGISTRY),
        None,
    )
    product_meta = _product_config(product_surface_name)
    if product_meta is not None:
        effective_surface_sets = tuple(
            str(item) for item in product_meta.get("surface_sets", ())
        )
        plugin_mode_name = _plugin_mode_for_surface_sets(effective_surface_sets)
        raw["surface_plugin_mode"] = plugin_mode_name
    else:
        effective_surface_sets = _derive_surface_sets(
            raw, plugin_mode_name, requested_surface_sets
        )
    effective_protocol_slices = _derive_protocol_slices(
        raw, allowed_profile_flags, requested_protocol_slices
    )
    effective_extensions = _derive_extensions(raw, requested_extensions)

    flags: dict[str, bool | str] = {}
    profile_flags = _all_profile_flags()
    for group_name, group in FEATURE_FLAG_GROUPS.items():
        group_flags = group.get("flags", {})
        if isinstance(group_flags, dict):
            names = tuple(group_flags.keys())
        else:
            names = tuple()
        for name in names:
            value = raw.get(name, DEFAULT_VALUES.get(name, False))
            if name in profile_flags:
                flags[name] = bool(value) and name in allowed_profile_flags
            elif name == "surface_plugin_mode":
                flags[name] = plugin_mode_name
            elif name == "oauth21_alignment_mode":
                flags[name] = str(value)
            else:
                flags[name] = bool(value) if isinstance(value, bool) else value

    for slice_name, meta in PROTOCOL_SLICE_REGISTRY.items():
        active = slice_name in effective_protocol_slices
        for flag in meta.get("flags", ()):
            flags[flag] = bool(flags.get(flag, False)) and active

    for extension_name, meta in EXTENSION_REGISTRY.items():
        active = extension_name in effective_extensions
        for flag in meta.get("flags", ()):
            if flag in flags:
                flags[flag] = bool(flags.get(flag, False)) and active

    surfaces = {
        "surface_public_enabled": "public-rest" in effective_surface_sets,
        "surface_admin_enabled": bool(
            {"admin-rest", "admin-rpc"}.intersection(effective_surface_sets)
        ),
        "surface_rpc_enabled": "admin-rpc" in effective_surface_sets,
        "surface_diagnostics_enabled": "diagnostics" in effective_surface_sets,
        "surface_operator_enabled": bool(raw.get("surface_operator_enabled", True)),
        "surface_plugin_mode": plugin_mode_name,
    }
    flags.update(surfaces)

    active_capabilities: list[str] = []
    active_routes: list[str] = []
    for capability_name, meta in SURFACE_CAPABILITY_REGISTRY.items():
        if meta.get("surface_set") not in effective_surface_sets:
            continue
        if not _capability_allowed(capability_name, product_meta):
            continue
        required_flags = tuple(meta.get("flags", ()))
        if all(bool(flags.get(name, False)) for name in required_flags):
            active_capabilities.append(capability_name)
            for path in tuple(meta.get("paths", ())):
                path_str = str(path)
                if path_str not in active_routes:
                    active_routes.append(path_str)

    active_contract_routes = [
        path
        for path in active_routes
        if bool(ROUTE_REGISTRY.get(path, {}).get("contract_visible", False))
    ]
    active_discovery_routes = [
        path
        for path in active_routes
        if bool(ROUTE_REGISTRY.get(path, {}).get("discovery_visible", False))
    ]

    active_targets: list[str] = []
    for label, required_flags in TARGET_FLAG_REQUIREMENTS.items():
        if all(bool(flags.get(name, False)) for name in required_flags):
            active_targets.append(label)

    if runtime_style_name in {"plugin", "standalone"}:
        active_targets.append("ASGI 3 application package")
    if runtime_style_name == "standalone":
        active_targets.extend(
            [
                "Runner profile: Uvicorn",
                "Runner profile: Hypercorn",
                "Runner profile: Tigrcorn",
            ]
        )
    if surfaces.get("surface_operator_enabled", False):
        active_targets.extend(
            [
                "CLI operator surface",
                "Bootstrap and migration lifecycle",
                "Key lifecycle and JWKS publication",
                "Import/export portability",
                "Release bundle and signature verification",
            ]
        )
    active_targets = list(dict.fromkeys(active_targets))

    active_methods: list[str] = []
    if bool(surfaces["surface_rpc_enabled"]):
        for name, meta in OPENRPC_METHOD_REGISTRY.items():
            if meta.get("surface_set") in effective_surface_sets:
                if not _rpc_method_allowed(name, product_meta):
                    continue
                active_methods.append(name)

    return ResolvedDeployment(
        profile=profile_name,
        plugin_mode=plugin_mode_name,
        runtime_style=runtime_style_name,
        surface_sets=tuple(effective_surface_sets),
        protocol_slices=tuple(effective_protocol_slices),
        extensions=tuple(effective_extensions),
        issuer=str(raw.get("issuer", DEFAULT_VALUES["issuer"])),
        protected_resource_identifier=str(
            raw.get(
                "protected_resource_identifier",
                DEFAULT_VALUES["protected_resource_identifier"],
            )
        ),
        strict_boundary_enforcement=bool(raw.get("strict_boundary_enforcement", True)),
        surfaces=surfaces,
        flags=flags,
        active_capabilities=tuple(active_capabilities),
        active_routes=tuple(active_routes),
        active_contract_routes=tuple(active_contract_routes),
        active_discovery_routes=tuple(active_discovery_routes),
        active_targets=tuple(active_targets),
        active_openrpc_methods=tuple(active_methods),
        product_surface=product_surface_name,
        allowed_admin_resources=tuple(
            str(item) for item in (product_meta or {}).get("admin_resources", ())
        ),
        allowed_admin_rest_groups=tuple(
            str(item) for item in (product_meta or {}).get("admin_rest_groups", ())
        ),
        profile_source=dict(
            profile_source
            or {"kind": "packaged-profile-id", "profile_id": profile_name}
        ),
    )


def deployment_from_app(
    app: Any | None, fallback_settings: object | None = None
) -> ResolvedDeployment:
    state = getattr(app, "state", None) if app is not None else None
    deployment = (
        getattr(state, "tigrbl_auth_deployment", None) if state is not None else None
    )
    if isinstance(deployment, ResolvedDeployment):
        return deployment
    return resolve_deployment(fallback_settings)


def deployment_from_request(
    request: Any | None, fallback_settings: object | None = None
) -> ResolvedDeployment:
    app = getattr(request, "app", None) if request is not None else None
    return deployment_from_app(app, fallback_settings)


__all__ = [
    "DEFAULT_VALUES",
    "EXTENSION_REGISTRY",
    "OPENRPC_METHOD_REGISTRY",
    "PLUGIN_MODE_TO_SURFACE_SETS",
    "PRODUCT_SURFACE_REGISTRY",
    "PROTOCOL_SLICE_REGISTRY",
    "ROUTE_REGISTRY",
    "ResolvedDeployment",
    "SURFACE_SET_REGISTRY",
    "TARGET_FLAG_REQUIREMENTS",
    "SURFACE_CAPABILITY_REGISTRY",
    "VALID_PLUGIN_MODES",
    "VALID_PRODUCT_SURFACES",
    "VALID_PROFILES",
    "VALID_RUNTIME_STYLES",
    "resolve_deployment",
    "deployment_from_app",
    "deployment_from_request",
]
