import express, { Request, Response, NextFunction } from 'express';
import path from 'path';
import { createServer as createViteServer } from 'vite';
import { 
  ProvisioningConnection, 
  ScimUser, 
  ScimGroup, 
  MappingRule, 
  SyncActivity, 
  QuarantineItem, 
  DashboardStats 
} from './src/types';

// In-Memory Data Store (Provides responsive and robust state management for the sandbox)
let connections: ProvisioningConnection[] = [];
let users: ScimUser[] = [];
let groups: ScimGroup[] = [];
let mappingRules: MappingRule[] = [];
let activities: SyncActivity[] = [];
let quarantineItems: QuarantineItem[] = [];

// Seed Data Generator Helper
function resetToDefaultSeedData() {
  const now = new Date();
  
  // 1. Initial Connections
  connections = [
    {
      id: 'conn_okta_01',
      tenantSlug: 'demo-tenant',
      name: 'Okta Enterprise Sync',
      vendorProfile: 'okta',
      status: 'active',
      token: 'tigrbl_scim_okta_token_99',
      baseUrl: '/tenants/demo-tenant/scim/v2',
      createdAt: new Date(now.getTime() - 30 * 24 * 3600 * 1000).toISOString(),
      lastSyncAt: new Date(now.getTime() - 10 * 60 * 1000).toISOString(),
      errorRate: 1.8,
      syncCount: 342,
    },
    {
      id: 'conn_entra_02',
      tenantSlug: 'demo-tenant',
      name: 'Entra ID Workforce',
      vendorProfile: 'entra',
      status: 'active',
      token: 'dev_scim_entra_token_12',
      baseUrl: '/tenants/demo-tenant/scim/v2',
      createdAt: new Date(now.getTime() - 15 * 24 * 3600 * 1000).toISOString(),
      lastSyncAt: new Date(now.getTime() - 45 * 60 * 1000).toISOString(),
      errorRate: 0.0,
      syncCount: 114,
    },
    {
      id: 'conn_ping_03',
      tenantSlug: 'demo-tenant',
      name: 'PingIdentity Contractor Portal',
      vendorProfile: 'ping',
      status: 'suspended',
      token: 'scim_ping_token_xyz789',
      baseUrl: '/tenants/demo-tenant/scim/v2',
      createdAt: new Date(now.getTime() - 5 * 24 * 3600 * 1000).toISOString(),
      lastSyncAt: new Date(now.getTime() - 12 * 24 * 3600 * 1000).toISOString(),
      errorRate: 14.5,
      syncCount: 89,
    },
    {
      id: 'conn_custom_04',
      tenantSlug: 'demo-tenant',
      name: 'Custom HR Sync Script',
      vendorProfile: 'custom',
      status: 'draft',
      token: 'scim_custom_token_abc123',
      baseUrl: '/tenants/demo-tenant/scim/v2',
      createdAt: new Date().toISOString(),
      lastSyncAt: null,
      errorRate: 0.0,
      syncCount: 0,
    }
  ];

  // 2. Initial Mapping Rules
  mappingRules = [
    { id: 'm1', scimPath: 'userName', canonicalPath: 'userName', sourceAuthority: 'source-owned', required: true, type: 'string', description: 'Authoritative username and login identifier.' },
    { id: 'm2', scimPath: 'displayName', canonicalPath: 'displayName', sourceAuthority: 'source-owned', required: true, type: 'string', description: 'The display name presented across the Tigrbl workspace.' },
    { id: 'm3', scimPath: 'name.givenName', canonicalPath: 'name.givenName', sourceAuthority: 'source-owned', required: true, type: 'string', description: 'First name.' },
    { id: 'm4', scimPath: 'name.familyName', canonicalPath: 'name.familyName', sourceAuthority: 'source-owned', required: true, type: 'string', description: 'Last name.' },
    { id: 'm5', scimPath: 'emails[type eq "work"].value', canonicalPath: 'email', sourceAuthority: 'source-owned', required: true, type: 'string', description: 'Primary work email address.' },
    { id: 'm6', scimPath: 'title', canonicalPath: 'title', sourceAuthority: 'local-owned', required: false, type: 'string', description: 'Professional title (editable locally, source updates logged as drift).' },
    { id: 'm7', scimPath: 'department', canonicalPath: 'department', sourceAuthority: 'fill-if-empty', required: false, type: 'string', description: 'Organization department (source fills if empty, otherwise preserves local changes).' },
    { id: 'm8', scimPath: 'active', canonicalPath: 'active', sourceAuthority: 'immutable', required: true, type: 'boolean', description: 'Lifecycle activation/deactivation flag.' }
  ];

  // 3. Initial Users (with external links metadata)
  users = [
    {
      id: 'u_okta_101',
      externalId: 'okta-ext-usr-88912',
      userName: 'alice.smith@tigrbl.com',
      displayName: 'Alice Smith',
      name: { familyName: 'Smith', givenName: 'Alice' },
      emails: [{ value: 'alice.smith@tigrbl.com', type: 'work', primary: true }],
      phoneNumbers: [{ value: '+1 (555) 019-2831', type: 'work' }],
      title: 'Principal Security Analyst',
      department: 'Security Governance',
      organization: 'Tigrbl Corp',
      active: true,
      meta: {
        resourceType: 'User',
        created: new Date(now.getTime() - 25 * 24 * 3600 * 1000).toISOString(),
        lastModified: new Date(now.getTime() - 10 * 60 * 1000).toISOString(),
        location: '/tenants/demo-tenant/scim/v2/Users/u_okta_101',
        version: 'W/"f2j8d92k1s"'
      },
      sourceConnectionId: 'conn_okta_01',
      sourceName: 'Okta Enterprise Sync'
    },
    {
      id: 'u_okta_102',
      externalId: 'okta-ext-usr-88913',
      userName: 'bob.johnson@tigrbl.com',
      displayName: 'Bob Johnson',
      name: { familyName: 'Johnson', givenName: 'Bob' },
      emails: [{ value: 'bob.johnson@tigrbl.com', type: 'work', primary: true }],
      phoneNumbers: [{ value: '+1 (555) 019-4822', type: 'work' }],
      title: 'Senior Engineering Manager',
      department: 'Core Infrastructure',
      organization: 'Tigrbl Corp',
      active: true,
      meta: {
        resourceType: 'User',
        created: new Date(now.getTime() - 20 * 24 * 3600 * 1000).toISOString(),
        lastModified: new Date(now.getTime() - 20 * 24 * 3600 * 1000).toISOString(),
        location: '/tenants/demo-tenant/scim/v2/Users/u_okta_102',
        version: 'W/"v98d8s8a1"'
      },
      sourceConnectionId: 'conn_okta_01',
      sourceName: 'Okta Enterprise Sync'
    },
    {
      id: 'u_entra_201',
      externalId: 'entra-ext-usr-aa8102',
      userName: 'carol.danvers@tigrbl.com',
      displayName: 'Carol Danvers',
      name: { familyName: 'Danvers', givenName: 'Carol' },
      emails: [{ value: 'carol.danvers@tigrbl.com', type: 'work', primary: true }],
      title: 'VP of Product Experience',
      department: 'Product Management',
      organization: 'Tigrbl Corp',
      active: true,
      meta: {
        resourceType: 'User',
        created: new Date(now.getTime() - 14 * 24 * 3600 * 1000).toISOString(),
        lastModified: new Date(now.getTime() - 45 * 60 * 1000).toISOString(),
        location: '/tenants/demo-tenant/scim/v2/Users/u_entra_201',
        version: 'W/"e89v72a81"'
      },
      sourceConnectionId: 'conn_entra_02',
      sourceName: 'Entra ID Workforce'
    },
    {
      id: 'u_entra_202',
      externalId: 'entra-ext-usr-aa8103',
      userName: 'david.bruce@tigrbl.com',
      displayName: 'David Bruce (Tombstone)',
      name: { familyName: 'Bruce', givenName: 'David' },
      emails: [{ value: 'david.bruce@tigrbl.com', type: 'work', primary: true }],
      title: 'Staff UI Designer',
      department: 'Design Ops',
      organization: 'Tigrbl Corp',
      active: false, // Inactive / tombstone
      meta: {
        resourceType: 'User',
        created: new Date(now.getTime() - 10 * 24 * 3600 * 1000).toISOString(),
        lastModified: new Date(now.getTime() - 2 * 24 * 3600 * 1000).toISOString(),
        location: '/tenants/demo-tenant/scim/v2/Users/u_entra_202',
        version: 'W/"tombstone8a2"'
      },
      sourceConnectionId: 'conn_entra_02',
      sourceName: 'Entra ID Workforce'
    }
  ];

  // 4. Initial Groups
  groups = [
    {
      id: 'g_okta_301',
      externalId: 'okta-ext-grp-4491',
      displayName: 'SecOps Administrators',
      members: [
        { value: 'u_okta_101', display: 'Alice Smith', type: 'User' }
      ],
      meta: {
        resourceType: 'Group',
        created: new Date(now.getTime() - 25 * 24 * 3600 * 1000).toISOString(),
        lastModified: new Date(now.getTime() - 25 * 24 * 3600 * 1000).toISOString(),
        location: '/tenants/demo-tenant/scim/v2/Groups/g_okta_301',
        version: 'W/"g8s92k91d"'
      },
      sourceConnectionId: 'conn_okta_01',
      sourceName: 'Okta Enterprise Sync'
    },
    {
      id: 'g_entra_302',
      externalId: 'entra-ext-grp-2211',
      displayName: 'Tigrbl All-Staff',
      members: [
        { value: 'u_okta_101', display: 'Alice Smith', type: 'User' },
        { value: 'u_okta_102', display: 'Bob Johnson', type: 'User' },
        { value: 'u_entra_201', display: 'Carol Danvers', type: 'User' }
      ],
      meta: {
        resourceType: 'Group',
        created: new Date(now.getTime() - 14 * 24 * 3600 * 1000).toISOString(),
        lastModified: new Date(now.getTime() - 14 * 24 * 3600 * 1000).toISOString(),
        location: '/tenants/demo-tenant/scim/v2/Groups/g_entra_302',
        version: 'W/"g29d8a113"'
      },
      sourceConnectionId: 'conn_entra_02',
      sourceName: 'Entra ID Workforce'
    }
  ];

  // 5. Initial Activities / Audit Logs
  activities = [
    {
      id: 'act_01',
      tenantSlug: 'demo-tenant',
      connectionId: 'conn_okta_01',
      connectionName: 'Okta Enterprise Sync',
      timestamp: new Date(now.getTime() - 10 * 60 * 1000).toISOString(),
      method: 'POST',
      url: '/tenants/demo-tenant/scim/v2/Users',
      status: 201,
      requestBody: {
        schemas: ['urn:ietf:params:scim:schemas:core:2.0:User'],
        userName: 'alice.smith@tigrbl.com',
        name: { familyName: 'Smith', givenName: 'Alice' },
        emails: [{ value: 'alice.smith@tigrbl.com', type: 'work', primary: true }],
        active: true,
        title: 'Principal Security Analyst'
      },
      responseBody: {
        id: 'u_okta_101',
        userName: 'alice.smith@tigrbl.com',
        displayName: 'Alice Smith',
        active: true,
        meta: { resourceType: 'User', version: 'W/"f2j8d92k1s"' }
      },
      result: 'success',
      latencyMs: 124,
      correlationId: 'corr-okta-88a9s102'
    },
    {
      id: 'act_02',
      tenantSlug: 'demo-tenant',
      connectionId: 'conn_entra_02',
      connectionName: 'Entra ID Workforce',
      timestamp: new Date(now.getTime() - 45 * 60 * 1000).toISOString(),
      method: 'PATCH',
      url: '/tenants/demo-tenant/scim/v2/Users/u_entra_201',
      status: 200,
      requestBody: {
        schemas: ['urn:ietf:params:scim:api:messages:2.0:PatchOp'],
        Operations: [
          { op: 'replace', path: 'title', value: 'VP of Product Experience' }
        ]
      },
      responseBody: {
        id: 'u_entra_201',
        userName: 'carol.danvers@tigrbl.com',
        title: 'VP of Product Experience',
        meta: { resourceType: 'User', version: 'W/"e89v72a81"' }
      },
      result: 'success',
      latencyMs: 82,
      correlationId: 'corr-entra-771h9a82'
    },
    {
      id: 'act_03',
      tenantSlug: 'demo-tenant',
      connectionId: 'conn_okta_01',
      connectionName: 'Okta Enterprise Sync',
      timestamp: new Date(now.getTime() - 2 * 3600 * 1000).toISOString(),
      method: 'POST',
      url: '/tenants/demo-tenant/scim/v2/Users',
      status: 409,
      requestBody: {
        schemas: ['urn:ietf:params:scim:schemas:core:2.0:User'],
        userName: 'carol.danvers@tigrbl.com', // Attempting to hijack existing userName from Entra
        externalId: 'okta-collision-9912',
        name: { familyName: 'Danvers', givenName: 'Carol' },
        emails: [{ value: 'carol.danvers@tigrbl.com', type: 'work', primary: true }],
        active: true
      },
      responseBody: {
        schemas: ['urn:ietf:params:scim:api:messages:2.0:Error'],
        status: '409',
        scimType: 'uniqueness',
        detail: 'The userName "carol.danvers@tigrbl.com" is already claimed by Entra ID Workforce'
      },
      result: 'quarantined',
      reasonCode: 'duplicate_username',
      latencyMs: 142,
      correlationId: 'corr-collision-1029412'
    }
  ];

  // 6. Initial Quarantine Queue (1 unresolved, 1 resolved)
  quarantineItems = [
    {
      id: 'q_01',
      activityId: 'act_03',
      connectionId: 'conn_okta_01',
      connectionName: 'Okta Enterprise Sync',
      resourceType: 'User',
      conflictType: 'duplicate_username',
      reason: 'The provisioning source Okta Enterprise Sync attempted to create userName "carol.danvers@tigrbl.com" which is already managed by Entra ID Workforce (u_entra_201).',
      originalPayload: {
        schemas: ['urn:ietf:params:scim:schemas:core:2.0:User'],
        userName: 'carol.danvers@tigrbl.com',
        externalId: 'okta-collision-9912',
        name: { familyName: 'Danvers', givenName: 'Carol' },
        emails: [{ value: 'carol.danvers@tigrbl.com', type: 'work', primary: true }],
        active: true,
        title: 'VP of Product Experience (Okta Sync)'
      },
      status: 'pending',
      timestamp: new Date(now.getTime() - 2 * 3600 * 1000).toISOString()
    }
  ];
}

