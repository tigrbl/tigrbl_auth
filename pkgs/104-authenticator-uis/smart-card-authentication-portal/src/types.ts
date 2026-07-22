export interface SmartCard {
  id: string;
  label: string;
  subject: string;
  issuer: string;
  serialNumber: string;
  fingerprint: string;
  notBefore: string;
  notAfter: string;
  eku: string[];
  san: string;
  status: 'active' | 'expiring' | 'expired' | 'revoked' | 'suspended';
  lastUsed: string;
  hardware: {
    reader: string;
    cardType: 'PIV' | 'CAC' | 'Custom';
    pinAttemptsRemaining: number;
    pinLocked: boolean;
    touchRequired: boolean;
  };
}

export interface TrustAnchor {
  id: string;
  name: string;
  subject: string;
  status: 'trusted' | 'untrusted' | 'revoked';
  expiry: string;
  crlUrl: string;
  ocspUrl: string;
  allowedEkis: string[];
}

export interface MTLSConfig {
  id: string;
  name: string;
  endpoint: string;
  boundCertFingerprint: string;
  authStrategy: 'strict-chain' | 'san-mapping' | 'subject-exact';
  createdAt: string;
  status: 'active' | 'inactive';
}

export interface AuditLog {
  id: string;
  timestamp: string;
  event: string;
  actor: string;
  status: 'success' | 'failure' | 'warning';
  cardFingerprint?: string;
  details: string;
  ipAddress: string;
}

export interface DiagnosticResult {
  step: string;
  status: 'pass' | 'fail' | 'warning' | 'pending';
  message: string;
  timestamp: string;
}

export interface TrustHealthMetrics {
  ocspLatencyMs: number;
  crlLastUpdate: string;
  activeAnchors: number;
  revocationServiceStatus: 'operational' | 'degraded' | 'outage';
  middlewareVersion: string;
}
