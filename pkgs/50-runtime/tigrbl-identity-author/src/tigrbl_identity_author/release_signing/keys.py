from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, load_pem_private_key

from .models import LoadedSigner, SignerIdentity
from .utils import DEFAULT_SIGNER_ID, sha256_text


def _public_key_manifest(private_key: Ed25519PrivateKey, *, signer_id: str, source: str) -> SignerIdentity:
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo).decode("utf-8")
    public_sha = sha256_text(public_pem)
    key_id = f"ed25519:{public_sha[:24]}"
    return SignerIdentity(
        signer_id=signer_id,
        key_id=key_id,
        public_key_pem=public_pem,
        public_key_sha256=public_sha,
        source=source,
    )


def _load_private_key_from_pem(pem: str) -> Ed25519PrivateKey:
    key = load_pem_private_key(pem.encode("utf-8"), password=None)
    if not isinstance(key, Ed25519PrivateKey):
        raise TypeError("release signing key must be an Ed25519 private key")
    return key


def _private_key_from_material(signing_key: str | None) -> tuple[Ed25519PrivateKey, str]:
    env_file = os.environ.get("TIGRBL_AUTH_RELEASE_SIGNING_KEY_FILE")
    env_pem = os.environ.get("TIGRBL_AUTH_RELEASE_SIGNING_KEY_PEM")
    env_seed = os.environ.get("TIGRBL_AUTH_RELEASE_SIGNING_SEED")
    material = signing_key or env_pem
    if env_file and not signing_key and not env_pem:
        pem = Path(env_file).read_text(encoding="utf-8")
        return _load_private_key_from_pem(pem), f"file:{env_file}"
    if material:
        if "BEGIN PRIVATE KEY" in material:
            return _load_private_key_from_pem(material), "inline-pem"
        maybe_path = Path(material)
        if maybe_path.exists() and maybe_path.is_file():
            pem = maybe_path.read_text(encoding="utf-8")
            return _load_private_key_from_pem(pem), f"file:{maybe_path}"
        seed = hashlib.sha256(material.encode("utf-8")).digest()
        return Ed25519PrivateKey.from_private_bytes(seed), "derived-inline-secret"
    if env_seed:
        seed = hashlib.sha256(env_seed.encode("utf-8")).digest()
        return Ed25519PrivateKey.from_private_bytes(seed), "derived-env-seed"
    return Ed25519PrivateKey.generate(), "generated-ephemeral-checkpoint-key"


def load_signer(*, signing_key: str | None = None, signer_id: str | None = None) -> LoadedSigner:
    private_key, source = _private_key_from_material(signing_key)
    identity = _public_key_manifest(private_key, signer_id=signer_id or os.environ.get("TIGRBL_AUTH_RELEASE_SIGNER_ID", DEFAULT_SIGNER_ID), source=source)
    return LoadedSigner(private_key=private_key, identity=identity)


def write_public_key_artifacts(bundle_root: Path, signer: LoadedSigner) -> dict[str, str]:
    attest_root = bundle_root / "attestations"
    key_dir = attest_root / "keys"
    key_dir.mkdir(parents=True, exist_ok=True)
    public_key_path = key_dir / f"{signer.identity.key_id.replace(':', '-')}.pub.pem"
    public_key_path.write_text(signer.identity.public_key_pem, encoding="utf-8")
    signer_identity_path = attest_root / "signer-identity.json"
    signer_identity_path.write_text(json.dumps(signer.identity.to_manifest(), indent=2) + "\n", encoding="utf-8")
    return {
        "public_key_path": str(public_key_path.relative_to(bundle_root)).replace("\\", "/"),
        "signer_identity_path": str(signer_identity_path.relative_to(bundle_root)).replace("\\", "/"),
    }
