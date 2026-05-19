from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any, Literal, Protocol, TypeAlias

Scope: TypeAlias = dict[str, Any]
ASGIMessage: TypeAlias = dict[str, Any]
Receive: TypeAlias = Callable[[], Awaitable[ASGIMessage]]
Send: TypeAlias = Callable[[ASGIMessage], Awaitable[None]]
RuntimeDiagnosticLevel = Literal["info", "warning", "error"]
RunnerOptionValueType = Literal["string", "int", "float", "bool", "choice"]


class ASGIApp(Protocol):
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None: ...


@dataclass(slots=True, frozen=True)
class RunnerCapability:
    name: str
    description: str
    portable: bool = True

    def to_manifest(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "portable": self.portable,
        }


@dataclass(slots=True, frozen=True)
class RunnerFlagMetadata:
    name: str
    flags: tuple[str, ...]
    description: str
    portable: bool = True
    default: Any = None
    choices: tuple[str, ...] = ()
    value_type: RunnerOptionValueType = "string"

    def to_manifest(self) -> dict[str, Any]:
        payload = {
            "name": self.name,
            "flags": list(self.flags),
            "description": self.description,
            "portable": self.portable,
            "value_type": self.value_type,
        }
        if self.default is not None:
            payload["default"] = self.default
        if self.choices:
            payload["choices"] = list(self.choices)
        return payload


@dataclass(slots=True, frozen=True)
class RuntimeDiagnostic:
    code: str
    level: RuntimeDiagnosticLevel
    message: str
    runner: str | None = None
    field: str | None = None

    def to_manifest(self) -> dict[str, Any]:
        payload = {
            "code": self.code,
            "level": self.level,
            "message": self.message,
        }
        if self.runner is not None:
            payload["runner"] = self.runner
        if self.field is not None:
            payload["field"] = self.field
        return payload




@dataclass(slots=True, frozen=True)
class CommandProbeResult:
    passed: bool
    command: str
    message: str
    exit_code: int | None = None
    executed: bool = True
    launch_ready: bool | None = None
    error_type: str | None = None
    stdout: str | None = None
    stderr: str | None = None

    def to_manifest(self) -> dict[str, Any]:
        payload = {
            "passed": self.passed,
            "executed": self.executed,
            "command": self.command,
            "message": self.message,
        }
        if self.exit_code is not None:
            payload["exit_code"] = self.exit_code
        if self.launch_ready is not None:
            payload["launch_ready"] = self.launch_ready
        if self.error_type is not None:
            payload["error_type"] = self.error_type
        if self.stdout is not None:
            payload["stdout"] = self.stdout
        if self.stderr is not None:
            payload["stderr"] = self.stderr
        return payload


@dataclass(slots=True, frozen=True)
class HttpEndpointProbeResult:
    name: str
    path: str
    passed: bool
    message: str
    status_code: int | None = None
    executed: bool = True
    expected_status: int | None = 200
    error_type: str | None = None

    def to_manifest(self) -> dict[str, Any]:
        payload = {
            "name": self.name,
            "path": self.path,
            "passed": self.passed,
            "executed": self.executed,
            "message": self.message,
        }
        if self.status_code is not None:
            payload["status_code"] = self.status_code
        if self.expected_status is not None:
            payload["expected_status"] = self.expected_status
        if self.error_type is not None:
            payload["error_type"] = self.error_type
        return payload

@dataclass(slots=True, frozen=True)
class ApplicationProbeResult:
    passed: bool
    app_factory: str
    message: str
    error_type: str | None = None

    def to_manifest(self) -> dict[str, Any]:
        payload = {
            "passed": self.passed,
            "app_factory": self.app_factory,
            "message": self.message,
        }
        if self.error_type is not None:
            payload["error_type"] = self.error_type
        return payload
