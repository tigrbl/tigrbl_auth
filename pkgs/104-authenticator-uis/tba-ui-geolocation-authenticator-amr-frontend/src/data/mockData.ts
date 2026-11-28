import { LocationSource, ZonePolicy, AuditRecord, SimulationProfile, ProviderHealth } from '../types';

export const INITIAL_SOURCES: LocationSource[] = [
  {
    id: 'src-gps',
    name: 'On-Device High-Accuracy GPS',
    type: 'device',
    state: 'active',
    priority: 1,
    accuracyThreshold: 15,
    freshnessLimit: 5,
    lastValidated: '2026-07-15T11:20:00-07:00'
  },
  {
    id: 'src-ent-wifi',
    name: 'Enterprise Corporate Office Wi-Fi',
    type: 'enterprise_zone',
    state: 'active',
    priority: 2,
    accuracyThreshold: 50,
    freshnessLimit: 15,
    lastValidated: '2026-07-15T11:22:00-07:00'
  },
  {
    id: 'src-trusted-posture',
    name: 'MDM Managed Device Signal',
    type: 'managed_posture',
    state: 'active',
    priority: 3,
    accuracyThreshold: 200,
    freshnessLimit: 10,
    lastValidated: '2026-07-15T11:25:00-07:00'
  },
  {
    id: 'src-carrier-ip',
    name: 'Carrier IP Geo-Database',
    type: 'network',
    state: 'active',
    priority: 4,
    accuracyThreshold: 5000,
    freshnessLimit: 60,
    lastValidated: '2026-07-15T11:15:00-07:00'
  },
  {
    id: 'src-idp-assertion',
    name: 'Upstream IDP Geolocation Claim',
    type: 'trusted_upstream',
    state: 'draft',
    priority: 5,
    accuracyThreshold: 25000,
    freshnessLimit: 120,
    lastValidated: '2026-07-15T11:10:00-07:00'
  }
];

export const INITIAL_POLICIES: ZonePolicy[] = [
  {
    id: 'pol-corp-hq',
    name: 'Enterprise Headquarters Access',
    description: 'Requires presence within Corporate HQ physical geofence or approved corporate range with high precision.',
    action: 'Allow',
    freshnessLimit: 10,
    accuracyRequired: 30,
    allowedCIDRs: ['10.240.0.0/16', '192.168.10.0/24'],
    bounds: {
      lat: 30.2672,
      lng: -97.7431,
      radius: 100 // 100 meters
    },
    isActive: true
  },
  {
    id: 'pol-low-risk-zone',
    name: 'Domestic Regional Access',
    description: 'Allows connection if within the same country and region as historical baseline, with basic step-up verification.',
    action: 'Step-Up',
    freshnessLimit: 30,
    accuracyRequired: 10000,
    allowedCIDRs: ['*'],
    bounds: {
      lat: 30.2672,
      lng: -97.7431,
      radius: 150000 // 150 km
    },
    isActive: true
  },
  {
    id: 'pol-restricted-embargo',
    name: 'Embargoed/Suspicious Countries Policy',
    description: 'Enforces hard block on any signals originating from restricted, sanctioned, or high-risk offshore zones.',
    action: 'Deny',
    freshnessLimit: 120,
    accuracyRequired: 100000,
    allowedCIDRs: ['185.120.0.0/16'],
    bounds: {
      lat: 35.6762,
      lng: 139.6503, // Custom geofence for block simulation
      radius: 200000
    },
    isActive: true
  }
];

export const INITIAL_SIMULATIONS: SimulationProfile[] = [
  {
    id: 'sim-ideal-hq',
    name: 'Corporate HQ Network (Ideal)',
    description: 'End user is inside HQ zone, connected to enterprise Wi-Fi, using macOS with GPS allowed.',
    lat: 30.26725,
    lng: -97.74305,
    accuracy: 10,
    ipAddress: '192.168.10.45',
    isp: 'Google Enterprise Infrastructure',
    vpnActive: false,
    mockLocationActive: false,
    providerStatus: 'healthy',
    permissionGranted: true,
    deviceOS: 'macOS'
  },
  {
    id: 'sim-remote-stepup',
    name: 'Remote Working (Normal)',
    description: 'User is working from a residential area in the same city. Requires SMS or Passkey Step-up.',
    lat: 30.2981,
    lng: -97.7212,
    accuracy: 25,
    ipAddress: '72.181.201.5',
    isp: 'Spectrum Residential',
    vpnActive: false,
    mockLocationActive: false,
    providerStatus: 'healthy',
    permissionGranted: true,
    deviceOS: 'iOS'
  },
  {
    id: 'sim-vpn-spoof',
    name: 'VPN Spoofing (Critical Risk)',
    description: 'User claims to be in HQ, but IP is from an open NordVPN node and GPS coordinates do not match Wi-Fi BSSID.',
    lat: 35.6762,
    lng: 139.6503,
    accuracy: 8,
    ipAddress: '185.120.44.12',
    isp: 'NordVPN / Hosting Provider',
    vpnActive: true,
    mockLocationActive: true,
    providerStatus: 'healthy',
    permissionGranted: true,
    deviceOS: 'Windows'
  },
  {
    id: 'sim-gps-disabled',
    name: 'GPS Permission Denied',
    description: 'User has denied browser geolocation prompts. System must fall back to Carrier IP geo-database.',
    lat: 0,
    lng: 0,
    accuracy: -1,
    ipAddress: '99.12.33.151',
    isp: 'AT&T Mobility',
    vpnActive: false,
    mockLocationActive: false,
    providerStatus: 'healthy',
    permissionGranted: false,
    deviceOS: 'Android'
  },
  {
    id: 'sim-outage-degraded',
    name: 'Provider Outage (Fail-Closed)',
    description: 'The GPS provider is completely offline. Core location evaluation is unable to confirm boundaries.',
    lat: 30.2672,
    lng: -97.7431,
    accuracy: 10,
    ipAddress: '192.168.10.99',
    isp: 'Google Enterprise Infrastructure',
    vpnActive: false,
    mockLocationActive: false,
    providerStatus: 'offline',
    permissionGranted: true,
    deviceOS: 'Linux'
  }
];

