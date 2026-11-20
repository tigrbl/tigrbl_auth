from collections.abc import Sequence

VCDM_2_RECOMMENDATION = "W3C Recommendation 15 May 2025"
VC_CONTEXT_V2 = "https://www.w3.org/ns/credentials/v2"


def validate_contexts(contexts: object) -> tuple[object, ...]:
    if (
        not isinstance(contexts, Sequence)
        or isinstance(contexts, (str, bytes))
        or not contexts
    ):
        raise ValueError("@context must be a non-empty array")
    if contexts[0] != VC_CONTEXT_V2:
        raise ValueError("VCDM 2.0 base context must be first")
    if any(not isinstance(context, (str, dict)) for context in contexts):
        raise ValueError("contexts must be URLs or context objects")
    return tuple(contexts)


__all__ = ["VCDM_2_RECOMMENDATION", "VC_CONTEXT_V2", "validate_contexts"]