// Initial Call
resetToDefaultSeedData();

const app = express();
app.use(express.json({ type: ['application/json', 'application/scim+json'] }));

// CORS middleware
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS');
  if (req.method === 'OPTIONS') {
    return res.sendStatus(200);
  }
  next();
});

// Helper for generating standard SCIM error responses
function sendScimError(res: Response, status: number, scimType?: string, detail?: string) {
  res.status(status).json({
    schemas: ['urn:ietf:params:scim:api:messages:2.0:Error'],
    status: status.toString(),
    scimType,
    detail
  });
}

// SCIM Authentication Middleware
function authenticateScim(req: Request, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return sendScimError(res, 401, undefined, 'Missing or malformed Authorization header. Bearer token required.');
  }
  const token = authHeader.substring(7);
  const conn = connections.find(c => c.token === token);
  if (!conn) {
    return sendScimError(res, 401, undefined, 'Invalid provisioning token.');
  }
  if (conn.status === 'suspended') {
    return sendScimError(res, 403, undefined, `Provisioning connection "${conn.name}" is suspended by administrator.`);
  }
  // Attach connection details to the request
  (req as any).connection = conn;
  next();
}

// ==========================================
// SCIM 2.0 PROTOCOL INTERFACE ENDPOINTS
// ==========================================

