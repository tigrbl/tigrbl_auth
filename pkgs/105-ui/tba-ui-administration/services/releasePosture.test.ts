import { describe, expect, it } from 'vitest';

import {
  buildPhase6ReleaseClosureSummary,
  summarizeDisclosureBoundaries,
  summarizeReleaseProvenance,
  summarizeTransportPosture,
  type DisclosureRuleRecord,
  type ProvenanceRequirementRecord,
  type TransportPostureRecord,
} from './releasePosture';

const transport: TransportPostureRecord[] = [
  {
    protocol: 'http11',
    backend_runtime_support: 'implemented',
    runtime_enablement: 'baseline runner transport',
    contract_visibility: 'indirect via deployment and runtime profile',
    uix_dependency: 'required browser transport baseline',
    certification_claimable: true,
    supported_runners: ['hypercorn', 'tigrcorn', 'uvicorn'],
    enablement_flags: [],
  },
  {
    protocol: 'http2',
    backend_runtime_support: 'implemented',
    runtime_enablement: 'opt-in runner flag where the adapter exposes HTTP/2',
    contract_visibility: 'indirect via runtime profile and operator configuration',
    uix_dependency: 'optional browser transport upgrade',
    certification_claimable: true,
    supported_runners: ['hypercorn'],
    enablement_flags: ['hypercorn_http2'],
  },
  {
    protocol: 'http3',
    backend_runtime_support: 'absent',
    runtime_enablement: 'not implemented in the current runner registry',
    contract_visibility: 'not declared in current OpenAPI or OpenRPC contracts',
    uix_dependency: 'no current UIX dependency',
    certification_claimable: false,
    supported_runners: [],
    enablement_flags: [],
  },
  {
    protocol: 'quic',
    backend_runtime_support: 'absent',
    runtime_enablement: 'not implemented in the current runner registry',
    contract_visibility: 'not declared in current OpenAPI or OpenRPC contracts',
    uix_dependency: 'no current UIX dependency',
    certification_claimable: false,
    supported_runners: [],
    enablement_flags: [],
  },
];

const disclosure: DisclosureRuleRecord[] = [
  {
    artifact_kind: 'json-schema',
    admin_rendering: 'schema field summary with sensitive examples removed',
    public_rendering: 'field list and requirement summary only',
    redacted_fields: ['default', 'examples', '$comment'],
    implementation_only_fields: ['$defs', 'unevaluatedProperties', 'x-internal'],
  },
  {
    artifact_kind: 'jws',
    admin_rendering: 'header and redacted claims with signature presence only',
    public_rendering: 'algorithm and claim-name summary without token material',
    redacted_fields: ['signature', 'client_secret', 'assertion'],
    implementation_only_fields: ['compact_token', 'raw_signature_bytes'],
  },
  {
    artifact_kind: 'jwe',
    admin_rendering: 'protected header and encrypted payload placeholder only',
    public_rendering: 'encryption status and header summary only',
    redacted_fields: ['ciphertext', 'encrypted_key', 'iv', 'tag'],
    implementation_only_fields: ['decrypted_payload', 'cek'],
  },
  {
    artifact_kind: 'jwt',
    admin_rendering: 'registered claims with secret-bearing values redacted',
    public_rendering: 'claim-name summary and bounded identity hints only',
    redacted_fields: ['access_token', 'authorization_details', 'refresh_token'],
    implementation_only_fields: ['raw_token', 'signature_material'],
  },
  {
    artifact_kind: 'jwks',
    admin_rendering: 'public key metadata only',
    public_rendering: 'key identifiers and public key-type summary only',
    redacted_fields: ['d', 'dp', 'dq', 'k', 'oth', 'p', 'q', 'qi'],
    implementation_only_fields: ['private_jwk_material', 'rotation_private_cache'],
  },
];

const provenance: ProvenanceRequirementRecord[] = [
  {
    standard: 'ssdf',
    required_artifact_paths: ['docs/runbooks/CLEAN_CHECKOUT_REPRO.md'],
    generated_projection_paths: ['docs/compliance/validated_execution_report.json'],
    release_gate_obligations: ['gate-21-repro-clean-room', 'gate-24-ci-install-profiles'],
    disclosure_paths: ['docs/compliance/validated_execution_report.md'],
    satisfied: true,
    missing_paths: [],
  },
  {
    standard: 'slsa',
    required_artifact_paths: ['uv.lock'],
    generated_projection_paths: ['docs/compliance/final_release_gate_report.json'],
    release_gate_obligations: ['gate-90-release'],
    disclosure_paths: ['docs/compliance/final_release_gate_report.md'],
    satisfied: true,
    missing_paths: [],
  },
  {
    standard: 'in-toto',
    required_artifact_paths: ['docs/compliance/release_signing_report.json'],
    generated_projection_paths: ['docs/compliance/release_signing_report.md'],
    release_gate_obligations: ['gate-87-peer-bundle-completeness'],
    disclosure_paths: ['docs/compliance/release_signing_report.md'],
    satisfied: true,
    missing_paths: [],
  },
];

describe('releasePosture', () => {
  it('summarizes transport posture across supported and missing protocols', () => {
    expect(summarizeTransportPosture(transport)).toEqual({
      implemented_protocols: ['http11', 'http2'],
      claimable_protocols: ['http11', 'http2'],
      upgrade_protocols: ['http2'],
      missing_protocols: ['http3', 'quic'],
    });
  });

  it('summarizes UIX disclosure boundaries and redaction counts', () => {
    expect(summarizeDisclosureBoundaries(disclosure)).toEqual({
      artifact_kinds: ['json-schema', 'jwe', 'jwks', 'jws', 'jwt'],
      admin_renderings: [
        'header and redacted claims with signature presence only',
        'protected header and encrypted payload placeholder only',
        'public key metadata only',
        'registered claims with secret-bearing values redacted',
        'schema field summary with sensitive examples removed',
      ],
      public_renderings: [
        'algorithm and claim-name summary without token material',
        'claim-name summary and bounded identity hints only',
        'encryption status and header summary only',
        'field list and requirement summary only',
        'key identifiers and public key-type summary only',
      ],
      redacted_field_count: 21,
      implementation_only_count: 11,
    });
  });

  it('summarizes release provenance requirements and gate obligations', () => {
    expect(summarizeReleaseProvenance(provenance)).toEqual({
      standards: ['in-toto', 'slsa', 'ssdf'],
      satisfied_standards: ['in-toto', 'slsa', 'ssdf'],
      missing_standards: [],
      release_gate_obligations: [
        'gate-21-repro-clean-room',
        'gate-24-ci-install-profiles',
        'gate-87-peer-bundle-completeness',
        'gate-90-release',
      ],
      disclosure_path_count: 3,
    });
  });

  it('builds the combined Phase 6 closure summary', () => {
    const summary = buildPhase6ReleaseClosureSummary({ transport, disclosure, provenance });

    expect(summary.transport.upgrade_protocols).toEqual(['http2']);
    expect(summary.disclosure.artifact_kinds).toEqual(['json-schema', 'jwe', 'jwks', 'jws', 'jwt']);
    expect(summary.provenance.satisfied_standards).toEqual(['in-toto', 'slsa', 'ssdf']);
  });
});
