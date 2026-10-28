import express from "express";
import path from "path";
import crypto from "crypto";
import { createServer as createViteServer } from "vite";
import { 
  ScimConnection, 
  UserRecord, 
  GroupRecord, 
  QuarantineRecord, 
  SyncEvent,
  OverviewMetrics
} from "./src/types";

const app = express();
const PORT = 3000;

// Enable JSON parser that also supports SCIM content type (application/scim+json)
app.use(express.json({ type: ["application/json", "application/scim+json"] }));
app.use(express.urlencoded({ extended: true }));

// ==========================================
// IN-MEMORY DATABASE STATE (MOCK DB)
// ==========================================
let connections: ScimConnection[] = [];
let users: UserRecord[] = [];
let groups: GroupRecord[] = [];
let quarantines: QuarantineRecord[] = [];
let events: SyncEvent[] = [];

// Helper to generate IDs
const generateId = (prefix: string) => `${prefix}_${crypto.randomBytes(6).toString("hex")}`;

// Helper to hash secrets
const hashSecret = (secret: string) => crypto.createHash("sha256").update(secret).digest("hex");

// Populate initial mock data
function resetDatabase() {
  const now = new Date();
  
  // 1. Initial Connections
  const oktaToken = "tgb_scim_live_okta_workforce_abc123xyz";
  const azureToken = "tgb_scim_live_azure_corporate_dir_987qwe";
  const workdayToken = "tgb_scim_live_workday_inbound_draft_456mnb";

  connections = [
    {
      connectionId: "conn_okta_hr",
      name: "Okta Workforce Identity Sync",
      sourceProfile: "okta",
      lifecycleState: "active",
      tokenSecretHash: hashSecret(oktaToken),
      createdAt: "2026-03-15T08:00:00Z",
      lastUsed: new Date(now.getTime() - 10 * 60 * 1000).toISOString(), // 10 mins ago
      totalManagedUsers: 42,
      totalManagedGroups: 4,
      errorRate: 0.8,
      baseScimUrl: "https://ais-dev-hsrwvfs24dud5lx37fvtmo-3000.us-east1.run.app/tenants/acme-corp/scim/v2",
      attributeMappings: [
        { sourcePath: "userName", targetField: "userName", ownership: "source-owned" },
        { sourcePath: "displayName", targetField: "displayName", ownership: "source-owned" },
        { sourcePath: "emails[type eq 'work'].value", targetField: "emails", ownership: "source-owned" },
        { sourcePath: "title", targetField: "title", ownership: "source-owned" },
        { sourcePath: "department", targetField: "department", ownership: "source-owned" },
        { sourcePath: "employeeNumber", targetField: "employeeNumber", ownership: "source-owned" }
      ],
      precedencePolicy: "quarantine-on-collision"
    },
    {
      connectionId: "conn_azure_ad",
      name: "Azure AD Corporate Directory",
      sourceProfile: "azure",
      lifecycleState: "active",
      tokenSecretHash: hashSecret(azureToken),
      createdAt: "2026-05-10T14:30:00Z",
      lastUsed: new Date(now.getTime() - 5 * 60 * 1000).toISOString(), // 5 mins ago
      totalManagedUsers: 18,
      totalManagedGroups: 2,
      errorRate: 1.2,
      baseScimUrl: "https://ais-dev-hsrwvfs24dud5lx37fvtmo-3000.us-east1.run.app/tenants/acme-corp/scim/v2",
      attributeMappings: [
        { sourcePath: "userName", targetField: "userName", ownership: "source-owned" },
        { sourcePath: "displayName", targetField: "displayName", ownership: "source-owned" },
        { sourcePath: "emails[primary eq true].value", targetField: "emails", ownership: "fill-if-empty" }
      ],
      precedencePolicy: "override"
    },
    {
      connectionId: "conn_workday",
      name: "Workday HR Inbound",
      sourceProfile: "workday",
      lifecycleState: "draft",
      tokenSecretHash: hashSecret(workdayToken),
      createdAt: "2026-07-01T09:15:00Z",
      lastUsed: "never",
      totalManagedUsers: 0,
      totalManagedGroups: 0,
      errorRate: 0.0,
      baseScimUrl: "https://ais-dev-hsrwvfs24dud5lx37fvtmo-3000.us-east1.run.app/tenants/acme-corp/scim/v2",
      attributeMappings: [
        { sourcePath: "userName", targetField: "userName", ownership: "source-owned" },
        { sourcePath: "emails[type eq 'work'].value", targetField: "emails", ownership: "source-owned" },
        { sourcePath: "employeeNumber", targetField: "employeeNumber", ownership: "source-owned" }
      ],
      precedencePolicy: "quarantine-on-collision"
    }
  ];

  // Store the raw tokens temporarily for one-time visual display in setup if needed, 
  // but since these are mock, we can show them on request.
  connections[0].tokenSecret = oktaToken;
  connections[1].tokenSecret = azureToken;
  connections[2].tokenSecret = workdayToken;

  // 2. Initial Users
  users = [
    {
      id: "usr_jane_doe",
      userName: "jane.doe@acme.com",
      displayName: "Jane Doe",
      emails: [{ value: "jane.doe@acme.com", type: "work", primary: true }],
      active: true,
      title: "Director of Engineering",
      department: "Engineering",
      organization: "Acme Corp",
      employeeNumber: "EMP-2041",
      createdAt: "2026-03-15T09:12:00Z",
      updatedAt: "2026-07-11T12:00:00Z",
      sourceConnectionId: "conn_okta_hr",
      externalId: "okta_usr_jane_101",
      scimId: "usr_jane_doe",
      sourceStatus: "linked",
      originalPayloadDigest: "md5:789bcf234e890acbd09"
    },
    {
      id: "usr_john_smith",
      userName: "john.smith@acme.com",
      displayName: "John Smith",
      emails: [{ value: "john.smith@acme.com", type: "work", primary: true }],
      active: true,
      title: "Staff Security Engineer",
      department: "Security",
      organization: "Acme Corp",
      employeeNumber: "EMP-4052",
      createdAt: "2026-03-15T09:15:00Z",
      updatedAt: "2026-07-10T15:20:00Z",
      sourceConnectionId: "conn_okta_hr",
      externalId: "okta_usr_john_102",
      scimId: "usr_john_smith",
      sourceStatus: "linked",
      originalPayloadDigest: "md5:123ab8923fd780fcca1"
    },
    {
      id: "usr_alice_j",
      userName: "alice.johnson@acme.com",
      displayName: "Alice Johnson",
      emails: [{ value: "alice.johnson@acme.com", type: "work", primary: true }],
      active: true,
      title: "Product Manager",
      department: "Product Management",
      organization: "Acme Corp",
      employeeNumber: "EMP-3012",
      createdAt: "2026-05-10T14:40:00Z",
      updatedAt: "2026-05-10T14:40:00Z",
      sourceConnectionId: "conn_azure_ad",
      externalId: "azure_usr_alice_301",
      scimId: "usr_alice_j",
      sourceStatus: "linked",
      originalPayloadDigest: "md5:fff328711eecbc78d0a"
    },
    {
      id: "usr_bob_w",
      userName: "bob.wilson@acme.com",
      displayName: "Bob Wilson",
      emails: [{ value: "bob.wilson@acme.com", type: "work", primary: true }],
      active: false,
      title: "Senior UX Designer",
      department: "Product Design",
      organization: "Acme Corp",
      employeeNumber: "EMP-9022",
      createdAt: "2026-05-10T14:45:00Z",
      updatedAt: "2026-07-01T10:00:00Z",
      sourceConnectionId: "conn_azure_ad",
      externalId: "azure_usr_bob_302",
      scimId: "usr_bob_w",
      sourceStatus: "inactive",
      originalPayloadDigest: "md5:abc8812328df8f9024c"
    }
  ];

  // 3. Initial Groups
  groups = [
    {
      id: "grp_eng_team",
      displayName: "Engineering Department",
      externalId: "okta_grp_eng_501",
      scimId: "grp_eng_team",
      sourceConnectionId: "conn_okta_hr",
      members: [{ value: "usr_jane_doe" }],
      mappedRoles: ["Developer", "Internal System Access"],
      mappedEntitlements: ["GitHub Developer Seat", "Slack Premium License"],
      createdAt: "2026-03-15T09:20:00Z",
      updatedAt: "2026-03-15T09:20:00Z"
    },
    {
      id: "grp_security_team",
      displayName: "Security Operations",
      externalId: "okta_grp_sec_502",
      scimId: "grp_security_team",
      sourceConnectionId: "conn_okta_hr",
      members: [{ value: "usr_john_smith" }],
      mappedRoles: ["Security Analyst", "Super Admin Access"],
      mappedEntitlements: ["AWS Security Admin Role", "CloudTrail Auditing Tool"],
      createdAt: "2026-03-15T09:25:00Z",
      updatedAt: "2026-07-11T12:00:00Z"
    },
    {
      id: "grp_design_team",
      displayName: "Design & Research",
      externalId: "azure_grp_design_701",
      scimId: "grp_design_team",
      sourceConnectionId: "conn_azure_ad",
      members: [{ value: "usr_bob_w" }],
      mappedRoles: ["UX Lead Contributor"],
      mappedEntitlements: ["Figma Enterprise Seat"],
      createdAt: "2026-05-10T14:50:00Z",
      updatedAt: "2026-05-10T14:50:00Z"
    }
  ];

  // 4. Initial Quarantines
  quarantines = [
    {
      id: "qtn_101",
      connectionId: "conn_okta_hr",
      connectionName: "Okta Workforce Identity Sync",
      resourceType: "User",
      scimId: "okta_temp_charles",
      externalId: "okta_usr_charles_103",
      payload: {
        schemas: ["urn:ietf:params:scim:schemas:core:2.0:User"],
        userName: "jane.doe@acme.com",
        name: { formatted: "Charles Doe", familyName: "Doe", givenName: "Charles" },
        emails: [{ value: "jane.doe@acme.com", primary: true, type: "work" }],
        active: true,
        title: "Principal Architect"
      },
      reason: "Inbound username collision: 'jane.doe@acme.com' already owned by canonical user 'Jane Doe' (usr_jane_doe)",
      conflictWithId: "usr_jane_doe",
      conflictField: "userName",
      conflictValue: "jane.doe@acme.com",
      timestamp: "2026-07-11T18:30:15Z"
    }
  ];

  // 5. Initial Sync Events
  events = [
    {
      id: "evt_1",
      timestamp: "2026-07-11T22:15:40Z",
      connectionId: "conn_azure_ad",
      connectionName: "Azure AD Corporate Directory",
      clientIp: "40.112.54.120",
      operation: "GET",
      resourceType: "Schema",
      status: "success",
      responseCode: 200,
      rawRequest: "GET /tenants/acme-corp/scim/v2/Schemas HTTP/1.1\nHost: ais-dev-hsrwvfs24dud5lx37fvtmo-3000.us-east1.run.app\nAuthorization: Bearer tgb_scim_live_azure_corporate_dir_***",
      rawResponse: JSON.stringify({ schemas: ["urn:ietf:params:scim:api:messages:2.0:ListResponse"], totalResults: 2 }, null, 2),
      latencyMs: 8,
      correlationId: "corr_98ab7612f0",
      summary: "Metadata Schema discovery check by Azure AD client."
    },
    {
      id: "evt_2",
      timestamp: "2026-07-11T22:15:35Z",
      connectionId: "conn_azure_ad",
      connectionName: "Azure AD Corporate Directory",
      clientIp: "40.112.54.120",
      operation: "GET",
      resourceType: "User",
      resourceId: "usr_alice_j",
      status: "success",
      responseCode: 200,
      rawRequest: "GET /tenants/acme-corp/scim/v2/Users?filter=userName eq \"alice.johnson@acme.com\" HTTP/1.1",
      rawResponse: JSON.stringify({ schemas: ["urn:ietf:params:scim:api:messages:2.0:ListResponse"], totalResults: 1 }, null, 2),
      latencyMs: 15,
      correlationId: "corr_bc87e51a23",
      summary: "Lookup of User 'alice.johnson@acme.com' returning 1 matching resource."
    },
    {
      id: "evt_3",
      timestamp: "2026-07-11T22:05:12Z",
      connectionId: "conn_okta_hr",
      connectionName: "Okta Workforce Identity Sync",
      clientIp: "3.14.88.204",
      operation: "PATCH",
      resourceType: "Group",
      resourceId: "grp_security_team",
      status: "success",
      responseCode: 200,
      rawRequest: "PATCH /tenants/acme-corp/scim/v2/Groups/grp_security_team HTTP/1.1\nContent-Type: application/scim+json\n\n" + JSON.stringify({
        schemas: ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
        Operations: [{ op: "add", path: "members", value: [{ value: "usr_john_smith" }] }]
      }, null, 2),
      rawResponse: JSON.stringify({ id: "grp_security_team", displayName: "Security Operations", members: [{ value: "usr_john_smith" }] }, null, 2),
      latencyMs: 38,
      correlationId: "corr_aa45bc890f",
      summary: "Group membership patch addition: 'usr_john_smith' added to group 'Security Operations'."
    },
    {
      id: "evt_4",
      timestamp: "2026-07-11T22:05:10Z",
      connectionId: "conn_okta_hr",
      connectionName: "Okta Workforce Identity Sync",
      clientIp: "3.14.88.204",
      operation: "UPDATE",
      resourceType: "User",
      resourceId: "usr_john_smith",
      status: "success",
      responseCode: 200,
      rawRequest: "PUT /tenants/acme-corp/scim/v2/Users/usr_john_smith HTTP/1.1\n\n" + JSON.stringify({
        userName: "john.smith@acme.com",
        displayName: "John Smith",
        title: "Staff Security Engineer",
        department: "Security",
        active: true
      }, null, 2),
      rawResponse: JSON.stringify({ id: "usr_john_smith", userName: "john.smith@acme.com", active: true }, null, 2),
      latencyMs: 42,
      correlationId: "corr_09bbef31d4",
      summary: "Full replacement PUT update for user 'john.smith@acme.com' from Okta."
    },
    {
      id: "evt_5",
      timestamp: "2026-07-11T18:30:15Z",
      connectionId: "conn_okta_hr",
      connectionName: "Okta Workforce Identity Sync",
      clientIp: "3.14.88.204",
      operation: "CREATE",
      resourceType: "User",
      status: "quarantined",
      responseCode: 409,
      rawRequest: "POST /tenants/acme-corp/scim/v2/Users HTTP/1.1\nContent-Type: application/scim+json\n\n" + JSON.stringify({
        schemas: ["urn:ietf:params:scim:schemas:core:2.0:User"],
        userName: "jane.doe@acme.com",
        emails: [{ value: "jane.doe@acme.com", primary: true, type: "work" }],
        active: true,
        title: "Principal Architect"
      }, null, 2),
      rawResponse: JSON.stringify({
        schemas: ["urn:ietf:params:scim:api:messages:2.0:Error"],
        status: "409",
        scimType: "uniqueness",
        detail: "Inbound username collision: 'jane.doe@acme.com' already owned by canonical user 'Jane Doe' (usr_jane_doe)"
      }, null, 2),
      latencyMs: 24,
      correlationId: "corr_77491bbca1",
      summary: "Attempted User creation with username 'jane.doe@acme.com' resulted in a uniqueness collision. Quarantined for administrator evaluation."
    },
    {
      id: "evt_6",
      timestamp: "2026-07-11T12:00:00Z",
      connectionId: "conn_okta_hr",
      connectionName: "Okta Workforce Identity Sync",
      clientIp: "3.14.88.204",
      operation: "GET",
      resourceType: "Config",
      status: "success",
      responseCode: 200,
      rawRequest: "GET /tenants/acme-corp/scim/v2/ServiceProviderConfig HTTP/1.1",
      rawResponse: JSON.stringify({ schemas: ["urn:ietf:params:scim:schemas:core:2.0:ServiceProviderConfig"], patch: { supported: true } }, null, 2),
      latencyMs: 4,
      correlationId: "corr_3321efbcad",
      summary: "Service Provider Configuration discovery retrieval by Okta connection."
    }
  ];
}

