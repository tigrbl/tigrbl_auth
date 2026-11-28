export type EvidenceSourceState =
  | 'draft'
  | 'active'
  | 'degraded'
  | 'suspended'
  | 'revoked'
  | 'expired'
  | 'deleted';

export type PolicyAction = 'Allow' | 'Step-Up' | 'Deny';

export type Granularity = 'precise' | 'coarse' | 'zone' | 'none';

export interface LocationSource {
  id: string;
  name: string;
  type: 'device' | 'network' | 'enterprise_zone' | 'trusted_upstream' | 'managed_posture';
  state: EvidenceSourceState;
  priority: number;
  accuracyThreshold: number; // in meters
  freshnessLimit: number; // in minutes
  lastValidated: string;
}

export interface ZonePolicy {
  id: string;
  name: string;
  description: string;
  action: PolicyAction;
  freshnessLimit: number; // in minutes
  accuracyRequired: number; // in meters
  allowedCIDRs: string[];
  bounds?: {
    lat: number;
    lng: number;
    radius: number; // in meters
  };
  isActive: boolean;
}

export interface AuditRecord {
  id: string;
  timestamp: string;
  userEmail: string;
  sourceType: string;
  granularity: Granularity;
  policyName: string;
  policyVersion: string;
  decision: PolicyAction;
  deviceOS: string;
  accuracy: number;
  isStale: boolean;
  spoofSuspected: boolean;
  providerStatus: 'healthy' | 'degraded' | 'offline';
  auditReference: string;
  fallbackUsed?: string;
}

export interface SimulationProfile {
  id: string;
  name: string;
  description: string;
  lat: number;
  lng: number;
  accuracy: number; // in meters
  ipAddress: string;
  isp: string;
  vpnActive: boolean;
  mockLocationActive: boolean;
  providerStatus: 'healthy' | 'degraded' | 'offline';
  permissionGranted: boolean;
  deviceOS: 'macOS' | 'iOS' | 'Windows' | 'Android' | 'Linux';
}

export interface ProviderHealth {
  id: string;
  name: string;
  type: 'IP' | 'GPS' | 'VPC' | 'Posture';
  latency: number; // ms
  errorRate: number; // %
  lastSync: string;
  datasetVersion: string;
  status: 'healthy' | 'degraded' | 'offline';
}
