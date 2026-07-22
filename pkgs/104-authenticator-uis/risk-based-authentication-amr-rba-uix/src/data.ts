import { 
  RiskSignal, 
  AuthMethod, 
  PolicyRule, 
  SimulationScenario, 
  ProviderHealth, 
  AuditLog,
  ActiveSession
} from './types';

// Initial Signal Definitions
export const INITIAL_SIGNALS: RiskSignal[] = [
  {
    id: 'sig_impossible_travel',
    name: 'Impossible Travel Detector',
    category: 'location',
    status: 'safe',
    value: '0.0 km/h (Last: Seattle, WA; Current: Seattle, WA)',
    source: 'GeoIP Correlation Engine v2.4',
    freshness: '3s ago',
    confidence: 98,
    privacyClass: 'restricted'
  },
  {
    id: 'sig_device_integrity',
    name: 'Hardware Attestation (Play Integrity / Secure Enclave)',
    category: 'device',
    status: 'safe',
    value: 'Strong Integrity & Basic Integrity Verified',
    source: 'OS Native Attestation Provider',
    freshness: '8s ago',
    confidence: 99,
    privacyClass: 'internal'
  },
  {
    id: 'sig_behavioral_typing',
    name: 'Keystroke & Mouse Dynamics',
    category: 'behavior',
    status: 'safe',
    value: '94% user behavioral match threshold',
    source: 'Continuous Behavioral Modality Engine',
    freshness: '1s ago',
    confidence: 85,
    privacyClass: 'redacted'
  },
  {
    id: 'sig_ip_reputation',
    name: 'IP Reputation Scoring',
    category: 'reputation',
    status: 'safe',
    value: 'Score: 0.02 (Low Risk, Residential IP)',
    source: 'Spamhaus & Webroot Intelligence Feed',
    freshness: '12s ago',
    confidence: 95,
    privacyClass: 'restricted'
  },
  {
    id: 'sig_network_vpn',
    name: 'Commercial VPN & Proxy Detection',
    category: 'network',
    status: 'safe',
    value: 'No proxy, VPN, or Tor node detected',
    source: 'MaxMind GeoIP2 Connection Type',
    freshness: '5s ago',
    confidence: 97,
    privacyClass: 'restricted'
  }
];

// Available authenticators for step-up ceremony
export const AUTHENTICATORS: AuthMethod[] = [
  {
    id: 'auth_passkey',
    name: 'FIDO2 WebAuthn Passkey',
    description: 'Cryptographic device credentials linked to FaceID, TouchID, or Hello.',
    icon: 'Fingerprint',
    category: 'inherence',
    enabled: true,
    ceremonySteps: ['Device Attestation', 'Biometric Authorization', 'Cryptographic Challenge Verification']
  },
  {
    id: 'auth_hardware_key',
    name: 'YubiKey Hardware Token',
    description: 'Physical USB/NFC security key providing high-assurance cryptographic proof.',
    icon: 'KeyRound',
    category: 'possession',
    enabled: true,
    ceremonySteps: ['Insert Security Key', 'Touch Physical Sensor', 'Verify Hardware Signature']
  },
  {
    id: 'auth_app_push',
    name: 'Secure Native App Push Notification',
    description: 'Approval request delivered directly to your verified, enrolled mobile app.',
    icon: 'Smartphone',
    category: 'possession',
    enabled: true,
    ceremonySteps: ['Generate Encrypted Push payload', 'Delivery confirmation to target device', 'User biometrics or PIN on device']
  },
  {
    id: 'auth_totp',
    name: 'Time-Based Authenticator Code (TOTP)',
    description: '6-digit rotating verification code from Google Authenticator, Authy, or 1Password.',
    icon: 'Clock',
    category: 'possession',
    enabled: true,
    ceremonySteps: ['Retrieve rotating 30s token', 'Submit OTP input', 'Drift evaluation check']
  },
  {
    id: 'auth_email_otp',
    name: 'Secure Link / Email One-Time Code',
    description: 'Out-of-band numeric passcode delivered to your primary verified email.',
    icon: 'Mail',
    category: 'knowledge',
    enabled: true,
    ceremonySteps: ['SMTP out-of-band dispatch', 'Retrieve 8-digit secure code', 'Verification of temporal token']
  },
  {
    id: 'auth_sms_otp',
    name: 'SMS One-Time Passcode',
    description: 'Fallback text message verification code. Susceptible to SIM swap risks.',
    icon: 'MessageSquare',
    category: 'possession',
    enabled: true,
    ceremonySteps: ['SMS provider dispatch', 'Retrieve numeric passcode', 'Submit challenge verification']
  }
];

