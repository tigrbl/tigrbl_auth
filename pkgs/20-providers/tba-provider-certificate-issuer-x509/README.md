# tba-provider-certificate-issuer-x509

Create an `X509CertificateIssuer` from `X509IssuerConfig`, then call
`issue_certificate(CertificateRequest(op="issue_certificate", ...))`.

The signed CSR supplies the public key. The trusted caller supplies the subject
and SANs. The `san` mapping recognizes `dns`, `uri`, `email`, and `ip`.
Optional extensions map dotted OIDs to `(x509.ExtensionType, critical)` pairs.
The issuer supplies the CA identity, Basic Constraints, and key identifiers.
The result is an `Artifact` containing a PEM or DER leaf certificate.
