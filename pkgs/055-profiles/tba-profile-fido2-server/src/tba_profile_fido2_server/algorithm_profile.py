REQUIRED_ALGORITHMS = (-7,)
RECOMMENDED_ALGORITHMS = (-7, -8, -257)


def algorithm_is_profiled(algorithm: int) -> bool:
    return algorithm in RECOMMENDED_ALGORITHMS


__all__ = ["RECOMMENDED_ALGORITHMS", "REQUIRED_ALGORITHMS", "algorithm_is_profiled"]