// Initial Policy Rules Configured by Admin
export const INITIAL_POLICY_RULES: PolicyRule[] = [
  {
    id: 'rule_critical_compromise',
    name: 'Force Deny on Device Integrity Failure',
    riskLevel: 'critical',
    conditions: [
      { field: 'sig_device_integrity', operator: 'equals', value: 'compromised' }
    ],
    outcome: 'deny',
    eligibleMethods: [],
    fallbackMethod: 'auth_email_otp',
    freshnessThreshold: 60,
    missingSignalBehavior: 'fail-closed',
    enabled: true
  },
  {
    id: 'rule_impossible_travel_block',
    name: 'Account Lockout on Compromised Travel Vector',
    riskLevel: 'critical',
    conditions: [
      { field: 'sig_impossible_travel', operator: 'equals', value: 'compromised' }
    ],
    outcome: 'deny',
    eligibleMethods: [],
    fallbackMethod: 'auth_email_otp',
    freshnessThreshold: 30,
    missingSignalBehavior: 'fail-closed',
    enabled: true
  },
  {
    id: 'rule_suspicious_travel_stepup',
    name: 'Step-up Ceremony for Travel Anomalies',
    riskLevel: 'high',
    conditions: [
      { field: 'sig_impossible_travel', operator: 'equals', value: 'suspicious' }
    ],
    outcome: 'step-up',
    eligibleMethods: ['auth_passkey', 'auth_hardware_key', 'auth_app_push'],
    fallbackMethod: 'auth_email_otp',
    freshnessThreshold: 300,
    missingSignalBehavior: 'fail-closed',
    enabled: true
  },
  {
    id: 'rule_reputation_stepup',
    name: 'Multi-factor Step-up for Proxy & VPN presence',
    riskLevel: 'medium',
    conditions: [
      { field: 'sig_network_vpn', operator: 'equals', value: 'suspicious' }
    ],
    outcome: 'step-up',
    eligibleMethods: ['auth_passkey', 'auth_app_push', 'auth_totp'],
    fallbackMethod: 'auth_email_otp',
    freshnessThreshold: 600,
    missingSignalBehavior: 'step-up',
    enabled: true
  },
  {
    id: 'rule_unfamiliar_typing_review',
    name: 'Governed Administrative Review on Typing Anomaly',
    riskLevel: 'medium',
    conditions: [
      { field: 'sig_behavioral_typing', operator: 'equals', value: 'suspicious' }
    ],
    outcome: 'review',
    eligibleMethods: ['auth_totp', 'auth_email_otp'],
    fallbackMethod: 'auth_email_otp',
    freshnessThreshold: 120,
    missingSignalBehavior: 'fail-open',
    enabled: true
  },
  {
    id: 'rule_stale_hardware_stepup',
    name: 'Enforce Step-up on Missing Device Attestation',
    riskLevel: 'high',
    conditions: [
      { field: 'sig_device_integrity', operator: 'equals', value: 'unavailable' }
    ],
    outcome: 'step-up',
    eligibleMethods: ['auth_passkey', 'auth_hardware_key'],
    fallbackMethod: 'auth_email_otp',
    freshnessThreshold: 60,
    missingSignalBehavior: 'fail-closed',
    enabled: true
  }
];