// Initial build
resetDatabase();

// ==========================================
// SCIM API MIDDLEWARE - SECURITY & AUTH
// ==========================================
const authenticateScimClient = (req: any, res: any, next: any) => {
  const authHeader = req.headers["authorization"];
  if (!authHeader || !authHeader.startsWith("Bearer ")) {
    const errorBody = {
      schemas: ["urn:ietf:params:scim:api:messages:2.0:Error"],
      status: "401",
      detail: "Missing SCIM bearer authentication token"
    };
    
    // Log auth failure
    const correlationId = `corr_auth_${crypto.randomBytes(4).toString("hex")}`;
    events.unshift({
      id: generateId("evt"),
      timestamp: new Date().toISOString(),
      connectionId: "unknown",
      connectionName: "Unauthenticated Client",
      clientIp: req.ip || "127.0.0.1",
      operation: req.method as any,
      resourceType: "Config",
      status: "failure",
      responseCode: 401,
      rawRequest: `${req.method} ${req.originalUrl}\nHeaders: ${JSON.stringify(req.headers, null, 2)}`,
      rawResponse: JSON.stringify(errorBody, null, 2),
      latencyMs: 1,
      correlationId,
      summary: `Failed authentication. Access denied.`
    });

    return res.status(401).header("Content-Type", "application/scim+json").json(errorBody);
  }

  const token = authHeader.substring(7).trim();
  const tokenHash = hashSecret(token);
  
  const conn = connections.find(c => c.tokenSecretHash === tokenHash);
  
  if (!conn) {
    const errorBody = {
      schemas: ["urn:ietf:params:scim:api:messages:2.0:Error"],
      status: "401",
      detail: "Invalid SCIM Bearer token"
    };

    const correlationId = `corr_auth_${crypto.randomBytes(4).toString("hex")}`;
    events.unshift({
      id: generateId("evt"),
      timestamp: new Date().toISOString(),
      connectionId: "unknown",
      connectionName: "Invalid Token",
      clientIp: req.ip || "127.0.0.1",
      operation: req.method as any,
      resourceType: "Config",
      status: "failure",
      responseCode: 401,
      rawRequest: `${req.method} ${req.originalUrl}`,
      rawResponse: JSON.stringify(errorBody, null, 2),
      latencyMs: 2,
      correlationId,
      summary: `Failed SCIM authentication: Provided token does not match any registered connection.`
    });

    return res.status(401).header("Content-Type", "application/scim+json").json(errorBody);
  }

  if (conn.lifecycleState === "suspended") {
    const errorBody = {
      schemas: ["urn:ietf:params:scim:api:messages:2.0:Error"],
      status: "403",
      detail: "Forbidden: Provisioning connection has been suspended by tenant administrator"
    };

    const correlationId = `corr_auth_${crypto.randomBytes(4).toString("hex")}`;
    events.unshift({
      id: generateId("evt"),
      timestamp: new Date().toISOString(),
      connectionId: conn.connectionId,
      connectionName: conn.name,
      clientIp: req.ip || "127.0.0.1",
      operation: req.method as any,
      resourceType: "Config",
      status: "failure",
      responseCode: 403,
      rawRequest: `${req.method} ${req.originalUrl}`,
      rawResponse: JSON.stringify(errorBody, null, 2),
      latencyMs: 2,
      correlationId,
      summary: `SCIM access blocked: Connection '${conn.name}' is currently suspended.`
    });

    return res.status(403).header("Content-Type", "application/scim+json").json(errorBody);
  }

  // Bind active connection and update lastUsed
  req.connection = conn;
  conn.lastUsed = new Date().toISOString();
  next();
};

