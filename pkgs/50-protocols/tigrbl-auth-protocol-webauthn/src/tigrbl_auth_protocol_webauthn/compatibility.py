from .features import features_for
from .versions import WebAuthnVersion


def compatible_features(
    source: WebAuthnVersion | str, target: WebAuthnVersion | str
) -> frozenset:
    return features_for(source).intersection(features_for(target))


__all__ = ["compatible_features"]
