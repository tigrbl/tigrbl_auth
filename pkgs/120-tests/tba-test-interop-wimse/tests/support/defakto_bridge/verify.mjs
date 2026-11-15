import { X509Certificate } from "node:crypto";
import { readFileSync } from "node:fs";
import { SpiffeID, verifyX509SVID } from "@defakto/spiffe";

try {
  const { certificate, anchor, expected } = JSON.parse(readFileSync(0, "utf8"));
  const { trustDomain } = SpiffeID.parse(expected);
  const bundle = {
    trustDomain,
    x509Authorities: [new X509Certificate(readFileSync(anchor))],
  };
  const identity = await verifyX509SVID([Buffer.from(certificate, "base64")], {
    async getBundleForTrustDomain(domain) {
      if (domain.toString() !== trustDomain.toString()) {
        throw new Error("untrusted SPIFFE domain");
      }
      return bundle;
    },
  });
  if (identity.toString() !== expected) {
    throw new Error("unexpected SPIFFE peer identity");
  }
  process.stdout.write(JSON.stringify(identity.toString()));
} catch (error) {
  process.stderr.write(error.message);
  process.exitCode = 1;
}