// ==========================================
// SCIM 2.0 PROTOCOL ENGINE ENDPOINTS
// ==========================================
const scimRouter = express.Router({ mergeParams: true });

// Discovery: Service Provider Config
scimRouter.get("/ServiceProviderConfig", (req: any, res) => {
  const start = Date.now();
  const config = {
    schemas: ["urn:ietf:params:scim:schemas:core:2.0:ServiceProviderConfig"],
    documentationUrl: "https://ais-dev-hsrwvfs24dud5lx37fvtmo-3000.us-east1.run.app/docs/scim",
    patch: { supported: true },
    bulk: { supported: false, maxOperations: 0, maxPayloadSize: 0 },
    filter: { supported: true, maxResults: 200 },
    changePassword: { supported: false },
    sort: { supported: false },
    etag: { supported: true },
    authenticationSchemes: [
      {
        name: "OAuth Bearer Token",
        description: "Standard HTTP Bearer authentication token issued in Tigrbl SCIM setup panel",
        specUri: "https://tools.ietf.org/html/rfc6750",
        type: "oauth2",
        primary: true
      }
    ]
  };

  res.header("Content-Type", "application/scim+json");
  res.json(config);

  const conn = req.connection;
  events.unshift({
    id: generateId("evt"),
    timestamp: new Date().toISOString(),
    connectionId: conn.connectionId,
    connectionName: conn.name,
    clientIp: req.ip || "127.0.0.1",
    operation: "GET",
    resourceType: "Config",
    status: "success",
    responseCode: 200,
    rawRequest: `GET ${req.originalUrl}`,
    rawResponse: JSON.stringify(config, null, 2),
    latencyMs: Date.now() - start,
    correlationId: `corr_${crypto.randomBytes(5).toString("hex")}`,
    summary: `Retrieved Service Provider Configuration.`
  });
});

// Discovery: Resource Types
scimRouter.get("/ResourceTypes", (req: any, res) => {
  const start = Date.now();
  const resourceTypes = {
    schemas: ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
    totalResults: 2,
    itemsPerPage: 2,
    startIndex: 1,
    Resources: [
      {
        schemas: ["urn:ietf:params:scim:schemas:core:2.0:ResourceType"],
        id: "User",
        name: "User",
        endpoint: "/Users",
        description: "User Account Resource",
        schema: "urn:ietf:params:scim:schemas:core:2.0:User",
        schemaExtensions: []
      },
      {
        schemas: ["urn:ietf:params:scim:schemas:core:2.0:ResourceType"],
        id: "Group",
        name: "Group",
        endpoint: "/Groups",
        description: "Group Resource",
        schema: "urn:ietf:params:scim:schemas:core:2.0:Group"
      }
    ]
  };

  res.header("Content-Type", "application/scim+json");
  res.json(resourceTypes);

  const conn = req.connection;
  events.unshift({
    id: generateId("evt"),
    timestamp: new Date().toISOString(),
    connectionId: conn.connectionId,
    connectionName: conn.name,
    clientIp: req.ip || "127.0.0.1",
    operation: "GET",
    resourceType: "ResourceType",
    status: "success",
    responseCode: 200,
    rawRequest: `GET ${req.originalUrl}`,
    rawResponse: JSON.stringify(resourceTypes, null, 2),
    latencyMs: Date.now() - start,
    correlationId: `corr_${crypto.randomBytes(5).toString("hex")}`,
    summary: `Retrieved SCIM Resource Types list.`
  });
});

// Discovery: Schemas
scimRouter.get("/Schemas", (req: any, res) => {
  const start = Date.now();
  const schemas = {
    schemas: ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
    totalResults: 2,
    Resources: [
      {
        id: "urn:ietf:params:scim:schemas:core:2.0:User",
        name: "User",
        description: "Core User Schema",
        attributes: [
          { name: "userName", type: "string", multiValued: false, required: true, caseExact: false, mutability: "readWrite" },
          { name: "displayName", type: "string", multiValued: false, required: false, caseExact: false, mutability: "readWrite" },
          { name: "emails", type: "complex", multiValued: true, required: false, subAttributes: [
            { name: "value", type: "string", mutability: "readWrite" },
            { name: "type", type: "string", mutability: "readWrite" },
            { name: "primary", type: "boolean", mutability: "readWrite" }
          ]}
        ]
      },
      {
        id: "urn:ietf:params:scim:schemas:core:2.0:Group",
        name: "Group",
        description: "Core Group Schema",
        attributes: [
          { name: "displayName", type: "string", multiValued: false, required: true, caseExact: false, mutability: "readWrite" },
          { name: "members", type: "complex", multiValued: true, required: false, subAttributes: [
            { name: "value", type: "string", mutability: "immutable" },
            { name: "display", type: "string", mutability: "readOnly" }
          ]}
        ]
      }
    ]
  };

  res.header("Content-Type", "application/scim+json");
  res.json(schemas);

  const conn = req.connection;
  events.unshift({
    id: generateId("evt"),
    timestamp: new Date().toISOString(),
    connectionId: conn.connectionId,
    connectionName: conn.name,
    clientIp: req.ip || "127.0.0.1",
    operation: "GET",
    resourceType: "Schema",
    status: "success",
    responseCode: 200,
    rawRequest: `GET ${req.originalUrl}`,
    rawResponse: JSON.stringify(schemas, null, 2),
    latencyMs: Date.now() - start,
    correlationId: `corr_${crypto.randomBytes(5).toString("hex")}`,
    summary: `Retrieved SCIM Schemas list.`
  });
});