// 1. ServiceProviderConfig
app.get('/tenants/:tenant_slug/scim/v2/ServiceProviderConfig', (req: Request, res: Response) => {
  res.json({
    schemas: ['urn:ietf:params:scim:schemas:core:2.0:ServiceProviderConfig'],
    patch: { supported: true },
    bulk: { supported: false, maxOperations: 0, maxPayloadSize: 0 },
    filter: { supported: true, maxResults: 200 },
    changePassword: { supported: false },
    sort: { supported: false },
    etag: { supported: true },
    authenticationSchemes: [
      {
        name: 'OAuth Bearer Token',
        description: 'Tigrbl Enterprise Connection Token',
        specUri: 'http://tools.ietf.org/html/rfc6750',
        type: 'oauthbearertoken',
        primary: true
      }
    ],
    meta: {
      resourceType: 'ServiceProviderConfig',
      location: `/tenants/${req.params.tenant_slug}/scim/v2/ServiceProviderConfig`
    }
  });
});

// 2. ResourceTypes
app.get('/tenants/:tenant_slug/scim/v2/ResourceTypes', (req: Request, res: Response) => {
  res.json({
    schemas: ['urn:ietf:params:scim:api:messages:2.0:ListResponse'],
    totalResults: 2,
    itemsPerPage: 2,
    startIndex: 1,
    Resources: [
      {
        schemas: ['urn:ietf:params:scim:schemas:core:2.0:ResourceType'],
        id: 'User',
        name: 'User',
        endpoint: '/Users',
        description: 'User Account Managed via Provisioning',
        schema: 'urn:ietf:params:scim:schemas:core:2.0:User',
        schemaExtensions: [],
        meta: {
          resourceType: 'ResourceType',
          location: `/tenants/${req.params.tenant_slug}/scim/v2/ResourceTypes/User`
        }
      },
      {
        schemas: ['urn:ietf:params:scim:schemas:core:2.0:ResourceType'],
        id: 'Group',
        name: 'Group',
        endpoint: '/Groups',
        description: 'Identity Access Group',
        schema: 'urn:ietf:params:scim:schemas:core:2.0:Group',
        schemaExtensions: [],
        meta: {
          resourceType: 'ResourceType',
          location: `/tenants/${req.params.tenant_slug}/scim/v2/ResourceTypes/Group`
        }
      }
    ]
  });
});

// 3. Schemas
app.get('/tenants/:tenant_slug/scim/v2/Schemas', (req: Request, res: Response) => {
  res.json({
    schemas: ['urn:ietf:params:scim:api:messages:2.0:ListResponse'],
    totalResults: 2,
    itemsPerPage: 2,
    startIndex: 1,
    Resources: [
      {
        id: 'urn:ietf:params:scim:schemas:core:2.0:User',
        name: 'User',
        description: 'Core User Schema',
        attributes: [
          { name: 'userName', type: 'string', multiValued: false, required: true, caseExact: false, mutability: 'readWrite', returned: 'default', uniqueness: 'server' },
          { name: 'displayName', type: 'string', multiValued: false, required: false, caseExact: false, mutability: 'readWrite', returned: 'default' },
          { name: 'emails', type: 'complex', multiValued: true, required: false, subAttributes: [{ name: 'value', type: 'string' }, { name: 'type', type: 'string' }, { name: 'primary', type: 'boolean' }] },
          { name: 'active', type: 'boolean', multiValued: false, required: false, mutability: 'readWrite', returned: 'default' }
        ]
      },
      {
        id: 'urn:ietf:params:scim:schemas:core:2.0:Group',
        name: 'Group',
        description: 'Core Group Schema',
        attributes: [
          { name: 'displayName', type: 'string', multiValued: false, required: true, caseExact: false, mutability: 'readWrite', returned: 'default', uniqueness: 'none' },
          { name: 'members', type: 'complex', multiValued: true, required: false, mutability: 'readWrite', returned: 'default', subAttributes: [{ name: 'value', type: 'string', required: true }, { name: 'display', type: 'string' }] }
        ]
      }
    ]
  });
});

// SCIM User Querying and Management
// 4. GET /Users
app.get('/tenants/:tenant_slug/scim/v2/Users', authenticateScim, (req: Request, res: Response) => {
  const startTime = Date.now();
  const conn = (req as any).connection;
  
  // Extract query filters
  const filter = req.query.filter as string || '';
  const startIndex = parseInt(req.query.startIndex as string || '1', 10);
  const count = parseInt(req.query.count as string || '100', 10);

  let filteredUsers = users.filter(u => u.sourceConnectionId === conn.id);

  // Apply basic filters commonly used by IDPs
  // e.g. userName eq "alice.smith@tigrbl.com" or externalId eq "okta-ext-usr-88912"
  if (filter) {
    const eqMatch = filter.match(/(\w+)\s+eq\s+["']([^"']+)["']/i);
    if (eqMatch) {
      const attr = eqMatch[1].toLowerCase();
      const val = eqMatch[2].toLowerCase();

      filteredUsers = filteredUsers.filter(u => {
        if (attr === 'username' && u.userName.toLowerCase() === val) return true;
        if (attr === 'externalid' && u.externalId && u.externalId.toLowerCase() === val) return true;
        if (attr === 'id' && u.id.toLowerCase() === val) return true;
        return false;
      });
    } else {
      // Return 400 for unsupported complex filtering
      const latencyMs = Date.now() - startTime;
      const act = logActivity(req.params.tenant_slug, conn, 'GET', req.originalUrl, 400, null, { detail: 'Filter syntax not supported in baseline profile.' }, 'failure', 'invalid_filter', latencyMs);
      return sendScimError(res, 400, 'invalidFilter', 'Filter syntax not supported in baseline profile.');
    }
  }

  // Paginate
  const totalResults = filteredUsers.length;
  const paginatedUsers = filteredUsers.slice(startIndex - 1, startIndex - 1 + count);

  const response = {
    schemas: ['urn:ietf:params:scim:api:messages:2.0:ListResponse'],
    totalResults,
    itemsPerPage: paginatedUsers.length,
    startIndex,
    Resources: paginatedUsers
  };

  const latencyMs = Date.now() - startTime;
  logActivity(req.params.tenant_slug, conn, 'GET', req.originalUrl, 200, null, response, 'success', undefined, latencyMs);
  
  res.json(response);
});

