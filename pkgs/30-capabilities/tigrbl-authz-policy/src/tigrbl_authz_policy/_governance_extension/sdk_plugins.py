from __future__ import annotations

from .models import *
from .models import _utc_now_iso, _version_in_range

class SDKEcosystemCatalog:
    def __init__(self) -> None:
        self._packages: dict[str, SDKPackage] = {}

    @property
    def packages(self) -> Mapping[str, SDKPackage]:
        return dict(self._packages)

    def register_sdk(
        self,
        sdk_id: str,
        *,
        package_name: str,
        language: str,
        version: str,
        compatible_runtime_range: tuple[str, str],
        generated_contracts: Mapping[str, str],
        auth_helpers: Iterable[str],
        supported_errors: Iterable[str],
        release_channel: str = "stable",
    ) -> SDKPackage:
        if not generated_contracts:
            raise ValueError("sdk package must declare generated contract alignment")
        helper_tuple = tuple(sorted(set(auth_helpers)))
        error_tuple = tuple(sorted(set(supported_errors)))
        if not helper_tuple:
            raise ValueError("sdk package must declare authentication helpers")
        if not error_tuple:
            raise ValueError("sdk package must declare supported errors")
        package = SDKPackage(
            sdk_id=sdk_id,
            package_name=package_name,
            language=language,
            version=version,
            compatible_runtime_range=compatible_runtime_range,
            generated_contracts=dict(generated_contracts),
            auth_helpers=helper_tuple,
            supported_errors=error_tuple,
            release_channel=release_channel,
        )
        self._packages[sdk_id] = package
        return package

    def compatible_sdk_ids(self, *, runtime_version: str, language: str | None = None) -> tuple[str, ...]:
        compatible: list[str] = []
        for package in self._packages.values():
            if language is not None and package.language != language:
                continue
            if _version_in_range(runtime_version, package.compatible_runtime_range):
                compatible.append(package.sdk_id)
        return tuple(sorted(compatible))

    def build_alignment_report(
        self,
        *,
        runtime_version: str,
        expected_contracts: Mapping[str, str],
    ) -> dict[str, Any]:
        aligned_sdk_ids: list[str] = []
        mismatches: dict[str, dict[str, str]] = {}
        for package in self._packages.values():
            if not _version_in_range(runtime_version, package.compatible_runtime_range):
                mismatches[package.sdk_id] = {"runtime": runtime_version, "reason": "runtime version out of range"}
                continue
            contract_mismatch = {
                kind: f"expected {expected_version}, got {package.generated_contracts.get(kind, 'missing')}"
                for kind, expected_version in expected_contracts.items()
                if package.generated_contracts.get(kind) != expected_version
            }
            if contract_mismatch:
                mismatches[package.sdk_id] = contract_mismatch
                continue
            aligned_sdk_ids.append(package.sdk_id)
        return {
            "runtime_version": runtime_version,
            "expected_contracts": dict(expected_contracts),
            "compatible_sdk_ids": list(self.compatible_sdk_ids(runtime_version=runtime_version)),
            "aligned_sdk_ids": sorted(aligned_sdk_ids),
            "mismatches": mismatches,
        }

    def summary(self) -> dict[str, Any]:
        languages = sorted({package.language for package in self._packages.values()})
        return {
            "package_count": len(self._packages),
            "languages": languages,
            "release_channels": sorted({package.release_channel for package in self._packages.values()}),
        }


class PluginRuntimeRegistry:
    def __init__(self) -> None:
        self._plugins: dict[str, PluginDescriptor] = {}
        self._hook_handlers: dict[str, dict[str, Callable[[Mapping[str, Any]], Mapping[str, Any]]]] = {}
        self._events: list[PluginLifecycleEvent] = []

    @property
    def plugins(self) -> Mapping[str, PluginDescriptor]:
        return dict(self._plugins)

    @property
    def events(self) -> tuple[PluginLifecycleEvent, ...]:
        return tuple(self._events)

    def register_plugin(
        self,
        plugin_id: str,
        *,
        name: str,
        version: str,
        extension_points: Iterable[str],
        hooks: Mapping[str, Callable[[Mapping[str, Any]], Mapping[str, Any]]],
        compatible_sdk_ids: Iterable[str],
        isolation_mode: str = "process",
        operator_controls: Iterable[str] = ("audit", "disable"),
        fail_behavior: str = "disable_on_error",
    ) -> PluginDescriptor:
        descriptor = PluginDescriptor(
            plugin_id=plugin_id,
            name=name,
            version=version,
            extension_points=tuple(sorted(set(extension_points))),
            lifecycle_hooks=tuple(sorted(set(hooks))),
            compatible_sdk_ids=tuple(sorted(set(compatible_sdk_ids))),
            isolation_mode=isolation_mode,
            operator_controls=tuple(sorted(set(operator_controls))),
            fail_behavior=fail_behavior,
            registered_at=_utc_now_iso(),
        )
        self._plugins[plugin_id] = descriptor
        self._hook_handlers[plugin_id] = dict(hooks)
        return descriptor

    def disable_plugin(self, plugin_id: str) -> PluginDescriptor:
        descriptor = self._plugins[plugin_id]
        updated = replace(descriptor, enabled=False)
        self._plugins[plugin_id] = updated
        return updated

    def enable_plugin(self, plugin_id: str) -> PluginDescriptor:
        descriptor = self._plugins[plugin_id]
        updated = replace(descriptor, enabled=True)
        self._plugins[plugin_id] = updated
        return updated

    def run_hook(self, plugin_id: str, hook_name: str, context: Mapping[str, Any]) -> Mapping[str, Any]:
        descriptor = self._plugins.get(plugin_id)
        if descriptor is None:
            raise KeyError(f"unknown plugin {plugin_id!r}")
        if not descriptor.enabled:
            raise PermissionError("plugin is disabled")
        handler = self._hook_handlers.get(plugin_id, {}).get(hook_name)
        if handler is None:
            raise KeyError(f"plugin {plugin_id!r} does not expose hook {hook_name!r}")
        try:
            result = dict(handler(dict(context)))
        except Exception as exc:  # pragma: no cover - exact exceptions are plugin-defined.
            message = f"{type(exc).__name__}: {exc}"
            self._events.append(
                PluginLifecycleEvent(
                    event_id=f"plg-{uuid4().hex}",
                    plugin_id=plugin_id,
                    hook_name=hook_name,
                    outcome="failed",
                    message=message,
                    recorded_at=_utc_now_iso(),
                )
            )
            if descriptor.fail_behavior == "disable_on_error" or "disable" in descriptor.operator_controls:
                self.disable_plugin(plugin_id)
            raise RuntimeError(f"plugin hook failed in isolated execution: {message}") from exc
        self._events.append(
            PluginLifecycleEvent(
                event_id=f"plg-{uuid4().hex}",
                plugin_id=plugin_id,
                hook_name=hook_name,
                outcome="succeeded",
                message="hook completed",
                recorded_at=_utc_now_iso(),
            )
        )
        return result

    def summary(self) -> dict[str, Any]:
        enabled = [plugin.plugin_id for plugin in self._plugins.values() if plugin.enabled]
        return {
            "plugin_count": len(self._plugins),
            "enabled_plugin_ids": sorted(enabled),
            "event_count": len(self._events),
            "isolation_modes": sorted({plugin.isolation_mode for plugin in self._plugins.values()}),
        }