// SCIM Helper to translate UserRecord to SCIM User JSON
function toScimUser(user: UserRecord): any {
  return {
    schemas: ["urn:ietf:params:scim:schemas:core:2.0:User"],
    id: user.id,
    externalId: user.externalId,
    userName: user.userName,
    displayName: user.displayName,
    emails: user.emails,
    active: user.active,
    title: user.title,
    department: user.department,
    organization: user.organization,
    employeeNumber: user.employeeNumber,
    meta: {
      resourceType: "User",
      created: user.createdAt,
      lastModified: user.updatedAt,
      version: `W/"${hashSecret(user.updatedAt + user.id).substring(0, 8)}"`
    }
  };
}

// SCIM Helper to translate GroupRecord to SCIM Group JSON
function toScimGroup(group: GroupRecord): any {
  const resolvedMembers = group.members.map(m => {
    const u = users.find(usr => usr.id === m.value);
    return {
      value: m.value,
      display: u ? u.displayName : m.display || m.value
    };
  });

  return {
    schemas: ["urn:ietf:params:scim:schemas:core:2.0:Group"],
    id: group.id,
    externalId: group.externalId,
    displayName: group.displayName,
    members: resolvedMembers,
    meta: {
      resourceType: "Group",
      created: group.createdAt,
      lastModified: group.updatedAt,
      version: `W/"${hashSecret(group.updatedAt + group.id).substring(0, 8)}"`
    }
  };
}