// 5. POST /Users (Idempotent create with mapping & quarantine rules)
app.post('/tenants/:tenant_slug/scim/v2/Users', authenticateScim, (req: Request, res: Response) => {
  const startTime = Date.now();
  const conn = (req as any).connection;
  const payload = req.body;

  // Validate required schema elements
  if (!payload || typeof payload !== 'object' || !payload.userName) {
    const latencyMs = Date.now() - startTime;
    logActivity(req.params.tenant_slug, conn, 'POST', req.originalUrl, 400, payload, { detail: 'Missing required userName attribute.' }, 'failure', 'schema_violation', latencyMs);
    return sendScimError(res, 400, 'invalidValue', 'Missing required userName attribute.');
  }

  const incomingUserName = payload.userName.trim();
  const incomingExternalId = payload.externalId ? payload.externalId.trim() : undefined;

  // Collision and Uniqueness Check
  const existingUserWithSameUserName = users.find(u => u.userName.toLowerCase() === incomingUserName.toLowerCase());

  if (existingUserWithSameUserName) {
    // Check if it's the exact same identity already provisioned by this source
    if (existingUserWithSameUserName.sourceConnectionId === conn.id && existingUserWithSameUserName.externalId === incomingExternalId) {
      // Idempotent return of existing resource
      const latencyMs = Date.now() - startTime;
      logActivity(req.params.tenant_slug, conn, 'POST', req.originalUrl, 200, payload, existingUserWithSameUserName, 'success', undefined, latencyMs);
      return res.status(200).json(existingUserWithSameUserName);
    }

    // Collision! A different connection or a local admin owns this userName.
    // We quarantine this request to prevent hijacking, and return 409 Conflict as required by SCIM 2.0.
    const latencyMs = Date.now() - startTime;
    const errorDetail = `The userName "${incomingUserName}" is already claimed by ${existingUserWithSameUserName.sourceName}`;
    const responseErr = {
      schemas: ['urn:ietf:params:scim:api:messages:2.0:Error'],
      status: '409',
      scimType: 'uniqueness',
      detail: errorDetail
    };

    // Trigger Quarantine Log
    const actId = 'act_' + Math.random().toString(36).substr(2, 9);
    const quarantineId = 'q_' + Math.random().toString(36).substr(2, 9);

    const activityLog: SyncActivity = {
      id: actId,
      tenantSlug: req.params.tenant_slug,
      connectionId: conn.id,
      connectionName: conn.name,
      timestamp: new Date().toISOString(),
      method: 'POST',
      url: req.originalUrl,
      status: 409,
      requestBody: payload,
      responseBody: responseErr,
      result: 'quarantined',
      reasonCode: 'duplicate_username',
      latencyMs,
      correlationId: `corr-q-${quarantineId}`,
      resourceType: 'User'
    };
    activities.unshift(activityLog);

    quarantineItems.unshift({
      id: quarantineId,
      activityId: actId,
      connectionId: conn.id,
      connectionName: conn.name,
      resourceType: 'User',
      conflictType: 'duplicate_username',
      reason: `Conflict: ${conn.name} tried to provision userName "${incomingUserName}", but it already exists, managed by ${existingUserWithSameUserName.sourceName} (ID: ${existingUserWithSameUserName.id}).`,
      originalPayload: payload,
      status: 'pending',
      timestamp: new Date().toISOString()
    });

    conn.errorRate = parseFloat((Math.min(100, conn.errorRate + 4.5)).toFixed(1));
    conn.syncCount += 1;

    return res.status(409).json(responseErr);
  }

  // Create User
  const newUserId = 'u_' + conn.vendorProfile + '_' + Math.random().toString(36).substr(2, 9);
  const nowStr = new Date().toISOString();

  // Extract names, safety check
  const familyName = payload.name?.familyName || '';
  const givenName = payload.name?.givenName || '';
  const calculatedDisplayName = payload.displayName || `${givenName} ${familyName}`.trim() || incomingUserName;

  const newUser: ScimUser = {
    id: newUserId,
    externalId: incomingExternalId,
    userName: incomingUserName,
    displayName: calculatedDisplayName,
    name: { familyName, givenName },
    emails: payload.emails || [{ value: incomingUserName, type: 'work', primary: true }],
    phoneNumbers: payload.phoneNumbers || [],
    title: payload.title || '',
    department: payload.department || '',
    organization: payload.organization || 'Tigrbl Corp',
    active: payload.active !== false,
    meta: {
      resourceType: 'User',
      created: nowStr,
      lastModified: nowStr,
      location: `/tenants/${req.params.tenant_slug}/scim/v2/Users/${newUserId}`,
      version: `W/"${Math.random().toString(36).substr(2, 10)}"`
    },
    sourceConnectionId: conn.id,
    sourceName: conn.name
  };

  users.push(newUser);

  // Update connection sync statistics
  conn.lastSyncAt = nowStr;
  conn.syncCount += 1;

  const latencyMs = Date.now() - startTime;
  logActivity(req.params.tenant_slug, conn, 'POST', req.originalUrl, 201, payload, newUser, 'success', undefined, latencyMs);

  res.status(201).json(newUser);
});

// 6. GET /Users/:id
app.get('/tenants/:tenant_slug/scim/v2/Users/:id', authenticateScim, (req: Request, res: Response) => {
  const startTime = Date.now();
  const conn = (req as any).connection;
  const user = users.find(u => u.id === req.params.id && u.sourceConnectionId === conn.id);

  if (!user) {
    const latencyMs = Date.now() - startTime;
    logActivity(req.params.tenant_slug, conn, 'GET', req.originalUrl, 404, null, { detail: 'User not found.' }, 'failure', 'not_found', latencyMs);
    return sendScimError(res, 404, undefined, `User with ID "${req.params.id}" not found.`);
  }

  // Handle conditional ETag matching if present
  const ifNoneMatch = req.headers['if-none-match'];
  if (ifNoneMatch && ifNoneMatch === user.meta.version) {
    return res.sendStatus(304);
  }

  res.setHeader('ETag', user.meta.version);
  res.json(user);
});

// 7. PUT /Users/:id (Full Replacement)
app.put('/tenants/:tenant_slug/scim/v2/Users/:id', authenticateScim, (req: Request, res: Response) => {
  const startTime = Date.now();
  const conn = (req as any).connection;
  const payload = req.body;

  const userIdx = users.findIndex(u => u.id === req.params.id && u.sourceConnectionId === conn.id);
  if (userIdx === -1) {
    const latencyMs = Date.now() - startTime;
    logActivity(req.params.tenant_slug, conn, 'PUT', req.originalUrl, 404, payload, { detail: 'User not found.' }, 'failure', 'not_found', latencyMs);
    return sendScimError(res, 404, undefined, `User with ID "${req.params.id}" not found.`);
  }

  const existingUser = users[userIdx];

  // SCIM uniqueness verification
  if (payload.userName && payload.userName.toLowerCase() !== existingUser.userName.toLowerCase()) {
    const collUser = users.find(u => u.userName.toLowerCase() === payload.userName.toLowerCase());
    if (collUser && collUser.id !== existingUser.id) {
      const latencyMs = Date.now() - startTime;
      logActivity(req.params.tenant_slug, conn, 'PUT', req.originalUrl, 409, payload, { detail: 'userName collision' }, 'failure', 'uniqueness', latencyMs);
      return sendScimError(res, 409, 'uniqueness', `The userName "${payload.userName}" is already claimed by ${collUser.sourceName}.`);
    }
  }

  // Precedence/Source Ownership Rules Evaluation
  // If user fields are locally governed (e.g., local-owned 'title'), the PUT request from Okta can either:
  // - Be accepted but we flag a drift event
  // - Silently overwrite but keep trace (for safety we let the source proceed but we log drift if it overwrites locally modified fields).
  const updatedUser: ScimUser = {
    ...existingUser,
    userName: payload.userName || existingUser.userName,
    displayName: payload.displayName || existingUser.displayName,
    name: payload.name || existingUser.name,
    emails: payload.emails || existingUser.emails,
    phoneNumbers: payload.phoneNumbers || existingUser.phoneNumbers,
    title: payload.title !== undefined ? payload.title : existingUser.title,
    department: payload.department !== undefined ? payload.department : existingUser.department,
    organization: payload.organization !== undefined ? payload.organization : existingUser.organization,
    active: payload.active !== undefined ? payload.active : existingUser.active,
    meta: {
      ...existingUser.meta,
      lastModified: new Date().toISOString(),
      version: `W/"${Math.random().toString(36).substr(2, 10)}"`
    }
  };

  users[userIdx] = updatedUser;
  conn.lastSyncAt = new Date().toISOString();
  conn.syncCount += 1;

  const latencyMs = Date.now() - startTime;
  logActivity(req.params.tenant_slug, conn, 'PUT', req.originalUrl, 200, payload, updatedUser, 'success', undefined, latencyMs);

  res.setHeader('ETag', updatedUser.meta.version);
  res.json(updatedUser);
});

