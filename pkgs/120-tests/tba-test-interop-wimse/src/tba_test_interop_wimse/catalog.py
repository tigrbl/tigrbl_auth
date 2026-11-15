"""Load and validate interop inputs."""
from importlib.resources import files

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


def read_catalog(filename):
    with files(__package__).joinpath(filename).open("rb") as source:
        data = tomllib.load(source)
    if data.get("schema_version") != 1:
        raise ValueError(f"Unsupported schema in {filename}")
    return data


def validate_catalog(factors, scenarios, exclusions):
    for key, factor in factors["factors"].items():
        levels = factor["levels"]
        if not levels or len(levels) != len(set(levels)):
            raise ValueError(f"Empty or duplicate levels in {key}")
    profiles = factors["hop_profiles"]
    for name, profile in profiles.items():
        for key in ("tls", "application_proof"):
            if profile[key] not in factors["factors"][key]["levels"]:
                raise ValueError(f"Unknown {key} in {name}")
    families = {}
    for family in scenarios["scenarios"]:
        identifier = family["id"]
        selected = family["profiles"]
        if identifier in families or not selected or not set(selected) <= profiles.keys():
            raise ValueError(f"Duplicate family or invalid profiles in {identifier}")
        variants = set()
        for variant in family["variants"]:
            key = variant["id"]
            hops = variant.get("hops", family["hops"])
            layers = variant.get("layers", ["operation"])
            if (key in variants or not hops or len(hops) != len(set(hops))
                    or variant.get("target", hops[-1]) not in hops
                    or not layers or not set(layers) <= {"tls", "application", "operation"}):
                raise ValueError(f"Invalid variant or hop in {identifier}/{key}")
            variants.add(key)
        if not variants:
            raise ValueError(f"No variants in {identifier}")
        families[identifier] = variants
    for rule in exclusions.get("trace_exclusions", []):
        if not rule["variants"] or not set(rule["variants"]) <= families.get(rule["scenario_id"], set()):
            raise ValueError(f"Unknown variant in {rule['id']}")


def validate_fixture_manifest(manifest, families, profiles):
    covered = set()
    for section in ("local", "peer"):
        for name, binding in manifest[section].items():
            if (binding["profile"] not in profiles or not binding["observations"]
                    or not set(binding["families"]) <= families):
                raise ValueError(f"Invalid fixture binding {name}")
            covered.update(binding["families"])
    unbound = set(manifest["unbound"]["families"])
    if covered & unbound or covered | unbound != families:
        raise ValueError("Fixture manifest must account for every family")