// Pre-packaged Simulation Scenarios
export const SIMULATION_SCENARIOS: SimulationScenario[] = [
  {
    id: 'scen_known_good',
    name: 'Ideal Session (Safe)',
    description: 'Regular residential IP, correct typing speed, strong secure enclave attestation, and local coordinates. Zero friction expected.',
    icon: 'ShieldCheck',
    signals: {
      sig_impossible_travel: { status: 'safe', value: '0.0 km/h (Cohesive Seattle pattern)', confidence: 99 },
      sig_device_integrity: { status: 'safe', value: 'Attestation Verified: Strong Device Bind', confidence: 99 },
      sig_behavioral_typing: { status: 'safe', value: '98% matching typing cadence signature', confidence: 91 },
      sig_ip_reputation: { status: 'safe', value: 'Score: 0.01 (Residential, Comcast)', confidence: 98 },
      sig_network_vpn: { status: 'safe', value: 'ISP connection. No Proxy/Tor detected', confidence: 99 }
    }
  },
  {
    id: 'scen_impossible_travel',
    name: 'Impossible Travel Alert',
    description: 'Sudden network request from London, UK, just 14 minutes after active session in Chicago, IL. Physical speed calculation: 8,300 km/h. High danger.',
    icon: 'PlaneTakeoff',
    signals: {
      sig_impossible_travel: { status: 'compromised', value: '8,300 km/h (Chicago to London mismatch)', confidence: 98 },
      sig_device_integrity: { status: 'safe', value: 'Attestation Verified: Enclave intact', confidence: 95 },
      sig_behavioral_typing: { status: 'safe', value: '91% matching typing signature', confidence: 80 },
      sig_ip_reputation: { status: 'suspicious', value: 'Score: 0.45 (Hosting center range)', confidence: 90 },
      sig_network_vpn: { status: 'safe', value: 'No VPN detected, raw connection', confidence: 94 }
    }
  },
  {
    id: 'scen_rooted_device',
    name: 'Compromised Device (Rooted)',
    description: 'Device attestation signals a jailbroken or rooted hardware posture with developer diagnostic bypass tools active. Critical infrastructure violation.',
    icon: 'Cpu',
    signals: {
      sig_impossible_travel: { status: 'safe', value: '0.0 km/h (Same location)', confidence: 99 },
      sig_device_integrity: { status: 'compromised', value: 'Strong Integrity Fail: Unlocked Bootloader', confidence: 99 },
      sig_behavioral_typing: { status: 'safe', value: '94% keystroke match', confidence: 85 },
      sig_ip_reputation: { status: 'safe', value: 'Score: 0.01 (Residential IP)', confidence: 97 },
      sig_network_vpn: { status: 'safe', value: 'No Proxy detected', confidence: 98 }
    }
  },
  {
    id: 'scen_suspicious_vpn',
    name: 'Unfamiliar Proxy & Anonymous VPN',
    description: 'User logging in from an anonymous NordVPN node. IP reputation shows frequent web scraping activities. Typical pattern for credential stuffing.',
    icon: 'Network',
    signals: {
      sig_impossible_travel: { status: 'safe', value: '12 km/h (Within region boundaries)', confidence: 80 },
      sig_device_integrity: { status: 'safe', value: 'Attestation Verified', confidence: 99 },
      sig_behavioral_typing: { status: 'safe', value: '92% typing speed match', confidence: 88 },
      sig_ip_reputation: { status: 'suspicious', value: 'Score: 0.72 (Commercial node proxy)', confidence: 95 },
      sig_network_vpn: { status: 'suspicious', value: 'VPN detected: NordVPN active node', confidence: 99 }
    }
  },
  {
    id: 'scen_behavioral_anomaly',
    name: 'Source Disagreement (Typing Drift)',
    description: 'Location, device, and network IP match perfectly, but typing pattern and cadence are completely erratic (e.g., potential takeover, sharing desktop, physical coercion).',
    icon: 'Fingerprint',
    signals: {
      sig_impossible_travel: { status: 'safe', value: '0.0 km/h (Cohesive)', confidence: 99 },
      sig_device_integrity: { status: 'safe', value: 'Attestation Verified', confidence: 99 },
      sig_behavioral_typing: { status: 'suspicious', value: '18% match (Major speed, pauses, deletions drift)', confidence: 89 },
      sig_ip_reputation: { status: 'safe', value: 'Score: 0.01', confidence: 99 },
      sig_network_vpn: { status: 'safe', value: 'No VPN detected', confidence: 99 }
    }
  },
  {
    id: 'scen_stale_collector',
    name: 'Stale / Missing Signal Fallback',
    description: 'The native device collector is unresponsive or disabled by aggressive user privacy settings. Hardware attestation payload is completely missing.',
    icon: 'EyeOff',
    signals: {
      sig_impossible_travel: { status: 'safe', value: '0.0 km/h', confidence: 90 },
      sig_device_integrity: { status: 'unavailable', value: 'Collector Unresponsive: Payload missing', confidence: 100 },
      sig_behavioral_typing: { status: 'safe', value: '91% typing match', confidence: 75 },
      sig_ip_reputation: { status: 'safe', value: 'Score: 0.05', confidence: 90 },
      sig_network_vpn: { status: 'safe', value: 'No proxy detected', confidence: 92 }
    }
  }
];