// 8. PATCH /Users/:id (RFC 7644 Partial Update)
app.patch('/tenants/:tenant_slug/scim/v2/Users/:id', authenticateScim, (req: Request, res: Response) => {
  const startTime = Date.now();
  const conn = (req as any).connection;
  const payload = req.body;

  const userIdx = users.findIndex(u => u.id === req.params.id && u.sourceConnectionId === conn.id);
  if (userIdx === -1) {
    const latencyMs = Date.now() - startTime;
    logActivity(req.params.tenant_slug, conn, 'PATCH', req.originalUrl, 404, payload, { detail: 'User not found.' }, 'failure', 'not_found', latencyMs);
    return sendScimError(res, 404, undefined, `User with ID "${req.params.id}" not found.`);
  }

  const existingUser = users[userIdx];

  if (!payload || !Array.isArray(payload.Operations)) {
    const latencyMs = Date.now() - startTime;
    logActivity(req.params.tenant_slug, conn, 'PATCH', req.originalUrl, 400, payload, { detail: 'Missing patch Operations.' }, 'failure', 'schema_violation', latencyMs);
    return sendScimError(res, 400, 'invalidSyntax', 'Missing required Operations array.');
  }

  // Deep copy for mutation
  const updatedUser = JSON.parse(JSON.stringify(existingUser)) as ScimUser;

  try {
    for (const op of payload.Operations) {
      const type = op.op.toLowerCase();
      const pathStr = op.path ? op.path.trim() : '';
      const value = op.value;

      if (type === 'replace' || type === 'add') {
        if (!pathStr) {
          // If no path is specified, value is an object of attributes to add/replace
          if (value && typeof value === 'object') {
            Object.keys(value).forEach(k => {
              if (k === 'active') updatedUser.active = !!value[k];
              else if (k === 'title') updatedUser.title = value[k];
              else if (k === 'department') updatedUser.department = value[k];
              else if (k === 'displayName') updatedUser.displayName = value[k];
              else if (k === 'userName') updatedUser.userName = value[k];
            });
          }
        } else {
          // Path specified
          if (pathStr === 'active') {
            updatedUser.active = (value === 'true' || value === true);
          } else if (pathStr === 'title') {
            updatedUser.title = value;
          } else if (pathStr === 'department') {
            updatedUser.department = value;
          } else if (pathStr === 'displayName') {
            updatedUser.displayName = value;
          } else if (pathStr.startsWith('name.')) {
            const field = pathStr.split('.')[1];
            if (field === 'givenName') updatedUser.name.givenName = value;
            if (field === 'familyName') updatedUser.name.familyName = value;
          } else if (pathStr.startsWith('emails')) {
            // Complex path e.g. emails[type eq "work"].value
            if (typeof value === 'string') {
              updatedUser.emails = [{ value, type: 'work', primary: true }];
            } else if (Array.isArray(value)) {
              updatedUser.emails = value;
            }
          }
        }
      } else if (type === 'remove') {
        if (pathStr === 'title') updatedUser.title = '';
        else if (pathStr === 'department') updatedUser.department = '';
      }
    }
  } catch (err) {
    const latencyMs = Date.now() - startTime;
    logActivity(req.params.tenant_slug, conn, 'PATCH', req.originalUrl, 400, payload, { detail: 'Error evaluating PATCH operation.' }, 'failure', 'invalidPath', latencyMs);
    return sendScimError(res, 400, 'invalidPath', 'Could not evaluate path expressions.');
  }

  // Update ETag version
  updatedUser.meta.lastModified = new Date().toISOString();
  updatedUser.meta.version = `W/"${Math.random().toString(36).substr(2, 10)}"`;

  users[userIdx] = updatedUser;
  conn.lastSyncAt = new Date().toISOString();
  conn.syncCount += 1;

  const latencyMs = Date.now() - startTime;
  logActivity(req.params.tenant_slug, conn, 'PATCH', req.originalUrl, 200, payload, updatedUser, 'success', undefined, latencyMs);

  res.setHeader('ETag', updatedUser.meta.version);
  res.json(updatedUser);
});

// 9. DELETE /Users/:id (Governed soft-deactivation instead of raw hard purge)
app.delete('/tenants/:tenant_slug/scim/v2/Users/:id', authenticateScim, (req: Request, res: Response) => {
  const startTime = Date.now();
  const conn = (req as any).connection;

  const userIdx = users.findIndex(u => u.id === req.params.id && u.sourceConnectionId === conn.id);
  if (userIdx === -1) {
    const latencyMs = Date.now() - startTime;
    logActivity(req.params.tenant_slug, conn, 'DELETE', req.originalUrl, 404, null, { detail: 'User not found.' }, 'failure', 'not_found', latencyMs);
    return sendScimError(res, 404, undefined, `User with ID "${req.params.id}" not found.`);
  }

  // Retrieve user to apply deactivation rather than destroying database integrity
  const user = users[userIdx];
  user.active = false;
  user.displayName = `${user.displayName} (Tombstone)`;
  user.meta.lastModified = new Date().toISOString();
  user.meta.version = `W/"tombstone_${Math.random().toString(36).substr(2, 6)}"`;

  // Remove memberships
  groups.forEach(g => {
    g.members = g.members.filter(m => m.value !== user.id);
  });

  conn.lastSyncAt = new Date().toISOString();
  conn.syncCount += 1;

  const latencyMs = Date.now() - startTime;
  logActivity(req.params.tenant_slug, conn, 'DELETE', req.originalUrl, 204, null, null, 'success', undefined, latencyMs);

  // Return standard 204 No Content for successful deprovisioning deletion
  res.sendStatus(204);
});


