export type TransportPostureRecord = {
  protocol: 'http11' | 'http2' | 'http3' | 'quic';
  backend_runtime_support: 'implemented' | 'absent';
  runtime_enablement: string;
  contract_visibility: string;
  uix_dependency: string;
  certification_claimable: boolean;
  supported_runners: string[];
  enablement_flags: string[];
};

export type DisclosureRuleRecord = {
  artifact_kind: 'json-schema' | 'jws' | 'jwe' | 'jwt' | 'jwks';
  admin_rendering: string;
  public_rendering: string;
  redacted_fields: string[];
  implementation_only_fields: string[];
};

export type ProvenanceRequirementRecord = {
  standard: 'ssdf' | 'slsa' | 'in-toto' | 'sigstore' | 'spdx' | 'cyclonedx';
  required_artifact_paths: string[];
  generated_projection_paths: string[];
  release_gate_obligations: string[];
  disclosure_paths: string[];
  satisfied: boolean;
  missing_paths: string[];
};

export type Phase6ReleaseClosureSummary = {
  transport: {
    implemented_protocols: string[];
    claimable_protocols: string[];
    upgrade_protocols: string[];
    missing_protocols: string[];
  };
  disclosure: {
    artifact_kinds: string[];
    admin_renderings: string[];
    public_renderings: string[];
    redacted_field_count: number;
    implementation_only_count: number;
  };
  provenance: {
    standards: string[];
    satisfied_standards: string[];
    missing_standards: string[];
    release_gate_obligations: string[];
    disclosure_path_count: number;
  };
};

export const summarizeTransportPosture = (records: TransportPostureRecord[]) => {
  return {
    implemented_protocols: records
      .filter((record) => record.backend_runtime_support === 'implemented')
      .map((record) => record.protocol)
      .sort(),
    claimable_protocols: records
      .filter((record) => record.certification_claimable)
      .map((record) => record.protocol)
      .sort(),
    upgrade_protocols: records
      .filter((record) => record.enablement_flags.length > 0)
      .map((record) => record.protocol)
      .sort(),
    missing_protocols: records
      .filter((record) => record.backend_runtime_support !== 'implemented')
      .map((record) => record.protocol)
      .sort(),
  };
};

export const summarizeDisclosureBoundaries = (records: DisclosureRuleRecord[]) => {
  return {
    artifact_kinds: records.map((record) => record.artifact_kind).sort(),
    admin_renderings: records.map((record) => record.admin_rendering).sort(),
    public_renderings: records.map((record) => record.public_rendering).sort(),
    redacted_field_count: records.reduce((total, record) => total + record.redacted_fields.length, 0),
    implementation_only_count: records.reduce((total, record) => total + record.implementation_only_fields.length, 0),
  };
};

export const summarizeReleaseProvenance = (records: ProvenanceRequirementRecord[]) => {
  return {
    standards: records.map((record) => record.standard).sort(),
    satisfied_standards: records
      .filter((record) => record.satisfied)
      .map((record) => record.standard)
      .sort(),
    missing_standards: records
      .filter((record) => !record.satisfied)
      .map((record) => record.standard)
      .sort(),
    release_gate_obligations: [...new Set(records.flatMap((record) => record.release_gate_obligations))].sort(),
    disclosure_path_count: records.reduce((total, record) => total + record.disclosure_paths.length, 0),
  };
};

export const buildPhase6ReleaseClosureSummary = ({
  transport,
  disclosure,
  provenance,
}: {
  transport: TransportPostureRecord[];
  disclosure: DisclosureRuleRecord[];
  provenance: ProvenanceRequirementRecord[];
}): Phase6ReleaseClosureSummary => {
  return {
    transport: summarizeTransportPosture(transport),
    disclosure: summarizeDisclosureBoundaries(disclosure),
    provenance: summarizeReleaseProvenance(provenance),
  };
};