// Signal Provider health logs
export const INITIAL_PROVIDER_HEALTH: ProviderHealth[] = [
  {
    id: 'prov_geoip',
    name: 'GeoIP travel correlation microservice',
    type: 'first-party',
    status: 'active',
    latency: 18,
    errorRate: 0.02,
    freshness: '100% active',
    lastChecked: 'Now'
  },
  {
    id: 'prov_attestation',
    name: 'FIDO Hardware & Enclave Attestation Service',
    type: 'third-party',
    status: 'active',
    latency: 122,
    errorRate: 0.1,
    freshness: '99.98% uptime',
    lastChecked: '4s ago'
  },
  {
    id: 'prov_keystroke',
    name: 'Continuous Behavioral dynamics model analyzer',
    type: 'first-party',
    status: 'active',
    latency: 8,
    errorRate: 0.4,
    freshness: '100% active',
    lastChecked: '12s ago'
  },
  {
    id: 'prov_spamhaus',
    name: 'Spamhaus Blocklist API Feed',
    type: 'third-party',
    status: 'active',
    latency: 240,
    errorRate: 0.0,
    freshness: '99.95% uptime',
    lastChecked: '1m ago'
  },
  {
    id: 'prov_maxmind',
    name: 'MaxMind proxy database updater',
    type: 'third-party',
    status: 'active',
    latency: 45,
    errorRate: 0.05,
    freshness: 'Database updated 4h ago',
    lastChecked: '10m ago'
  }
];

// Initial Audit logs
export const INITIAL_AUDIT_LOGS: AuditLog[] = [
  {
    id: 'aud_93k82l',
    timestamp: '2026-07-20T14:42:15Z',
    trackingId: 'TX-8293-84K9',
    subject: 'jick.68.0@gmail.com',
    action: 'Session Authentication Request',
    policyVersion: 'RBA-v1.4.2',
    signalClasses: ['device', 'location', 'network'],
    decision: 'continue',
    achievedMethods: ['auth_passkey'],
    redactedEvidence: 'IP: 198.51.100.*, Dev: MacIntel macOS 15.4 (Redacted)',
    freshnessMet: true,
    tenantId: 'tenant-demo-default'
  },
  {
    id: 'aud_84n27j',
    timestamp: '2026-07-20T14:15:30Z',
    trackingId: 'TX-5231-92D1',
    subject: 'jick.68.0@gmail.com',
    action: 'Funds Transfer $10,000 Step-up',
    policyVersion: 'RBA-v1.4.2',
    signalClasses: ['reputation', 'network'],
    decision: 'step-up',
    achievedMethods: ['auth_passkey', 'auth_hardware_key'],
    redactedEvidence: 'IP: 203.0.113.* (Commercial Proxy Detected), Dev: Redacted',
    freshnessMet: true,
    tenantId: 'tenant-demo-default'
  },
  {
    id: 'aud_51x93p',
    timestamp: '2026-07-20T13:02:11Z',
    trackingId: 'TX-0182-39M8',
    subject: 'jick.68.0@gmail.com',
    action: 'Interactive Workspace Login',
    policyVersion: 'RBA-v1.4.2',
    signalClasses: ['device', 'location'],
    decision: 'deny',
    achievedMethods: [],
    redactedEvidence: 'Play Integrity Violation: Strong Hardware Posture Unmatched',
    freshnessMet: false,
    tenantId: 'tenant-demo-default'
  }
];

export const INITIAL_SESSIONS: ActiveSession[] = [
  {
    id: 'sess_1',
    device: 'Apple MacBook Pro 16" (Safari 18.2)',
    location: 'Seattle, WA, United States',
    ipAddress: '172.56.21.109',
    startTime: '2 hours ago',
    lastActive: 'Active now',
    riskLevel: 'low',
    signalsVerified: ['sig_device_integrity', 'sig_impossible_travel', 'sig_behavioral_typing'],
    amr: ['pwd', 'passkey']
  },
  {
    id: 'sess_2',
    device: 'Google Pixel 8 Pro (Chrome Mobile 126)',
    location: 'Seattle, WA, United States',
    ipAddress: '172.56.21.14',
    startTime: '1 day ago',
    lastActive: '5 hours ago',
    riskLevel: 'low',
    signalsVerified: ['sig_device_integrity', 'sig_impossible_travel'],
    amr: ['pwd', 'sms_otp']
  },
  {
    id: 'sess_3',
    device: 'Unknown Linux Server (curl/8.5.0)',
    location: 'London, United Kingdom',
    ipAddress: '185.112.144.12',
    startTime: '12 minutes ago',
    lastActive: '12 minutes ago',
    riskLevel: 'critical',
    signalsVerified: [],
    amr: ['pwd']
  }
];