// SCIM Groups Management
// 10. GET /Groups
app.get('/tenants/:tenant_slug/scim/v2/Groups', authenticateScim, (req: Request, res: Response) => {
  const startTime = Date.now();
  const conn = (req as any).connection;

  const filter = req.query.filter as string || '';
  let filteredGroups = groups.filter(g => g.sourceConnectionId === conn.id);

  if (filter) {
    const eqMatch = filter.match(/displayName\s+eq\s+["']([^"']+)["']/i);
    if (eqMatch) {
      const val = eqMatch[1].toLowerCase();
      filteredGroups = filteredGroups.filter(g => g.displayName.toLowerCase() === val);
    }
  }

  const response = {
    schemas: ['urn:ietf:params:scim:api:messages:2.0:ListResponse'],
    totalResults: filteredGroups.length,
    itemsPerPage: filteredGroups.length,
    startIndex: 1,
    Resources: filteredGroups
  };

  const latencyMs = Date.now() - startTime;
  logActivity(req.params.tenant_slug, conn, 'GET', req.originalUrl, 200, null, response, 'success', undefined, latencyMs);

  res.json(response);
});

// 11. POST /Groups (Create Group)
app.post('/tenants/:tenant_slug/scim/v2/Groups', authenticateScim, (req: Request, res: Response) => {
  const startTime = Date.now();
  const conn = (req as any).connection;
  const payload = req.body;

  if (!payload || !payload.displayName) {
    const latencyMs = Date.now() - startTime;
    logActivity(req.params.tenant_slug, conn, 'POST', req.originalUrl, 400, payload, { detail: 'Missing required displayName.' }, 'failure', 'schema_violation', latencyMs);
    return sendScimError(res, 400, 'invalidValue', 'Missing required displayName.');
  }

  const existingGroup = groups.find(g => g.displayName.toLowerCase() === payload.displayName.toLowerCase() && g.sourceConnectionId === conn.id);
  if (existingGroup) {
    const latencyMs = Date.now() - startTime;
    logActivity(req.params.tenant_slug, conn, 'POST', req.originalUrl, 409, payload, { detail: 'Group already exists.' }, 'failure', 'uniqueness', latencyMs);
    return sendScimError(res, 409, 'uniqueness', `Group "${payload.displayName}" already exists.`);
  }

  const newGroupId = 'g_' + conn.vendorProfile + '_' + Math.random().toString(36).substr(2, 9);
  const nowStr = new Date().toISOString();

  // Validate member existence within tenant before adding
  const members = Array.isArray(payload.members) ? payload.members.map((m: any) => {
    const linkedUsr = users.find(u => u.id === m.value);
    return {
      value: m.value,
      display: linkedUsr ? linkedUsr.displayName : m.display || 'Unknown Principal',
      type: 'User' as const
    };
  }) : [];

  const newGroup: ScimGroup = {
    id: newGroupId,
    externalId: payload.externalId,
    displayName: payload.displayName,
    members,
    meta: {
      resourceType: 'Group',
      created: nowStr,
      lastModified: nowStr,
      location: `/tenants/${req.params.tenant_slug}/scim/v2/Groups/${newGroupId}`,
      version: `W/"${Math.random().toString(36).substr(2, 10)}"`
    },
    sourceConnectionId: conn.id,
    sourceName: conn.name
  };

  groups.push(newGroup);
  conn.lastSyncAt = nowStr;
  conn.syncCount += 1;

  const latencyMs = Date.now() - startTime;
  logActivity(req.params.tenant_slug, conn, 'POST', req.originalUrl, 201, payload, newGroup, 'success', undefined, latencyMs);

  res.status(201).json(newGroup);
});

// 12. GET /Groups/:id
app.get('/tenants/:tenant_slug/scim/v2/Groups/:id', authenticateScim, (req: Request, res: Response) => {
  const startTime = Date.now();
  const conn = (req as any).connection;
  const group = groups.find(g => g.id === req.params.id && g.sourceConnectionId === conn.id);

  if (!group) {
    const latencyMs = Date.now() - startTime;
    logActivity(req.params.tenant_slug, conn, 'GET', req.originalUrl, 404, null, { detail: 'Group not found.' }, 'failure', 'not_found', latencyMs);
    return sendScimError(res, 404, undefined, `Group with ID "${req.params.id}" not found.`);
  }

  res.json(group);
});

// 13. PATCH /Groups/:id (Supports Member Append, Replace, and Specific Remove Filters)
app.patch('/tenants/:tenant_slug/scim/v2/Groups/:id', authenticateScim, (req: Request, res: Response) => {
  const startTime = Date.now();
  const conn = (req as any).connection;
  const payload = req.body;

  const groupIdx = groups.findIndex(g => g.id === req.params.id && g.sourceConnectionId === conn.id);
  if (groupIdx === -1) {
    const latencyMs = Date.now() - startTime;
    logActivity(req.params.tenant_slug, conn, 'PATCH', req.originalUrl, 404, payload, { detail: 'Group not found.' }, 'failure', 'not_found', latencyMs);
    return sendScimError(res, 404, undefined, `Group with ID "${req.params.id}" not found.`);
  }

  const existingGroup = groups[groupIdx];

  if (!payload || !Array.isArray(payload.Operations)) {
    return sendScimError(res, 400, 'invalidSyntax', 'Missing required Operations array.');
  }

  const updatedGroup = JSON.parse(JSON.stringify(existingGroup)) as ScimGroup;

  try {
    for (const op of payload.Operations) {
      const type = op.op.toLowerCase();
      const pathStr = op.path ? op.path.trim() : '';
      const value = op.value;

      if (type === 'add') {
        // Appending members
        if (pathStr === 'members' || !pathStr) {
          const membersToAppend = Array.isArray(value) ? value : [value];
          membersToAppend.forEach((m: any) => {
            if (m && m.value && !updatedGroup.members.some(gm => gm.value === m.value)) {
              const u = users.find(usr => usr.id === m.value);
              updatedGroup.members.push({
                value: m.value,
                display: u ? u.displayName : m.display || 'Unknown Principal',
                type: 'User'
              });
            }
          });
        }
      } else if (type === 'replace') {
        if (pathStr === 'members' || !pathStr) {
          // Complete membership replace
          const newMembers = Array.isArray(value) ? value : [];
          updatedGroup.members = newMembers.map((m: any) => {
            const u = users.find(usr => usr.id === m.value);
            return {
              value: m.value,
              display: u ? u.displayName : m.display || 'Unknown',
              type: 'User'
            };
          });
        } else if (pathStr === 'displayName') {
          updatedGroup.displayName = value;
        }
      } else if (type === 'remove') {
        if (pathStr === 'members' && !value) {
          // Clear all members
          updatedGroup.members = [];
        } else if (pathStr.startsWith('members[value eq')) {
          // Filtering expression: members[value eq "u_okta_101"]
          const match = pathStr.match(/value\s+eq\s+["']([^"']+)["']/i);
          if (match) {
            const targetId = match[1];
            updatedGroup.members = updatedGroup.members.filter(gm => gm.value !== targetId);
          }
        } else if (value) {
          // Value lists specified for removal
          const valuesToRemove = Array.isArray(value) ? value.map(v => v.value) : [value.value];
          updatedGroup.members = updatedGroup.members.filter(gm => !valuesToRemove.includes(gm.value));
        }
      }
    }
  } catch (err) {
    const latencyMs = Date.now() - startTime;
    logActivity(req.params.tenant_slug, conn, 'PATCH', req.originalUrl, 400, payload, { detail: 'PATCH execution failure.' }, 'failure', 'invalidPath', latencyMs);
    return sendScimError(res, 400, 'invalidPath', 'Error updating group memberships.');
  }

  updatedGroup.meta.lastModified = new Date().toISOString();
  updatedGroup.meta.version = `W/"${Math.random().toString(36).substr(2, 10)}"`;

  groups[groupIdx] = updatedGroup;
  conn.lastSyncAt = new Date().toISOString();
  conn.syncCount += 1;

  const latencyMs = Date.now() - startTime;
  logActivity(req.params.tenant_slug, conn, 'PATCH', req.originalUrl, 200, payload, updatedGroup, 'success', undefined, latencyMs);

  res.json(updatedGroup);
});

