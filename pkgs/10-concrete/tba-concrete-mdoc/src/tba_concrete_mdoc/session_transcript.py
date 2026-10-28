from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SessionTranscript:
    device_engagement_bytes: bytes | None
    reader_key_bytes: bytes | None
    handover: object


__all__ = ["SessionTranscript"]
