_EVALUATION = frozenset({"access-evaluation"})
_BATCH = _EVALUATION | {"access-evaluations"}
_SEARCH = _BATCH | {"search-subject", "search-resource", "search-action"}
_DISCOVERY = _SEARCH | {"configuration", "capabilities", "signed-metadata"}

FEATURES_BY_VERSION = {
    "draft-00": _EVALUATION,
    "draft-01": _EVALUATION,
    "implementers-draft-1": _EVALUATION,
    "draft-02": _BATCH,
    "draft-03": _SEARCH,
    "draft-04": _DISCOVERY,
    "draft-05": _DISCOVERY,
    "1.0": _DISCOVERY,
}


def supports(feature: str, version: str = "1.0") -> bool:
    try:
        return feature in FEATURES_BY_VERSION[version]
    except KeyError as exc:
        raise ValueError(f"unsupported AuthZEN version: {version}") from exc


__all__ = ["FEATURES_BY_VERSION", "supports"]
