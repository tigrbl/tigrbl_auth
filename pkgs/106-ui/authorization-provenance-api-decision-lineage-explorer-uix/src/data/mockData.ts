import { DecisionRecord } from '../types';

export const mockDecisions: DecisionRecord[] = [
  {
    id: 'dec_01HQ7K9X8M5V2Z3F4G6H8J9K',
    decisionKey: 'key_perm_std_v1',
    timestamp: '2023-10-25T14:32:01Z',
    tenant: 'corp-finance',
    subject: { id: 'usr_sarah_connor', type: 'user', name: 'Sarah Connor' },
    resource: { id: 'rep_q3_earnings', type: 'report', name: 'Q3 Earnings Draft' },
    action: 'read',
    effect: 'permit',
    policyVersion: 'pol_v2.4.1',
    engineVersion: 'pdp_core_1.9.0',
    reason: 'Explicitly allowed by role assignment: Finance Auditor',
    integritySeal: 'valid',
    replayable: true,
    facts: [
      { id: 'fct_1', type: 'role_assignment', source: 'identity_svc', version: 'v12', freshness: 'fresh', observedAt: '2023-10-25T14:30:00Z', value: { role: 'Finance Auditor' } },
      { id: 'fct_2', type: 'document_classification', source: 'content_svc', version: 'v3', freshness: 'fresh', observedAt: '2023-10-25T14:31:00Z', value: { level: 'confidential' } }
    ],
    steps: [
      { id: 'stp_1', ruleId: 'rule_deny_unauth', evaluator: 'RBAC', outcome: 'not_matched', durationMs: 2 },
      { id: 'stp_2', ruleId: 'rule_permit_auditor', evaluator: 'RBAC', outcome: 'matched', durationMs: 4 }
    ],
    obligations: [
      { id: 'obl_1', type: 'audit_log', status: 'fulfilled', description: 'Log sensitive read access' }
    ],
    enforcement: { id: 'enf_1', pepId: 'api_gw_east', status: 'enforced', timestamp: '2023-10-25T14:32:02Z' }
  },
  {
    id: 'dec_01HQ7KB4X9M2C3V4B5N6M7L',
    decisionKey: 'key_deny_geo_v1',
    timestamp: '2023-10-25T15:10:44Z',
    tenant: 'corp-engineering',
    subject: { id: 'usr_john_doe', type: 'user', name: 'John Doe' },
    resource: { id: 'srv_prod_db_main', type: 'database', name: 'Production DB Main' },
    action: 'delete',
    effect: 'deny',
    policyVersion: 'pol_v2.4.1',
    engineVersion: 'pdp_core_1.9.0',
    reason: 'Denied by explicit sovereignty constraint: Action not allowed from current region.',
    integritySeal: 'valid',
    replayable: true,
    facts: [
      { id: 'fct_3', type: 'network_origin', source: 'network_svc', version: 'v1', freshness: 'fresh', observedAt: '2023-10-25T15:10:40Z', value: { region: 'ap-south-1' } },
      { id: 'fct_4', type: 'resource_residency', source: 'infra_svc', version: 'v4', freshness: 'fresh', observedAt: '2023-10-25T15:10:00Z', value: { region: 'us-east-1' } }
    ],
    steps: [
      { id: 'stp_3', ruleId: 'rule_deny_cross_region_mutation', evaluator: 'ABAC', outcome: 'matched', durationMs: 8 },
      { id: 'stp_4', ruleId: 'rule_permit_db_admin', evaluator: 'RBAC', outcome: 'short_circuited', durationMs: 0 }
    ],
    obligations: [],
    enforcement: { id: 'enf_2', pepId: 'db_proxy', status: 'enforced', timestamp: '2023-10-25T15:10:45Z' }
  },
  {
    id: 'dec_01HQ7KC9X2M4V5B6N7M8L9K',
    decisionKey: 'key_perm_delegated_v1',
    timestamp: '2023-10-26T09:15:22Z',
    tenant: 'corp-sales',
    subject: { id: 'svc_crm_sync', type: 'service_account', name: 'CRM Sync Bot', delegatedFrom: 'usr_alice_manager' },
    resource: { id: 'api_customer_records', type: 'api_endpoint', name: 'Customer Records API' },
    action: 'write',
    effect: 'permit',
    policyVersion: 'pol_v2.4.2',
    engineVersion: 'pdp_core_1.9.0',
    reason: 'Permit via verified delegation grant from Alice Manager.',
    integritySeal: 'valid',
    replayable: true,
    facts: [
      { id: 'fct_5', type: 'delegation_grant', source: 'trust_registry', version: 'v89', freshness: 'fresh', observedAt: '2023-10-26T09:15:00Z', value: { delegator: 'usr_alice_manager', scope: 'write:customers', expiresAt: '2023-10-27T00:00:00Z' } }
    ],
    steps: [
      { id: 'stp_5', ruleId: 'rule_verify_delegation_chain', evaluator: 'TrustEngine', outcome: 'matched', durationMs: 12 },
      { id: 'stp_6', ruleId: 'rule_permit_delegated_action', evaluator: 'ABAC', outcome: 'matched', durationMs: 5 }
    ],
    obligations: [],
    enforcement: { id: 'enf_3', pepId: 'api_gw_west', status: 'enforced', timestamp: '2023-10-26T09:15:23Z' }
  },
  {
    id: 'dec_01HQ7KD4X8M2C3V4B5N6M7L',
    decisionKey: 'key_deny_stale_fact',
    timestamp: '2023-10-26T11:05:10Z',
    tenant: 'corp-hr',
    subject: { id: 'usr_bob_intern', type: 'user', name: 'Bob Intern' },
    resource: { id: 'doc_payroll_summary', type: 'document', name: 'Payroll Summary 2023' },
    action: 'read',
    effect: 'deny',
    policyVersion: 'pol_v2.4.2',
    engineVersion: 'pdp_core_1.9.0',
    reason: 'Denied due to stale clearance fact exceeding maximum allowed cache age (300s).',
    integritySeal: 'valid',
    replayable: false,
    facts: [
      { id: 'fct_6', type: 'security_clearance', source: 'hr_system', version: 'v1', freshness: 'stale', observedAt: '2023-10-26T10:00:00Z', value: { level: 'L1' } }
    ],
    steps: [
      { id: 'stp_7', ruleId: 'rule_require_fresh_clearance', evaluator: 'ABAC', outcome: 'failed', durationMs: 3 }
    ],
    obligations: [],
    enforcement: { id: 'enf_4', pepId: 'doc_viewer_app', status: 'enforced', timestamp: '2023-10-26T11:05:11Z' }
  },
  {
    id: 'dec_01HQ7KF8X9M2C3V4B5N6M7L',
    decisionKey: 'key_perm_enf_mismatch',
    timestamp: '2023-10-26T14:22:00Z',
    tenant: 'corp-finance',
    subject: { id: 'usr_eve_trader', type: 'user', name: 'Eve Trader' },
    resource: { id: 'api_trade_exec', type: 'api_endpoint', name: 'Trade Execution API' },
    action: 'execute',
    effect: 'permit',
    policyVersion: 'pol_v2.4.2',
    engineVersion: 'pdp_core_1.9.0',
    reason: 'Explicitly allowed by role, but enforcement receipt indicates application failed to execute.',
    integritySeal: 'valid',
    replayable: true,
    facts: [
      { id: 'fct_7', type: 'role_assignment', source: 'identity_svc', version: 'v55', freshness: 'fresh', observedAt: '2023-10-26T14:20:00Z', value: { role: 'Senior Trader' } },
      { id: 'fct_8', type: 'trading_hours', source: 'market_svc', version: 'v1', freshness: 'fresh', observedAt: '2023-10-26T14:21:00Z', value: { status: 'open' } }
    ],
    steps: [
      { id: 'stp_8', ruleId: 'rule_permit_trading_hours', evaluator: 'ABAC', outcome: 'matched', durationMs: 6 }
    ],
    obligations: [
      { id: 'obl_2', type: 'record_trade', status: 'pending', description: 'Record trade details to compliance ledger' }
    ],
    enforcement: { id: 'enf_5', pepId: 'trade_gw', status: 'mismatch', timestamp: '2023-10-26T14:22:05Z' }
  }
];

export const getDashboardStats = () => ({
  totalDecisions: 1245000,
  permitRate: 88.5,
  denyRate: 11.2,
  indeterminateRate: 0.3,
  provenanceCoverage: 99.8,
  enforcementMatchRate: 98.2,
  avgLatencyMs: 14.5
});
