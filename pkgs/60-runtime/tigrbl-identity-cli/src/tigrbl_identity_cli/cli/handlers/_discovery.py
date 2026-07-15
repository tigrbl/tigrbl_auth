from __future__ import annotations

from tigrbl_identity_cli.discovery_service import (
    diff_discovery as _svc_diff_discovery,
    publish_discovery as _svc_publish_discovery,
    show_discovery as _svc_show_discovery,
    validate_discovery as _svc_validate_discovery,
)


def handle_discovery_show(args: Any) -> int:
    deployment = _resolved_from_args(args)
    payload = {
        "command": "discovery.show",
        "profile_source": deployment.profile_source,
        **_svc_show_discovery(
            _repo_root(getattr(args, "repo_root", None)), profile=deployment.profile
        ),
    }
    return _emit(args, payload)


def handle_discovery_validate(args: Any) -> int:
    deployment = _resolved_from_args(args)
    payload = {
        "command": "discovery.validate",
        "profile_source": deployment.profile_source,
        **_svc_validate_discovery(
            _repo_root(getattr(args, "repo_root", None)), profile=deployment.profile
        ),
    }
    return _emit(args, payload)


def handle_discovery_publish(args: Any) -> int:
    context = _svc_context(args, "discovery", "discovery.publish")
    result = _svc_publish_discovery(
        context,
        output_dir=Path(getattr(args, "output", None)).resolve()
        if getattr(args, "output", None)
        else None,
    )
    return _svc_emit(args, result)


def handle_discovery_diff(args: Any) -> int:
    deployment = _resolved_from_args(args)
    payload = {
        "command": "discovery.diff",
        "profile_source": deployment.profile_source,
        **_svc_diff_discovery(
            _repo_root(getattr(args, "repo_root", None)),
            left_profile=getattr(args, "left_profile", None) or deployment.profile,
            right_profile=getattr(args, "right_profile", None),
        ),
    }
    return _emit(args, payload)