export const INITIAL_HEALTH: ProviderHealth[] = [
  {
    id: 'p-gps',
    name: 'On-Device W3C Geolocation API',
    type: 'GPS',
    latency: 18,
    errorRate: 0.4,
    lastSync: '2026-07-15T11:25:00-07:00',
    datasetVersion: 'N/A (Hardware)',
    status: 'healthy'
  },
  {
    id: 'p-geoip',
    name: 'MaxMind GeoIP2 Enterprise Database',
    type: 'IP',
    latency: 8,
    errorRate: 1.2,
    lastSync: '2026-07-15T02:00:00-07:00',
    datasetVersion: 'v2026.07.14.02',
    status: 'healthy'
  },
  {
    id: 'p-corporate',
    name: 'RADIUS/802.1X Enterprise AP Mapping',
    type: 'VPC',
    latency: 24,
    errorRate: 2.1,
    lastSync: '2026-07-15T11:20:00-07:00',
    datasetVersion: 'WiFi-Map-v4.11',
    status: 'healthy'
  },
  {
    id: 'p-mdm',
    name: 'Microsoft Intune / Jamf API',
    type: 'Posture',
    latency: 145,
    errorRate: 5.6,
    lastSync: '2026-07-15T11:15:00-07:00',
    datasetVersion: 'MDM-Policy-v12',
    status: 'degraded'
  }
];

export const INITIAL_AUDIT: AuditRecord[] = [
  {
    id: 'aud-001',
    timestamp: '2026-07-15T11:22:05-07:00',
    userEmail: 'jick.68.0@gmail.com',
    sourceType: 'Enterprise Wi-Fi & Device GPS',
    granularity: 'precise',
    policyName: 'Enterprise Headquarters Access',
    policyVersion: 'v2.4.0',
    decision: 'Allow',
    deviceOS: 'macOS',
    accuracy: 12,
    isStale: false,
    spoofSuspected: false,
    providerStatus: 'healthy',
    auditReference: 'tx_8f8e833b91a78b30'
  },
  {
    id: 'aud-002',
    timestamp: '2026-07-15T11:18:42-07:00',
    userEmail: 'jick.68.0@gmail.com',
    sourceType: 'Carrier IP Geo-Database',
    granularity: 'coarse',
    policyName: 'Domestic Regional Access',
    policyVersion: 'v2.4.0',
    decision: 'Step-Up',
    deviceOS: 'iOS',
    accuracy: 8500,
    isStale: false,
    spoofSuspected: false,
    providerStatus: 'healthy',
    auditReference: 'tx_12a7f5643e2e5c8e',
    fallbackUsed: 'SMS OTP'
  },
  {
    id: 'aud-003',
    timestamp: '2026-07-15T11:05:12-07:00',
    userEmail: 'attacker-spoof@malicious.io',
    sourceType: 'Untrusted Upstream IP Claim',
    granularity: 'none',
    policyName: 'Embargoed/Suspicious Countries Policy',
    policyVersion: 'v2.4.0',
    decision: 'Deny',
    deviceOS: 'Windows',
    accuracy: 250000,
    isStale: true,
    spoofSuspected: true,
    providerStatus: 'healthy',
    auditReference: 'tx_c7b50fde2c91838d'
  },
  {
    id: 'aud-004',
    timestamp: '2026-07-15T10:45:00-07:00',
    userEmail: 'jick.68.0@gmail.com',
    sourceType: 'Device GPS (Stale Claim)',
    granularity: 'precise',
    policyName: 'Enterprise Headquarters Access',
    policyVersion: 'v2.3.9',
    decision: 'Step-Up',
    deviceOS: 'Android',
    accuracy: 15,
    isStale: true,
    spoofSuspected: false,
    providerStatus: 'healthy',
    auditReference: 'tx_78d5301824ab11cb',
    fallbackUsed: 'Passkey'
  },
  {
    id: 'aud-005',
    timestamp: '2026-07-15T09:15:30-07:00',
    userEmail: 'jick.68.0@gmail.com',
    sourceType: 'Enterprise Wi-Fi & Device GPS',
    granularity: 'precise',
    policyName: 'Enterprise Headquarters Access',
    policyVersion: 'v2.3.9',
    decision: 'Step-Up',
    deviceOS: 'macOS',
    accuracy: 14,
    isStale: false,
    spoofSuspected: false,
    providerStatus: 'degraded', // MDM was down
    auditReference: 'tx_df245b08ee3e20e1',
    fallbackUsed: 'Authenticator App TOTP'
  }
];

export const INITIAL_CONSENTS = [
  {
    id: 'c-1',
    purpose: 'Security verification for enterprise app access',
    precision: 'Precise Location (< 15 meters)',
    grantedAt: '2026-07-15T08:00:00-07:00',
    retention: '7 Days (Audit log bound to session)',
    device: 'MacBook Pro (macOS)',
    status: 'Active'
  },
  {
    id: 'c-2',
    purpose: 'Automatic region matching check',
    precision: 'Coarse / Regional',
    grantedAt: '2026-07-14T15:20:00-07:00',
    retention: '30 Days (Anonymized analytics)',
    device: 'iPhone 15 Pro (iOS)',
    status: 'Active'
  }
];
