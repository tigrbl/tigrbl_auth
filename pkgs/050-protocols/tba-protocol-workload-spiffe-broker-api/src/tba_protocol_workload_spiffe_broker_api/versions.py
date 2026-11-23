from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BrokerApiVersion:
    identifier: str
    status: str
    specification_uri: str


CURRENT_VERSION = BrokerApiVersion(
    "SPIFFE-v1.15.1-Broker-API",
    "Incubating",
    "https://github.com/spiffe/spiffe/tree/v1.15.1",
)
VERSION_HISTORY = (CURRENT_VERSION,)