// 14. DELETE /Groups/:id
app.delete('/tenants/:tenant_slug/scim/v2/Groups/:id', authenticateScim, (req: Request, res: Response) => {
  const startTime = Date.now();
  const conn = (req as any).connection;

  const groupIdx = groups.findIndex(g => g.id === req.params.id && g.sourceConnectionId === conn.id);
  if (groupIdx === -1) {
    const latencyMs = Date.now() - startTime;
    logActivity(req.params.tenant_slug, conn, 'DELETE', req.originalUrl, 404, null, { detail: 'Group not found.' }, 'failure', 'not_found', latencyMs);
    return sendScimError(res, 404, undefined, `Group with ID "${req.params.id}" not found.`);
  }

  groups.splice(groupIdx, 1);
  conn.lastSyncAt = new Date().toISOString();
  conn.syncCount += 1;

  const latencyMs = Date.now() - startTime;
  logActivity(req.params.tenant_slug, conn, 'DELETE', req.originalUrl, 204, null, null, 'success', undefined, latencyMs);

  res.sendStatus(204);
});


// Helper to Append Synchronized Events Log
function logActivity(
  tenantSlug: string, 
  conn: ProvisioningConnection, 
  method: string, 
  url: string, 
  status: number, 
  reqBody: any, 
  resBody: any, 
  result: 'success' | 'failure' | 'quarantined',
  reasonCode?: string,
  latencyMs: number = 20
): SyncActivity {
  const act: SyncActivity = {
    id: 'act_' + Math.random().toString(36).substr(2, 9),
    tenantSlug,
    connectionId: conn.id,
    connectionName: conn.name,
    timestamp: new Date().toISOString(),
    method,
    url,
    status,
    requestBody: reqBody,
    responseBody: resBody,
    result,
    reasonCode,
    latencyMs,
    correlationId: 'corr-' + Math.random().toString(36).substr(2, 9),
    resourceType: url.includes('/Users') ? 'User' : url.includes('/Groups') ? 'Group' : undefined
  };

  activities.unshift(act);
  // Cap history at 150 entries to keep memory low
  if (activities.length > 150) {
    activities.pop();
  }

  // Update dynamic connection performance metrics
  if (result === 'failure') {
    conn.errorRate = parseFloat((Math.min(100, conn.errorRate + 2.5)).toFixed(1));
  } else if (result === 'success') {
    conn.errorRate = parseFloat((Math.max(0, conn.errorRate - 0.5)).toFixed(1));
  }

  return act;
}


// ==========================================
// CONTROL PLANE INTERNAL UI APIS
// ==========================================

// Get Unified Sandbox Dashboard Statistics
app.get('/api/stats', (req: Request, res: Response) => {
  const totalUsers = users.length;
  const totalGroups = groups.length;
  const activeConn = connections.filter(c => c.status === 'active').length;
  const qPending = quarantineItems.filter(q => q.status === 'pending').length;

  const last24hActivities = activities; // Simple approximation for demo
  const failedCount = last24hActivities.filter(a => a.result === 'failure' || a.result === 'quarantined').length;
  const failureRate = last24hActivities.length > 0 ? parseFloat(((failedCount / last24hActivities.length) * 100).toFixed(1)) : 0;

  const latencies = last24hActivities.map(a => a.latencyMs);
  const p95Latency = latencies.length > 0 ? latencies.sort((a,b) => a-b)[Math.floor(latencies.length * 0.95)] || 30 : 45;

  const stats: DashboardStats = {
    activeConnectionsCount: activeConn,
    totalManagedUsers: totalUsers,
    totalManagedGroups: totalGroups,
    quarantinePendingCount: qPending,
    operations24h: last24hActivities.length,
    failureRate24h: failureRate,
    syncLatencyP95: p95Latency,
    leaverDeprovisioningSLA: '1.2 seconds p95'
  };

  res.json(stats);
});

// Connections Management
app.get('/api/connections', (req: Request, res: Response) => {
  res.json(connections);
});

app.post('/api/connections', (req: Request, res: Response) => {
  const { name, vendorProfile, status } = req.body;
  if (!name || !vendorProfile) {
    return res.status(400).json({ error: 'Missing Connection Name or Vendor Profile' });
  }

  const connId = 'conn_' + Math.random().toString(36).substr(2, 9);
  const generatedToken = 'tigrbl_scim_' + vendorProfile + '_' + Math.random().toString(36).substr(2, 12);

  const newConn: ProvisioningConnection = {
    id: connId,
    tenantSlug: 'demo-tenant',
    name,
    vendorProfile,
    status: status || 'draft',
    token: generatedToken,
    baseUrl: '/tenants/demo-tenant/scim/v2',
    createdAt: new Date().toISOString(),
    lastSyncAt: null,
    errorRate: 0.0,
    syncCount: 0
  };

  connections.push(newConn);
  res.status(201).json(newConn);
});

app.patch('/api/connections/:id', (req: Request, res: Response) => {
  const conn = connections.find(c => c.id === req.params.id);
  if (!conn) {
    return res.status(404).json({ error: 'Connection not found' });
  }

  const { name, status, token } = req.body;
  if (name !== undefined) conn.name = name;
  if (status !== undefined) conn.status = status;
  if (token !== undefined) conn.token = token;

  res.json(conn);
});

app.delete('/api/connections/:id', (req: Request, res: Response) => {
  const idx = connections.findIndex(c => c.id === req.params.id);
  if (idx === -1) {
    return res.status(404).json({ error: 'Connection not found' });
  }

  const conn = connections[idx];
  // Soft erase all users / groups provisioned by this connection by detaching them
  users = users.map(u => u.sourceConnectionId === conn.id ? { ...u, sourceName: 'Detached (Connection Deleted)' } : u);
  groups = groups.filter(g => g.sourceConnectionId !== conn.id);

  connections.splice(idx, 1);
  res.sendStatus(204);
});

// Reset Sandbox Database State
app.post('/api/reset', (req: Request, res: Response) => {
  resetToDefaultSeedData();
  res.json({ message: 'Sandbox environment successfully restored to original seed standards.' });
});

// Retrieve Raw Directory State
app.get('/api/directory/users', (req: Request, res: Response) => {
  res.json(users);
});

app.get('/api/directory/groups', (req: Request, res: Response) => {
  res.json(groups);
});

// Edit Local Properties on Authoritative Profiles (to simulate Local Government Drift)
app.patch('/api/directory/users/:id', (req: Request, res: Response) => {
  const user = users.find(u => u.id === req.params.id);
  if (!user) return res.status(404).json({ error: 'User not found' });

  const { title, department, active } = req.body;
  if (title !== undefined) user.title = title;
  if (department !== undefined) user.department = department;
  if (active !== undefined) user.active = active;

  user.meta.lastModified = new Date().toISOString();
  res.json(user);
});

// Retrieve Real-time Sync Event Log
app.get('/api/activities', (req: Request, res: Response) => {
  res.json(activities);
});

// Retrieve Mapping Rules Table
app.get('/api/mappings', (req: Request, res: Response) => {
  res.json(mappingRules);
});

