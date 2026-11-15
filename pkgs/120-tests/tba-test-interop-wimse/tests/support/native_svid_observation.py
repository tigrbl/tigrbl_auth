"""Capture the credential fingerprints seen by actual native receivers."""

from hashlib import sha256

from tba_concrete_jwt import decode_jwt_unverified


def observe_svids(receiver, hop):
    observed = {}
    if hop["wic_issuer"] == "tba-x509-svid":
        verifier = receiver.verifier if hop["profile"] == "wic-mtls" else receiver.client_verifier
        verify = verifier.verify

        def observe_certificate(certificate, **options):
            evidence = {"sha256": sha256(certificate).hexdigest(), "verified": False}
            observed["tba-x509-svid"] = evidence
            identity = verify(certificate, **options)
            evidence.update(verified=True, identity=identity)
            return identity

        verifier.verify = observe_certificate
    if hop["wit_issuer"] == "tba-wit-svid":
        authenticate = receiver.authenticate_proof

        def observe_proof(request, path):
            serialized = request.headers["Workload-Identity-Token"]
            token = decode_jwt_unverified(serialized)
            headers = token.jws.protected_headers
            assert (headers["kid"], headers["typ"]) == ("tba-native-wit-svid", "wit+jwt")
            evidence = {"sha256": sha256(serialized.encode()).hexdigest(), "verified": False}
            observed["tba-wit-svid"] = evidence
            identity = authenticate(request, path)
            evidence.update(verified=True, identity=identity)
            return identity

        receiver.authenticate_proof = observe_proof
    return observed
