from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SecuredVcFormat:
    media_type: str
    artifact_kind: str
    envelope_family: str


FORMATS = {
    "application/vc+jwt": SecuredVcFormat(
        "application/vc+jwt",
        "credential",
        "JOSE",
    ),
    "application/vc+cose": SecuredVcFormat(
        "application/vc+cose",
        "credential",
        "COSE",
    ),
}


def select_format(media_type: str) -> SecuredVcFormat:
    try:
        return FORMATS[media_type]
    except KeyError as exc:
        raise ValueError(f"unsupported VC-JOSE-COSE media type: {media_type}") from exc
