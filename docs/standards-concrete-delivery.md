# Identity Standards Concrete Delivery

This document records the first executable delivery across the repository's
layered package model. It distinguishes implemented structural capability from
full protocol or cryptographic conformance. A parser or contract is not, by
itself, a claim of standards certification.

## Layer-by-layer delivery

| Layer | Package | Additions and updates | Removals | Verification |
|---|---|---|---|---|
| 00 primitives | `tigrbl-identity-core` | Artifact, credential-format, token, presentation, attestation, manifest, lifecycle, verification, media-type, nonce, URI, digest, protocol-tag, and opaque identifier primitives | None | Primitive unit tests |
| 01 storage | `tigrbl-identity-storage` | No tables in this increment. Durable records are deliberately deferred until lifecycle and retention requirements are approved for credentials, presentations, attestations, manifests, SVID bundles, and protocol transactions. | None | No schema churn |
| 02 contracts | `tigrbl-identity-contracts` | Neutral assurance, credential/presentation, verifier, attestation/appraisal, workload identity/SVID, DID resolution, AuthZEN, and XACML adaptation contracts | None | Contract unit tests |
| 05 bases | `tigrbl-identity-model-bases` | Abstract issuer, presentation builder, and artifact verifier bases | None | Import and contract tests |
| 10 concrete | `tigrbl-oidc-claims-concrete` | Final EAP ACR/AMR vocabulary and Identity Assurance parsing/serialization | None | EAP hierarchy and verified-claims tests |
| 10 concrete | `tigrbl-identity-credentials-concrete` | VCDM 2.0 structural validation, SD-JWT VC compact parsing, ISO mdoc decoded-object parsing, EAT claims, and CoRIM/CoMID reference material | None | Positive and negative structure tests |
| 10 concrete | `tigrbl-set-concrete` | Correct RFC 8417 SET claims profile | Obsolete RFC 7952 SET test | RFC 8417 tests |
| 20 providers | Existing JOSE, trust, authenticator, and certificate providers | Reused as the future cryptographic/key/trust implementation boundary. No misleading format-specific provider was added before algorithms and trust policies are selected. | None | Existing provider suites remain authoritative |
| 50 protocols | `tigrbl-auth-protocol-oidc` | OID4VCI credential offers, OID4VP presentation requests, HAIP policy constraints, RFC 8935 SET push, and RFC 8936 SET poll contracts | None | Protocol structure tests |
| 50 protocols | `tigrbl-auth-protocol-oauth` | GNAP grant request structure | None | GNAP structure tests |
| 60 runtime | `tigrbl-identity-runtime` | RFC 8417 feature flag, settings, deployment defaults, and product-surface correction | RFC 7952 runtime flag name | Boundary tests |
| 60 runtime | `tigrbl-identity-cli` | RFC 8417 boundary and required-extension labels | RFC 7952 current boundary label | Generated boundary validation |
| Compliance | targets, mappings, claims, evidence, generated docs | Current SET target corrected to RFC 8417 and regenerated across primary claim/evidence mappings | Current RFC 7952-as-SET mapping | Generator and boundary checkpoint |

## Concrete object ownership

| Object | Kind | Owning layer/package | Provider/runtime still required |
|---|---|---|---|
| `VerifiedClaims` | assurance payload | 02 contracts | OIDC delivery and trust-framework policy |
| `CredentialArtifact` | credential representation | 02 contracts | issuer, key, status, schema, and trust providers |
| `PresentationArtifact` | holder-created presentation | 02 contracts | holder binding, verifier policy, replay storage |
| `SdJwtVc` | credential format | 10 credential concrete | JWS verification, disclosure digest checking, KB-JWT verification, status/schema/trust |
| `Mdoc` | credential/document format | 10 credential concrete | CBOR/COSE decoding, MSO validation, certificate path validation, device/session authentication |
| VCDM VC/VP | data-model objects | 10 credential concrete | selected securing mechanism, status, schema, controller/key resolution |
| EAT | attestation evidence token | 10 credential concrete | CWT/COSE or JWT verification and appraisal policy |
| CoRIM/CoMID | signed reference integrity material | 10 credential concrete | COSE verification, reference-value selection, appraisal engine |
| `SpiffeId` | workload identity | 02 contracts | Workload API and trust-bundle provider |
| `Svid` | workload credential | 02 contracts | X.509/JWT validation and rotation provider |
| SET | event token | 10 SET concrete | JOSE signer/verifier and replay/delivery persistence |
| DID | identifier | 02 contracts | method-specific resolver providers |
| AuthZEN request/response | policy wire object | 02 contracts | PDP provider and protocol endpoint |
| XACML decision | policy decision object | 02 contracts | XML/JSON profile parser and PDP adapter |
| GNAP request | grant transaction object | 50 OAuth protocol | continuation, interaction, proof, token, and resource-server runtime |

## Intentional storage deferral

The 01 layer was not expanded speculatively. The next storage migration should
add tables only for product-enabled lifecycles, likely:

- credential issuance transactions and deferred/batch state;
- presentation nonces, response correlation, replay decisions, and audit data;
- credential status and notification state;
- SET push/poll delivery acknowledgements and errors;
- attestation evidence/appraisal results where retention is permitted;
- SPIFFE bundles and SVID rotation metadata, never private key material;
- GNAP continuation and interaction state.

Presentation payloads, raw identity evidence, selective-disclosure source data,
and attestation evidence require explicit minimization, encryption, retention,
and deletion policies before persistence.

## What full conformance still requires

Each standards target still needs version-locked normative requirement
inventories, complete serializers/parsers, cryptographic and trust providers,
negative and interoperability vectors, replay/freshness/channel binding,
runtime endpoint behavior, discovery metadata, durable lifecycle state where
needed, privacy controls, operational documentation, and independent evidence.
The current delivery creates the correct package seams and executable
vocabulary without overstating that those later requirements are complete.