// USERS: Read/Search/List
scimRouter.get("/Users", (req: any, res) => {
  const start = Date.now();
  const filter = req.query.filter as string;
  const startIndex = parseInt(req.query.startIndex as string) || 1;
  const count = parseInt(req.query.count as string) || 50;

  let filtered = [...users];

  if (filter) {
    // Basic filter parsing: userName eq "..." or externalId eq "..."
    const usernameEqMatch = filter.match(/userName\s+eq\s+["'](.+?)["']/i);
    const externalIdEqMatch = filter.match(/externalId\s+eq\s+["'](.+?)["']/i);
    const idEqMatch = filter.match(/id\s+eq\s+["'](.+?)["']/i);

    if (usernameEqMatch) {
      const emailVal = usernameEqMatch[1].toLowerCase();
      filtered = filtered.filter(u => u.userName.toLowerCase() === emailVal);
    } else if (externalIdEqMatch) {
      const extVal = externalIdEqMatch[1];
      filtered = filtered.filter(u => u.externalId === extVal);
    } else if (idEqMatch) {
      const idVal = idEqMatch[1];
      filtered = filtered.filter(u => u.id === idVal);
    } else {
      // Return 400 for unsupported filter grammar
      const err = {
        schemas: ["urn:ietf:params:scim:api:messages:2.0:Error"],
        status: "400",
        scimType: "invalidFilter",
        detail: `Unsupported filter query expression: "${filter}". At minimum, eq query on userName, externalId, or id is supported.`
      };
      return res.status(400).header("Content-Type", "application/scim+json").json(err);
    }
  }

  const totalResults = filtered.length;
  // Apply pagination (SCIM startIndex is 1-based)
  const paginated = filtered.slice(startIndex - 1, startIndex - 1 + count);

  const listResponse = {
    schemas: ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
    totalResults,
    itemsPerPage: paginated.length,
    startIndex,
    Resources: paginated.map(u => toScimUser(u))
  };

  res.header("Content-Type", "application/scim+json");
  res.json(listResponse);

  const conn = req.connection;
  events.unshift({
    id: generateId("evt"),
    timestamp: new Date().toISOString(),
    connectionId: conn.connectionId,
    connectionName: conn.name,
    clientIp: req.ip || "127.0.0.1",
    operation: "GET",
    resourceType: "User",
    status: "success",
    responseCode: 200,
    rawRequest: `GET ${req.originalUrl}`,
    rawResponse: JSON.stringify(listResponse, null, 2),
    latencyMs: Date.now() - start,
    correlationId: `corr_${crypto.randomBytes(5).toString("hex")}`,
    summary: `Queried SCIM Users. Filter: "${filter || 'None'}", Results: ${totalResults}.`
  });
});

// USERS: Create (POST)
scimRouter.post("/Users", (req: any, res) => {
  const start = Date.now();
  const conn = req.connection as ScimConnection;
  const payload = req.body;

  const correlationId = `corr_${crypto.randomBytes(5).toString("hex")}`;

  if (!payload.userName) {
    const err = {
      schemas: ["urn:ietf:params:scim:api:messages:2.0:Error"],
      status: "400",
      detail: "Missing required attribute: userName"
    };
    events.unshift({
      id: generateId("evt"),
      timestamp: new Date().toISOString(),
      connectionId: conn.connectionId,
      connectionName: conn.name,
      clientIp: req.ip || "127.0.0.1",
      operation: "CREATE",
      resourceType: "User",
      status: "failure",
      responseCode: 400,
      rawRequest: `POST /Users\n\n${JSON.stringify(payload, null, 2)}`,
      rawResponse: JSON.stringify(err, null, 2),
      latencyMs: Date.now() - start,
      correlationId,
      summary: "Failed User creation: Missing userName."
    });
    return res.status(400).header("Content-Type", "application/scim+json").json(err);
  }

  const userName = payload.userName.toLowerCase();
  
  // Check for uniqueness conflict
  const existingUser = users.find(u => u.userName.toLowerCase() === userName);
  
  if (existingUser) {
    if (conn.precedencePolicy === "quarantine-on-collision") {
      // Place request into quarantine and return standard 409 conflict
      const qId = generateId("qtn");
      const qRecord: QuarantineRecord = {
        id: qId,
        connectionId: conn.connectionId,
        connectionName: conn.name,
        resourceType: "User",
        scimId: payload.id || generateId("usr_temp"),
        externalId: payload.externalId,
        payload,
        reason: `Inbound username collision: '${userName}' already owned by canonical user '${existingUser.displayName}' (${existingUser.id})`,
        conflictWithId: existingUser.id,
        conflictField: "userName",
        conflictValue: userName,
        timestamp: new Date().toISOString()
      };
      
      quarantines.unshift(qRecord);
      
      const scimErr = {
        schemas: ["urn:ietf:params:scim:api:messages:2.0:Error"],
        status: "409",
        scimType: "uniqueness",
        detail: qRecord.reason
      };

      events.unshift({
        id: generateId("evt"),
        timestamp: new Date().toISOString(),
        connectionId: conn.connectionId,
        connectionName: conn.name,
        clientIp: req.ip || "127.0.0.1",
        operation: "CREATE",
        resourceType: "User",
        status: "quarantined",
        responseCode: 409,
        rawRequest: `POST /Users\n\n${JSON.stringify(payload, null, 2)}`,
        rawResponse: JSON.stringify(scimErr, null, 2),
        latencyMs: Date.now() - start,
        correlationId,
        summary: `Username collision on '${userName}'. Connection configuration routed this request to the Quarantine and rejected it with 409 Conflict.`
      });

      return res.status(409).header("Content-Type", "application/scim+json").json(scimErr);
    } else if (conn.precedencePolicy === "override") {
      // Override: Modify existing user source link and overwrite fields!
      existingUser.sourceConnectionId = conn.connectionId;
      existingUser.externalId = payload.externalId || existingUser.externalId;
      existingUser.displayName = payload.displayName || existingUser.displayName;
      existingUser.active = payload.active !== undefined ? payload.active : true;
      existingUser.title = payload.title || existingUser.title;
      existingUser.department = payload.department || existingUser.department;
      existingUser.updatedAt = new Date().toISOString();
      existingUser.sourceStatus = existingUser.active ? "linked" : "inactive";

      const scimUser = toScimUser(existingUser);
      events.unshift({
        id: generateId("evt"),
        timestamp: new Date().toISOString(),
        connectionId: conn.connectionId,
        connectionName: conn.name,
        clientIp: req.ip || "127.0.0.1",
        operation: "CREATE",
        resourceId: existingUser.id,
        resourceType: "User",
        status: "success",
        responseCode: 200,
        rawRequest: `POST /Users\n\n${JSON.stringify(payload, null, 2)}`,
        rawResponse: JSON.stringify(scimUser, null, 2),
        latencyMs: Date.now() - start,
        correlationId,
        summary: `Precedence policy 'override' matched existing user '${userName}'. Overwrote authoritative attributes.`
      });

      return res.status(200).header("Content-Type", "application/scim+json").json(scimUser);
    } else {
      // Ignore / reject simple 409
      const err = {
        schemas: ["urn:ietf:params:scim:api:messages:2.0:Error"],
        status: "409",
        scimType: "uniqueness",
        detail: `Collision detected: userName '${userName}' is already taken.`
      };
      
      events.unshift({
        id: generateId("evt"),
        timestamp: new Date().toISOString(),
        connectionId: conn.connectionId,
        connectionName: conn.name,
        clientIp: req.ip || "127.0.0.1",
        operation: "CREATE",
        resourceType: "User",
        status: "failure",
        responseCode: 409,
        rawRequest: `POST /Users\n\n${JSON.stringify(payload, null, 2)}`,
        rawResponse: JSON.stringify(err, null, 2),
        latencyMs: Date.now() - start,
        correlationId,
        summary: `Collision detected on '${userName}'. Request rejected.`
      });

      return res.status(409).header("Content-Type", "application/scim+json").json(err);
    }
  }

  // Otherwise, create user
  const newUserId = generateId("usr");
  const newRecord: UserRecord = {
    id: newUserId,
    userName,
    displayName: payload.displayName || userName.split("@")[0],
    emails: payload.emails || [{ value: userName, primary: true }],
    active: payload.active !== undefined ? payload.active : true,
    title: payload.title,
    department: payload.department,
    organization: payload.organization || "Acme Corp",
    employeeNumber: payload.employeeNumber,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    sourceConnectionId: conn.connectionId,
    externalId: payload.externalId,
    scimId: newUserId,
    sourceStatus: (payload.active !== undefined ? payload.active : true) ? "linked" : "inactive",
    originalPayloadDigest: `sha256:${hashSecret(JSON.stringify(payload))}`
  };

  users.push(newRecord);
  
  // Increment managed counter
  conn.totalManagedUsers += 1;

  const responseScim = toScimUser(newRecord);
  res.status(201).header("Content-Type", "application/scim+json").json(responseScim);

  events.unshift({
    id: generateId("evt"),
    timestamp: new Date().toISOString(),
    connectionId: conn.connectionId,
    connectionName: conn.name,
    clientIp: req.ip || "127.0.0.1",
    operation: "CREATE",
    resourceId: newUserId,
    resourceType: "User",
    status: "success",
    responseCode: 201,
    rawRequest: `POST /Users\n\n${JSON.stringify(payload, null, 2)}`,
    rawResponse: JSON.stringify(responseScim, null, 2),
    latencyMs: Date.now() - start,
    correlationId,
    summary: `Successfully provisioned new canonical user '${newRecord.displayName}' (${newUserId}).`
  });
});

// USERS: Read Individual (GET)
scimRouter.get("/Users/:id", (req: any, res) => {
  const start = Date.now();
  const conn = req.connection;
  const user = users.find(u => u.id === req.params.id);

  if (!user) {
    const err = {
      schemas: ["urn:ietf:params:scim:api:messages:2.0:Error"],
      status: "404",
      detail: `User with identifier '${req.params.id}' not found.`
    };
    return res.status(404).header("Content-Type", "application/scim+json").json(err);
  }

  const response = toScimUser(user);
  res.header("Content-Type", "application/scim+json");
  res.json(response);

  events.unshift({
    id: generateId("evt"),
    timestamp: new Date().toISOString(),
    connectionId: conn.connectionId,
    connectionName: conn.name,
    clientIp: req.ip || "127.0.0.1",
    operation: "GET",
    resourceId: user.id,
    resourceType: "User",
    status: "success",
    responseCode: 200,
    rawRequest: `GET ${req.originalUrl}`,
    rawResponse: JSON.stringify(response, null, 2),
    latencyMs: Date.now() - start,
    correlationId: `corr_${crypto.randomBytes(5).toString("hex")}`,
    summary: `Fetched detailed representation of User '${user.displayName}'.`
  });
});

// USERS: Replace (PUT)
scimRouter.put("/Users/:id", (req: any, res) => {
  const start = Date.now();
  const conn = req.connection;
  const payload = req.body;
  const user = users.find(u => u.id === req.params.id);

  if (!user) {
    const err = {
      schemas: ["urn:ietf:params:scim:api:messages:2.0:Error"],
      status: "404",
      detail: `User with identifier '${req.params.id}' not found for replacement.`
    };
    return res.status(404).header("Content-Type", "application/scim+json").json(err);
  }

  // Update properties according to PUT rules (replace everything)
  user.displayName = payload.displayName || user.userName;
  user.emails = payload.emails || [];
  user.active = payload.active !== undefined ? payload.active : true;
  user.title = payload.title || undefined;
  user.department = payload.department || undefined;
  user.organization = payload.organization || undefined;
  user.employeeNumber = payload.employeeNumber || undefined;
  user.updatedAt = new Date().toISOString();
  user.sourceStatus = user.active ? "linked" : "inactive";

  const response = toScimUser(user);
  res.header("Content-Type", "application/scim+json");
  res.json(response);

  events.unshift({
    id: generateId("evt"),
    timestamp: new Date().toISOString(),
    connectionId: conn.connectionId,
    connectionName: conn.name,
    clientIp: req.ip || "127.0.0.1",
    operation: "UPDATE",
    resourceId: user.id,
    resourceType: "User",
    status: "success",
    responseCode: 200,
    rawRequest: `PUT ${req.originalUrl}\n\n${JSON.stringify(payload, null, 2)}`,
    rawResponse: JSON.stringify(response, null, 2),
    latencyMs: Date.now() - start,
    correlationId: `corr_${crypto.randomBytes(5).toString("hex")}`,
    summary: `PUT replaced User '${user.displayName}' properties.`
  });
});

// USERS: Patch (PATCH)
scimRouter.patch("/Users/:id", (req: any, res) => {
  const start = Date.now();
  const conn = req.connection;
  const payload = req.body;
  const user = users.find(u => u.id === req.params.id);

  const correlationId = `corr_${crypto.randomBytes(5).toString("hex")}`;

  if (!user) {
    const err = {
      schemas: ["urn:ietf:params:scim:api:messages:2.0:Error"],
      status: "404",
      detail: `User with identifier '${req.params.id}' not found for patch operation.`
    };
    return res.status(404).header("Content-Type", "application/scim+json").json(err);
  }

  const ops = payload.Operations;
  if (!ops || !Array.isArray(ops)) {
    const err = {
      schemas: ["urn:ietf:params:scim:api:messages:2.0:Error"],
      status: "400",
      detail: "Invalid patch payload: Operations array is required."
    };
    return res.status(400).header("Content-Type", "application/scim+json").json(err);
  }

  // Iterate operations
  try {
    for (const op of ops) {
      const type = op.op.toLowerCase(); // 'add', 'replace', 'remove'
      const pathValue = op.path;
      const val = op.value;

      if (type === "replace" || type === "add") {
        if (!pathValue && typeof val === "object") {
          // Object containing properties
          if (val.active !== undefined) user.active = val.active;
          if (val.displayName) user.displayName = val.displayName;
          if (val.title) user.title = val.title;
          if (val.department) user.department = val.department;
          if (val.emails) user.emails = val.emails;
        } else if (pathValue === "active") {
          user.active = val === true || val === "true";
        } else if (pathValue === "displayName") {
          user.displayName = val;
        } else if (pathValue === "title") {
          user.title = val;
        } else if (pathValue === "department") {
          user.department = val;
        } else if (pathValue === "emails") {
          user.emails = Array.isArray(val) ? val : [val];
        }
      } else if (type === "remove") {
        if (pathValue === "title") {
          user.title = undefined;
        } else if (pathValue === "department") {
          user.department = undefined;
        }
      }
    }

    user.updatedAt = new Date().toISOString();
    user.sourceStatus = user.active ? "linked" : "inactive";

    const response = toScimUser(user);
    res.header("Content-Type", "application/scim+json");
    res.json(response);

    events.unshift({
      id: generateId("evt"),
      timestamp: new Date().toISOString(),
      connectionId: conn.connectionId,
      connectionName: conn.name,
      clientIp: req.ip || "127.0.0.1",
      operation: "PATCH",
      resourceId: user.id,
      resourceType: "User",
      status: "success",
      responseCode: 200,
      rawRequest: `PATCH ${req.originalUrl}\n\n${JSON.stringify(payload, null, 2)}`,
      rawResponse: JSON.stringify(response, null, 2),
      latencyMs: Date.now() - start,
      correlationId,
      summary: `Evaluated PATCH update on User '${user.displayName}'. State synchronized.`
    });
  } catch (error: any) {
    const err = {
      schemas: ["urn:ietf:params:scim:api:messages:2.0:Error"],
      status: "400",
      detail: `Failed evaluating PATCH commands: ${error.message}`
    };
    return res.status(400).header("Content-Type", "application/scim+json").json(err);
  }
});

// USERS: Delete / Deactivate (DELETE)
scimRouter.delete("/Users/:id", (req: any, res) => {
  const start = Date.now();
  const conn = req.connection;
  const userIndex = users.findIndex(u => u.id === req.params.id);

  if (userIndex === -1) {
    const err = {
      schemas: ["urn:ietf:params:scim:api:messages:2.0:Error"],
      status: "404",
      detail: `User with identifier '${req.params.id}' not found for deletion.`
    };
    return res.status(404).header("Content-Type", "application/scim+json").json(err);
  }

  const user = users[userIndex];
  
  // "Default to governed deactivation/tombstone behavior, not silent hard deletion."
  user.active = false;
  user.sourceStatus = "inactive";
  user.updatedAt = new Date().toISOString();

  // Also remove from any groups
  groups.forEach(g => {
    g.members = g.members.filter(m => m.value !== user.id);
  });

  res.status(204).end(); // SCIM deletes typically yield 204 No Content

  events.unshift({
    id: generateId("evt"),
    timestamp: new Date().toISOString(),
    connectionId: conn.connectionId,
    connectionName: conn.name,
    clientIp: req.ip || "127.0.0.1",
    operation: "DELETE",
    resourceId: user.id,
    resourceType: "User",
    status: "success",
    responseCode: 204,
    rawRequest: `DELETE ${req.originalUrl}`,
    rawResponse: "204 No Content (Tombstone Applied)",
    latencyMs: Date.now() - start,
    correlationId: `corr_${crypto.randomBytes(5).toString("hex")}`,
    summary: `SCIM DELETE received for '${user.displayName}'. Governed tombstone applied, user deactivated, group memberships cleared.`
  });
});

// GROUPS: Read/List
scimRouter.get("/Groups", (req: any, res) => {
  const start = Date.now();
  const filter = req.query.filter as string;
  const startIndex = parseInt(req.query.startIndex as string) || 1;
  const count = parseInt(req.query.count as string) || 50;

  let filtered = [...groups];

  if (filter) {
    const displayNameMatch = filter.match(/displayName\s+eq\s+["'](.+?)["']/i);
    if (displayNameMatch) {
      const gName = displayNameMatch[1].toLowerCase();
      filtered = filtered.filter(g => g.displayName.toLowerCase() === gName);
    }
  }

  const totalResults = filtered.length;
  const paginated = filtered.slice(startIndex - 1, startIndex - 1 + count);

  const listResponse = {
    schemas: ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
    totalResults,
    itemsPerPage: paginated.length,
    startIndex,
    Resources: paginated.map(g => toScimGroup(g))
  };

  res.header("Content-Type", "application/scim+json");
  res.json(listResponse);

  const conn = req.connection;
  events.unshift({
    id: generateId("evt"),
    timestamp: new Date().toISOString(),
    connectionId: conn.connectionId,
    connectionName: conn.name,
    clientIp: req.ip || "127.0.0.1",
    operation: "GET",
    resourceType: "Group",
    status: "success",
    responseCode: 200,
    rawRequest: `GET ${req.originalUrl}`,
    rawResponse: JSON.stringify(listResponse, null, 2),
    latencyMs: Date.now() - start,
    correlationId: `corr_${crypto.randomBytes(5).toString("hex")}`,
    summary: `Queried SCIM Groups list. Filter: "${filter || 'None'}", Results: ${totalResults}.`
  });
});

// GROUPS: Create (POST)
scimRouter.post("/Groups", (req: any, res) => {
  const start = Date.now();
  const conn = req.connection;
  const payload = req.body;

  if (!payload.displayName) {
    const err = {
      schemas: ["urn:ietf:params:scim:api:messages:2.0:Error"],
      status: "400",
      detail: "Missing required Group attribute: displayName"
    };
    return res.status(400).header("Content-Type", "application/scim+json").json(err);
  }

  const gId = generateId("grp");
  const newGroup: GroupRecord = {
    id: gId,
    displayName: payload.displayName,
    externalId: payload.externalId,
    scimId: gId,
    sourceConnectionId: conn.connectionId,
    members: payload.members ? payload.members.map((m: any) => ({ value: m.value, display: m.display })) : [],
    mappedRoles: [],
    mappedEntitlements: [],
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  };

  groups.push(newGroup);
  conn.totalManagedGroups += 1;

  const response = toScimGroup(newGroup);
  res.status(201).header("Content-Type", "application/scim+json").json(response);

  events.unshift({
    id: generateId("evt"),
    timestamp: new Date().toISOString(),
    connectionId: conn.connectionId,
    connectionName: conn.name,
    clientIp: req.ip || "127.0.0.1",
    operation: "CREATE",
    resourceId: gId,
    resourceType: "Group",
    status: "success",
    responseCode: 201,
    rawRequest: `POST /Groups\n\n${JSON.stringify(payload, null, 2)}`,
    rawResponse: JSON.stringify(response, null, 2),
    latencyMs: Date.now() - start,
    correlationId: `corr_${crypto.randomBytes(5).toString("hex")}`,
    summary: `Created new SCIM-synced Group '${newGroup.displayName}' (${gId}).`
  });
});

// GROUPS: Read Individual (GET)
scimRouter.get("/Groups/:id", (req: any, res) => {
  const start = Date.now();
  const conn = req.connection;
  const group = groups.find(g => g.id === req.params.id);

  if (!group) {
    const err = {
      schemas: ["urn:ietf:params:scim:api:messages:2.0:Error"],
      status: "404",
      detail: `Group with identifier '${req.params.id}' not found.`
    };
    return res.status(404).header("Content-Type", "application/scim+json").json(err);
  }

  const response = toScimGroup(group);
  res.header("Content-Type", "application/scim+json");
  res.json(response);

  events.unshift({
    id: generateId("evt"),
    timestamp: new Date().toISOString(),
    connectionId: conn.connectionId,
    connectionName: conn.name,
    clientIp: req.ip || "127.0.0.1",
    operation: "GET",
    resourceId: group.id,
    resourceType: "Group",
    status: "success",
    responseCode: 200,
    rawRequest: `GET ${req.originalUrl}`,
    rawResponse: JSON.stringify(response, null, 2),
    latencyMs: Date.now() - start,
    correlationId: `corr_${crypto.randomBytes(5).toString("hex")}`,
    summary: `Fetched detailed representation of Group '${group.displayName}'.`
  });
});

// GROUPS: Patch (PATCH)
scimRouter.patch("/Groups/:id", (req: any, res) => {
  const start = Date.now();
  const conn = req.connection;
  const payload = req.body;
  const group = groups.find(g => g.id === req.params.id);

  if (!group) {
    const err = {
      schemas: ["urn:ietf:params:scim:api:messages:2.0:Error"],
      status: "404",
      detail: `Group with identifier '${req.params.id}' not found for patching.`
    };
    return res.status(404).header("Content-Type", "application/scim+json").json(err);
  }

  const ops = payload.Operations;
  if (!ops || !Array.isArray(ops)) {
    const err = {
      schemas: ["urn:ietf:params:scim:api:messages:2.0:Error"],
      status: "400",
      detail: "Missing Operations array in PATCH body"
    };
    return res.status(400).header("Content-Type", "application/scim+json").json(err);
  }

  try {
    for (const op of ops) {
      const type = op.op.toLowerCase();
      const pathVal = op.path;
      const val = op.value;

      if (type === "add") {
        const membersToAdd = Array.isArray(val) ? val : (pathVal === "members" ? val : []);
        for (const m of membersToAdd) {
          if (!group.members.some(gm => gm.value === m.value)) {
            group.members.push({ value: m.value, display: m.display });
          }
        }
      } else if (type === "remove") {
        if (pathVal && pathVal.startsWith("members")) {
          // Check for filtered value, e.g. members[value eq "usr_jane"]
          const filterMatch = pathVal.match(/value\s+eq\s+["'](.+?)["']/i);
          if (filterMatch) {
            const memberId = filterMatch[1];
            group.members = group.members.filter(gm => gm.value !== memberId);
          }
        } else if (Array.isArray(val)) {
          for (const m of val) {
            group.members = group.members.filter(gm => gm.value !== m.value);
          }
        }
      } else if (type === "replace") {
        if (pathVal === "displayName") {
          group.displayName = val;
        } else if (pathVal === "members" || !pathVal) {
          group.members = Array.isArray(val) ? val.map(m => ({ value: m.value, display: m.display })) : [];
        }
      }
    }

    group.updatedAt = new Date().toISOString();
    const response = toScimGroup(group);
    res.header("Content-Type", "application/scim+json");
    res.json(response);

    events.unshift({
      id: generateId("evt"),
      timestamp: new Date().toISOString(),
      connectionId: conn.connectionId,
      connectionName: conn.name,
      clientIp: req.ip || "127.0.0.1",
      operation: "PATCH",
      resourceId: group.id,
      resourceType: "Group",
      status: "success",
      responseCode: 200,
      rawRequest: `PATCH ${req.originalUrl}\n\n${JSON.stringify(payload, null, 2)}`,
      rawResponse: JSON.stringify(response, null, 2),
      latencyMs: Date.now() - start,
      correlationId: `corr_${crypto.randomBytes(5).toString("hex")}`,
      summary: `Evaluated group member modifications for Group '${group.displayName}'.`
    });
  } catch (err: any) {
    const errorBody = {
      schemas: ["urn:ietf:params:scim:api:messages:2.0:Error"],
      status: "400",
      detail: `Failed to patch group members: ${err.message}`
    };
    return res.status(400).header("Content-Type", "application/scim+json").json(errorBody);
  }
});

// GROUPS: Delete
scimRouter.delete("/Groups/:id", (req: any, res) => {
  const start = Date.now();
  const conn = req.connection;
  const groupIndex = groups.findIndex(g => g.id === req.params.id);

  if (groupIndex === -1) {
    const err = {
      schemas: ["urn:ietf:params:scim:api:messages:2.0:Error"],
      status: "404",
      detail: `Group with identifier '${req.params.id}' not found for deletion.`
    };
    return res.status(404).header("Content-Type", "application/scim+json").json(err);
  }

  const group = groups[groupIndex];
  groups.splice(groupIndex, 1);
  conn.totalManagedGroups = Math.max(0, conn.totalManagedGroups - 1);

  res.status(204).end();

  events.unshift({
    id: generateId("evt"),
    timestamp: new Date().toISOString(),
    connectionId: conn.connectionId,
    connectionName: conn.name,
    clientIp: req.ip || "127.0.0.1",
    operation: "DELETE",
    resourceId: group.id,
    resourceType: "Group",
    status: "success",
    responseCode: 204,
    rawRequest: `DELETE ${req.originalUrl}`,
    rawResponse: "204 No Content (Deleted Successfully)",
    latencyMs: Date.now() - start,
    correlationId: `corr_${crypto.randomBytes(5).toString("hex")}`,
    summary: `Hard deleted SCIM synced Group '${group.displayName}'.`
  });
});

// Bind routers
app.use("/tenants/:tenant_slug/scim/v2", authenticateScimClient, scimRouter);


// ==========================================
// ADMINISTRATIVE MANAGEMENT ENDPOINTS (UI BACKED)
// ==========================================

// Dashboard Metrics
app.get("/api/admin/overview", (req, res) => {
  const activeCount = connections.filter(c => c.lifecycleState === "active").length;
  
  const successEvents = events.filter(e => e.status === "success").length;
  const totalSyncEvents = events.filter(e => e.operation !== "DISCOVER").length;
  const successRate = totalSyncEvents > 0 ? parseFloat(((successEvents / totalSyncEvents) * 100).toFixed(1)) : 100.0;
  
  const avgLat = events.length > 0 ? Math.round(events.reduce((acc, curr) => acc + curr.latencyMs, 0) / events.length) : 15;
  const recentFailures = events.filter(e => e.status === "failure").length;

  const metrics: OverviewMetrics = {
    totalConnections: connections.length,
    totalUsers: users.length,
    totalGroups: groups.length,
    quarantinedCount: quarantines.length,
    avgLatencyMs: avgLat,
    syncSuccessRate: successRate,
    recentFailuresCount: recentFailures
  };

  res.json(metrics);
});

// Connections Management List
app.get("/api/admin/connections", (req, res) => {
  res.json(connections);
});

// Create Connection
app.post("/api/admin/connections", (req, res) => {
  const { name, sourceProfile, precedencePolicy, attributeMappings } = req.body;

  if (!name || !sourceProfile) {
    return res.status(400).json({ error: "Missing required fields: name and sourceProfile" });
  }

  const cId = generateId("conn");
  const rawToken = `tgb_scim_live_${sourceProfile}_${crypto.randomBytes(12).toString("hex")}`;
  const tokenHash = hashSecret(rawToken);

  const defaultMappings = attributeMappings || [
    { sourcePath: "userName", targetField: "userName", ownership: "source-owned" },
    { sourcePath: "displayName", targetField: "displayName", ownership: "source-owned" },
    { sourcePath: "emails[type eq 'work'].value", targetField: "emails", ownership: "source-owned" }
  ];

  const newConn: ScimConnection = {
    connectionId: cId,
    name,
    sourceProfile,
    lifecycleState: "draft",
    tokenSecret: rawToken, // Return raw token ONLY ONCE in create response
    tokenSecretHash: tokenHash,
    createdAt: new Date().toISOString(),
    lastUsed: "never",
    totalManagedUsers: 0,
    totalManagedGroups: 0,
    errorRate: 0.0,
    baseScimUrl: `https://ais-dev-hsrwvfs24dud5lx37fvtmo-3000.us-east1.run.app/tenants/acme-corp/scim/v2`,
    attributeMappings: defaultMappings,
    precedencePolicy: precedencePolicy || "quarantine-on-collision"
  };

  connections.push(newConn);

  // Audit event
  events.unshift({
    id: generateId("evt"),
    timestamp: new Date().toISOString(),
    connectionId: "admin",
    connectionName: "Tenant Admin Panel",
    clientIp: "127.0.0.1",
    operation: "CREATE",
    resourceType: "Config",
    resourceId: cId,
    status: "success",
    responseCode: 201,
    rawRequest: `POST /api/admin/connections\n\n${JSON.stringify({ name, sourceProfile }, null, 2)}`,
    rawResponse: JSON.stringify(newConn, null, 2),
    latencyMs: 5,
    correlationId: `corr_admin_${crypto.randomBytes(4).toString("hex")}`,
    summary: `Created new SCIM Connection '${name}' in Draft mode. Generated Bearer Credentials.`
  });

  res.status(201).json(newConn);
});

// Edit Connection Mappings, Precedence, Status
app.patch("/api/admin/connections/:id", (req, res) => {
  const conn = connections.find(c => c.connectionId === req.params.id);
  if (!conn) {
    return res.status(404).json({ error: "Connection not found" });
  }

  const { name, lifecycleState, precedencePolicy, attributeMappings } = req.body;

  if (name !== undefined) conn.name = name;
  if (lifecycleState !== undefined) conn.lifecycleState = lifecycleState;
  if (precedencePolicy !== undefined) conn.precedencePolicy = precedencePolicy;
  if (attributeMappings !== undefined) conn.attributeMappings = attributeMappings;

  // Audit event
  events.unshift({
    id: generateId("evt"),
    timestamp: new Date().toISOString(),
    connectionId: "admin",
    connectionName: "Tenant Admin Panel",
    clientIp: "127.0.0.1",
    operation: "UPDATE",
    resourceType: "Config",
    resourceId: conn.connectionId,
    status: "success",
    responseCode: 200,
    rawRequest: `PATCH /api/admin/connections/${conn.connectionId}`,
    rawResponse: JSON.stringify(conn, null, 2),
    latencyMs: 3,
    correlationId: `corr_admin_${crypto.randomBytes(4).toString("hex")}`,
    summary: `Updated settings for Connection '${conn.name}'. Lifecycle: ${conn.lifecycleState}.`
  });

  res.json(conn);
});

// Rotate Token Secret
app.post("/api/admin/connections/:id/rotate", (req, res) => {
  const conn = connections.find(c => c.connectionId === req.params.id);
  if (!conn) {
    return res.status(404).json({ error: "Connection not found" });
  }

  const newRawToken = `tgb_scim_live_${conn.sourceProfile}_rotated_${crypto.randomBytes(12).toString("hex")}`;
  conn.tokenSecretHash = hashSecret(newRawToken);
  conn.tokenSecret = newRawToken; // Shown once visually

  // Audit event
  events.unshift({
    id: generateId("evt"),
    timestamp: new Date().toISOString(),
    connectionId: "admin",
    connectionName: "Tenant Admin Panel",
    clientIp: "127.0.0.1",
    operation: "UPDATE",
    resourceType: "Config",
    resourceId: conn.connectionId,
    status: "success",
    responseCode: 200,
    rawRequest: `POST /api/admin/connections/${conn.connectionId}/rotate`,
    rawResponse: `Hashed and rotated secrets successfully.`,
    latencyMs: 12,
    correlationId: `corr_admin_${crypto.randomBytes(4).toString("hex")}`,
    summary: `Rotated access bearer credentials for Connection '${conn.name}'. Prior secrets invalidated.`
  });

  res.json({ status: "success", tokenSecret: newRawToken });
});

// Delete Connection
app.delete("/api/admin/connections/:id", (req, res) => {
  const idx = connections.findIndex(c => c.connectionId === req.params.id);
  if (idx === -1) {
    return res.status(404).json({ error: "Connection not found" });
  }

  const conn = connections[idx];
  connections.splice(idx, 1);

  // Sever links of existing users/groups or tombstone them
  users.forEach(u => {
    if (u.sourceConnectionId === conn.connectionId) {
      u.sourceStatus = "pending"; // Detached!
    }
  });

  // Audit event
  events.unshift({
    id: generateId("evt"),
    timestamp: new Date().toISOString(),
    connectionId: "admin",
    connectionName: "Tenant Admin Panel",
    clientIp: "127.0.0.1",
    operation: "DELETE",
    resourceType: "Config",
    resourceId: conn.connectionId,
    status: "success",
    responseCode: 200,
    rawRequest: `DELETE /api/admin/connections/${conn.connectionId}`,
    rawResponse: `Connection removed.`,
    latencyMs: 4,
    correlationId: `corr_admin_${crypto.randomBytes(4).toString("hex")}`,
    summary: `Removed Connection '${conn.name}'. Synchronized accounts have been detached/marked pending local admin review.`
  });

  res.json({ status: "success" });
});

// Directory list with details
app.get("/api/admin/directory", (req, res) => {
  // Combine users, groups, memberships
  res.json({
    users,
    groups
  });
});

// Quarantine Queue
app.get("/api/admin/quarantine", (req, res) => {
  res.json(quarantines);
});

// Resolve Quarantine
app.post("/api/admin/quarantine/:id/resolve", (req, res) => {
  const qId = req.params.id;
  const { action } = req.body; // 'link', 'force-separate', 'reject'
  
  const qRecord = quarantines.find(q => q.id === qId);
  if (!qRecord) {
    return res.status(404).json({ error: "Quarantine record not found" });
  }

  const conn = connections.find(c => c.connectionId === qRecord.connectionId);

  if (action === "link") {
    // Merge colliding payload with the canonical record
    const targetUserId = qRecord.conflictWithId;
    const existingUser = users.find(u => u.id === targetUserId);
    if (!existingUser) {
      return res.status(400).json({ error: "Collision user target not found in Directory" });
    }

    // Adopt connection attributes and map
    existingUser.sourceConnectionId = qRecord.connectionId;
    existingUser.externalId = qRecord.externalId;
    existingUser.sourceStatus = "linked";
    existingUser.updatedAt = new Date().toISOString();
    
    // Clear quarantine
    quarantines = quarantines.filter(q => q.id !== qId);

    // Increment counter
    if (conn) conn.totalManagedUsers += 1;

    // Audit event
    events.unshift({
      id: generateId("evt"),
      timestamp: new Date().toISOString(),
      connectionId: "admin",
      connectionName: "Tenant Admin Panel",
      clientIp: "127.0.0.1",
      operation: "UPDATE",
      resourceType: "User",
      resourceId: existingUser.id,
      status: "success",
      responseCode: 200,
      rawRequest: `Quarantine Resolve Link: ${qId}`,
      rawResponse: `Linked external user to canonical profile ${existingUser.id}`,
      latencyMs: 10,
      correlationId: `corr_admin_${crypto.randomBytes(4).toString("hex")}`,
      summary: `Manually resolved username collision. External identity from '${qRecord.connectionName}' linked to existing canonical profile of '${existingUser.displayName}'.`
    });

    return res.json({ status: "resolved", action: "link", user: existingUser });

  } else if (action === "force-separate") {
    // Generate a unique userName to separate them, e.g. suffixing with connection name or string
    const newUserName = `${qRecord.payload.userName.split("@")[0]}_${qRecord.connectionName.toLowerCase().replace(/\s+/g, "_")}@acme.com`;
    
    const newUserId = generateId("usr");
    const newRecord: UserRecord = {
      id: newUserId,
      userName: newUserName,
      displayName: qRecord.payload.name?.formatted || qRecord.payload.displayName || newUserName.split("@")[0],
      emails: [{ value: newUserName, type: "work", primary: true }],
      active: true,
      title: qRecord.payload.title,
      department: qRecord.payload.department,
      organization: "Acme Corp",
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      sourceConnectionId: qRecord.connectionId,
      externalId: qRecord.externalId,
      scimId: newUserId,
      sourceStatus: "linked",
      originalPayloadDigest: `resolved-separate:${qRecord.id}`
    };

    users.push(newRecord);
    quarantines = quarantines.filter(q => q.id !== qId);
    if (conn) conn.totalManagedUsers += 1;

    // Audit event
    events.unshift({
      id: generateId("evt"),
      timestamp: new Date().toISOString(),
      connectionId: "admin",
      connectionName: "Tenant Admin Panel",
      clientIp: "127.0.0.1",
      operation: "CREATE",
      resourceType: "User",
      resourceId: newUserId,
      status: "success",
      responseCode: 201,
      rawRequest: `Quarantine Resolve Force-Separate: ${qId}`,
      rawResponse: JSON.stringify(newRecord, null, 2),
      latencyMs: 15,
      correlationId: `corr_admin_${crypto.randomBytes(4).toString("hex")}`,
      summary: `Manually resolved collision via Separation. Provisioned separate user '${newRecord.displayName}' with unique userName suffix '${newUserName}'.`
    });

    return res.json({ status: "resolved", action: "force-separate", user: newRecord });

  } else if (action === "reject") {
    // Discard the quarantined entry entirely
    quarantines = quarantines.filter(q => q.id !== qId);

    // Audit event
    events.unshift({
      id: generateId("evt"),
      timestamp: new Date().toISOString(),
      connectionId: "admin",
      connectionName: "Tenant Admin Panel",
      clientIp: "127.0.0.1",
      operation: "DELETE",
      resourceType: "User",
      status: "success",
      responseCode: 200,
      rawRequest: `Quarantine Resolve Reject: ${qId}`,
      rawResponse: `Discarded quarantined payload`,
      latencyMs: 5,
      correlationId: `corr_admin_${crypto.randomBytes(4).toString("hex")}`,
      summary: `Administrator manually rejected and discarded quarantined payload of Charles Doe.`
    });

    return res.json({ status: "resolved", action: "reject" });
  }

  res.status(400).json({ error: "Invalid resolution action: " + action });
});

// Logs/Events Timeline
app.get("/api/admin/events", (req, res) => {
  res.json(events);
});

// Reset Database Trigger
app.post("/api/admin/reset", (req, res) => {
  resetDatabase();
  res.json({ status: "success", message: "Database reset to rich initial mock dataset" });
});


// ==========================================
// CLIENT-SIDE SPA DEV/PROD VITE ROUTING
// ==========================================
async function startServer() {
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa"
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), "dist");
    app.use(express.static(distPath));
    app.get("*", (req, res) => {
      res.sendFile(path.join(distPath, "index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server successfully booted on port ${PORT}`);
  });
}

startServer();