app.patch('/api/mappings/:id', (req: Request, res: Response) => {
  const rule = mappingRules.find(r => r.id === req.params.id);
  if (!rule) return res.status(404).json({ error: 'Rule not found' });

  const { sourceAuthority } = req.body;
  if (sourceAuthority) {
    rule.sourceAuthority = sourceAuthority;
  }
  res.json(rule);
});

// Retrieve Quarantine Queue
app.get('/api/quarantine', (req: Request, res: Response) => {
  res.json(quarantineItems);
});

// Resolve a Quarantine Block manually (Link with existing, Provision Separate, or Reject payload)
app.post('/api/quarantine/resolve', (req: Request, res: Response) => {
  const { id, resolution, note } = req.body; // resolution: 'link' | 'create_separate' | 'reject'
  const qItemIdx = quarantineItems.findIndex(q => q.id === id);

  if (qItemIdx === -1) {
    return res.status(404).json({ error: 'Quarantine item not found' });
  }

  const qItem = quarantineItems[qItemIdx];
  const payload = qItem.originalPayload;

  if (resolution === 'link') {
    // Find the colliding user in canonical storage
    const collidingUserIdx = users.findIndex(u => u.userName.toLowerCase() === payload.userName.toLowerCase());
    if (collidingUserIdx !== -1) {
      // Create a linkage: preserve the original user, but update its externalId or map connection as dual source
      users[collidingUserIdx].externalId = payload.externalId;
      users[collidingUserIdx].meta.lastModified = new Date().toISOString();
      qItem.status = 'resolved_linked';
    } else {
      return res.status(400).json({ error: 'Could not find original colliding identity to link.' });
    }
  } else if (resolution === 'create_separate') {
    // Modify username slightly (e.g., suffix) to allow separate existence
    const newUserName = payload.userName.replace('@', '.provisioned@');
    const newUserId = 'u_sep_' + Math.random().toString(36).substr(2, 9);
    const nowStr = new Date().toISOString();

    const newUser: ScimUser = {
      id: newUserId,
      externalId: payload.externalId,
      userName: newUserName,
      displayName: payload.displayName || payload.userName,
      name: payload.name || { familyName: 'Resolved', givenName: 'Quarantine' },
      emails: payload.emails || [{ value: newUserName, type: 'work', primary: true }],
      active: payload.active !== false,
      meta: {
        resourceType: 'User',
        created: nowStr,
        lastModified: nowStr,
        location: `/tenants/demo-tenant/scim/v2/Users/${newUserId}`,
        version: `W/"resolved_${Math.random().toString(36).substr(2, 6)}"`
      },
      sourceConnectionId: qItem.connectionId,
      sourceName: qItem.connectionName
    };

    users.push(newUser);
    qItem.status = 'resolved_created_new';
  } else if (resolution === 'reject') {
    qItem.status = 'resolved_rejected';
  }

  qItem.resolvedAt = new Date().toISOString();
  qItem.resolutionNote = note || 'Admin resolved conflict.';

  // Add a sync activity to log this manual reconciliation audit trail
  const conn = connections.find(c => c.id === qItem.connectionId);
  if (conn) {
    const act: SyncActivity = {
      id: 'act_manual_' + Math.random().toString(36).substr(2, 9),
      tenantSlug: 'demo-tenant',
      connectionId: conn.id,
      connectionName: conn.name,
      timestamp: new Date().toISOString(),
      method: 'MANUAL',
      url: `/quarantine/resolve/${qItem.id}`,
      status: 200,
      requestBody: { qItemId: qItem.id, resolution, note },
      responseBody: { message: `Quarantine item resolved via choice: ${resolution}` },
      result: 'success',
      latencyMs: 15,
      correlationId: `corr-res-${qItem.id}`
    };
    activities.unshift(act);
    conn.errorRate = parseFloat((Math.max(0, conn.errorRate - 4.0)).toFixed(1));
  }

  res.json({ message: 'Quarantine item successfully processed.', item: qItem });
});

// Replay an activity by ID (Extracts previous method, endpoint and body to retry)
app.post('/api/activities/replay/:id', async (req: Request, res: Response) => {
  const act = activities.find(a => a.id === req.params.id);
  if (!act) {
    return res.status(404).json({ error: 'Sync activity log not found.' });
  }

  const conn = connections.find(c => c.id === act.connectionId);
  if (!conn) {
    return res.status(404).json({ error: 'Associated connection is missing or deleted.' });
  }

  // Emulate request
  const mockHeaders = {
    'Content-Type': 'application/scim+json',
    'Authorization': `Bearer ${conn.token}`
  };

  try {
    const response = await fetch(`http://127.0.0.1:3000${act.url}`, {
      method: act.method,
      headers: mockHeaders,
      body: act.method !== 'GET' && act.method !== 'DELETE' && act.requestBody ? JSON.stringify(act.requestBody) : undefined
    });

    const status = response.status;
    let resBody: any = null;
    try {
      resBody = await response.json();
    } catch {
      resBody = '';
    }

    res.json({
      success: true,
      status,
      body: resBody
    });
  } catch (err: any) {
    res.status(500).json({ error: `Replay failed: ${err.message}` });
  }
});

// Live Dev Console Manual Request Direct Injection Handler
app.post('/api/console/test', async (req: Request, res: Response) => {
  const { connectionId, method, path: requestPath, headers, body } = req.body;
  const conn = connections.find(c => c.id === connectionId);

  if (!conn) {
    return res.status(404).json({ error: 'Selected connection profile does not exist.' });
  }

  // Create an internal fetch emulator to bypass real HTTP networking loops
  const mockHeaders: any = {
    'Content-Type': 'application/scim+json',
    'Authorization': `Bearer ${conn.token}`
  };

  if (headers && typeof headers === 'object') {
    Object.assign(mockHeaders, headers);
  }

  // Set up the local Express routing request emulation context
  // Send back full information about how our SCIM server processed it
  const urlPath = `/tenants/demo-tenant/scim/v2${requestPath}`;

  // Simply trigger internal routes using an HTTP mock loop, or we can mock evaluate in-place:
  // For ultimate reliability, let's run the logic right here or call Express handler.
  // Actually, we can just trigger a real HTTP loop to self on port 3000! Let's do that!
  try {
    const response = await fetch(`http://127.0.0.1:3000${urlPath}`, {
      method,
      headers: mockHeaders,
      body: method !== 'GET' && method !== 'DELETE' ? JSON.stringify(body) : undefined
    });

    const status = response.status;
    let resBody: any = null;
    try {
      resBody = await response.json();
    } catch {
      resBody = '';
    }

    res.json({
      status,
      headers: Object.fromEntries(response.headers.entries()),
      body: resBody
    });
  } catch (err: any) {
    res.status(500).json({ error: `Sandbox API emulator failed: ${err.message}` });
  }
});


// ==========================================
// STATIC FRONTEND ASSETS AND VITE INTEGRATION
// ==========================================

async function startServer() {
  if (process.env.NODE_ENV !== 'production') {
    // Integrate Vite as a dev middleware
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: 'spa',
    });
    app.use(vite.middlewares);
  } else {
    // Serve production static assets from dist
    const distPath = path.join(process.cwd(), 'dist');
    app.use(express.static(distPath));
    app.get('*', (req: Request, res: Response) => {
      res.sendFile(path.join(distPath, 'index.html'));
    });
  }

  const PORT = 3000;
  app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server fully operational on http://0.0.0.0:${PORT}`);
    console.log(`SCIM Base Protocol Root: /tenants/{tenant_slug}/scim/v2`);
  });
}

startServer();
