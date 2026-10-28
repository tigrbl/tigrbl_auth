/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

export interface EnterpriseDomain {
  id: string;
  name: string;
  verified: boolean;
  trustType: 'bidirectional' | 'one-way-incoming' | 'one-way-outgoing' | 'none';
  kdcServer: string;
  mappedUsersCount: number;
  lastSync: string;
}

export interface ServicePrincipalName {
  id: string;
  spn: string;
  serviceAccount: string;
  realm: string;
  encryptionTypes: string[];
  delegationAllowed: boolean;
  delegationAllowlist: string[];
}

export interface BrowserPolicy {
  wiaEnabled: boolean;
  allowPrivateBrowsingWia: boolean;
  intranetZoneOnly: boolean;
  requireChannelBinding: boolean;
  extendedProtection: 'Off' | 'WhenSupported' | 'Required';
  supportedBrowsers: {
    browser: string;
    os: string;
    supported: boolean;
    policyStatus: 'Active' | 'Warning' | 'NotConfigured';
  }[];
}

export interface UserEnterpriseIdentity {
  id: string;
  upn: string; // User Principal Name, e.g. j.doe@corp.enterprise.local
  samAccountName: string; // e.g. CORP\jdoe
  sid: string; // Security Identifier, e.g. S-1-5-21-...
  displayName: string;
  email: string;
  domain: string;
  memberOf: string[];
  linkedAt?: string;
  status: 'active' | 'degraded' | 'suspended' | 'pending';
  assuranceLevel: 'Low' | 'Medium' | 'High';
  lastAuthEvidence?: {
    amr: string[];
    spnUsed: string;
    authTime: string;
    ticketFreshnessSeconds: number;
    channelBound: boolean;
  };
}

export interface SystemHealthMetric {
  kdcStatus: 'healthy' | 'degraded' | 'unreachable';
  dnsSrvStatus: 'healthy' | 'missing';
  clockDriftSeconds: number;
  keyAgeDays: number;
  replicationLagSeconds: number;
  conformanceStatus: 'passed' | 'failed' | 'warning';
}

export type SimMode =
  | 'success_auto' // Perfect automatic silent sign-in
  | 'success_prompt' // OS Prompts for Windows credentials
  | 'unsupported_browser' // Browser not in Intranet zone/unsupported
  | 'unmanaged_device' // Outside company corpnet
  | 'private_mode' // Private window restrictions
  | 'domain_mismatch' // Token domain is not verified/trusted
  | 'ambiguous_mapping' // AD token maps to multiple local accounts
  | 'account_denied' // AD Account is suspended/disabled
  | 'clock_skew' // Clock drift > 300 seconds
  | 'spn_failure' // SPN target server is incorrect or missing
  | 'trust_failure' // Realm trust invalid or expired
  | 'provider_timeout' // KDC times out
  | 'credential_replay' // Detected a replay attack
  | 'proxy_stripped'; // Proxy has stripped the Negotiate headers

export interface SimConfig {
  activeMode: SimMode;
  networkLatencyMs: number;
  browserType: 'Chrome_Managed' | 'Edge_Enterprise' | 'Firefox_Unmanaged' | 'Safari_Private' | 'Native_App';
  isCorpNetwork: boolean;
  systemClockOffsetSeconds: number;
  simulatePromptCancellation: boolean;
}

export interface AuditLog {
  id: string;
  timestamp: string;
  eventType: 'discovery' | 'negotiation' | 'token_validation' | 'account_link' | 'policy_update' | 'health_alert' | 'error';
  summary: string;
  details: string;
  actor: string;
  amr?: string[];
  status: 'success' | 'failure' | 'warning';
  ipAddress: string;
  userAgent: string;
}
