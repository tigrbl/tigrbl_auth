import { DetailPanel, PageHeader, ResourceTable, StatusBadge } from "@tigrbl-auth/uix-core";
import { ShortId } from "../components/ShortId";
import type { Identity, Realm, Tenant } from "../types";

function tenantStatus(tenant: Tenant) {
  return tenant.is_active === false ? "Suspended" : "Active";
}

function identityRole(identity: Pick<Identity, "is_admin" | "is_superuser">) {
  if (identity.is_superuser) return "Superuser";
  if (identity.is_admin) return "Admin";
  return "User";
}

function identityRoles(identity: Identity) {
  const assigned = new Set(identity.roles);
  if (identity.is_superuser) assigned.add("superuser");
  if (identity.is_admin) assigned.add("admin");
  return Array.from(assigned);
}

function isTenantAdministrator(identity: Identity) {
  return identity.is_admin || identity.is_superuser || identity.roles.some((role) => role.includes("admin"));
}

function NotFoundDetail({ collectionHref, id, title }: { collectionHref: string; id: string; title: string }) {
  return (
    <div className="tigrbl-page-stack">
      <PageHeader title={title} description="This member route renders one collection row." />
      <DetailPanel title="Not found">
        <p>The requested row is not visible to this platform session.</p>
        <p>
          <span className="tigrbl-label">Requested ID</span>
          <ShortId id={id} />
        </p>
        <p><a href={collectionHref}>Back to collection</a></p>
      </DetailPanel>
    </div>
  );
}

export function RealmMemberPage({
  identities,
  realmId,
  realms,
  tenants
}: {
  identities: Identity[];
  realmId: string;
  realms: Realm[];
  tenants: Tenant[];
}) {
  const realm = realms.find((item) => item.id === realmId) ?? null;
  if (!realm) return <NotFoundDetail collectionHref="#/realms" id={realmId} title="Realm detail" />;
  const realmTenants = tenants.filter((tenant) => tenant.realm_id === realm.id);
  const activeTenantCount = realmTenants.filter((tenant) => tenant.is_active !== false).length;
  const suspendedTenantCount = realmTenants.length - activeTenantCount;
  const realmTenantIds = new Set(realmTenants.map((tenant) => tenant.id));
  const realmAdministrators = identities.filter((identity) => realmTenantIds.has(identity.tenant_id) && isTenantAdministrator(identity));

  return (
    <div className="tigrbl-page-stack">
      <PageHeader title={realm.name} description="Realm collection member detail." />
      <DetailPanel title="Realm details">
        <div className="tigrbl-summary-grid">
          <div>
            <span className="tigrbl-label">Realm</span>
            <strong>{realm.name}</strong>
            <p>{realm.slug}</p>
          </div>
          <div>
            <span className="tigrbl-label">Issuer path</span>
            <strong>{realm.issuer_path || "default issuer"}</strong>
          </div>
          <div>
            <span className="tigrbl-label">Status</span>
            <StatusBadge tone="success">Active</StatusBadge>
          </div>
          <div>
            <span className="tigrbl-label">Tenants</span>
            <strong>{realmTenants.length}</strong>
            <p>{activeTenantCount} active / {suspendedTenantCount} suspended</p>
          </div>
          <div>
            <span className="tigrbl-label">Administrators</span>
            <strong>{realmAdministrators.length}</strong>
            <p>Visible tenant and realm operators</p>
          </div>
          <div>
            <span className="tigrbl-label">ID</span>
            <ShortId id={realm.id} />
          </div>
        </div>
      </DetailPanel>
      {realm.description && <DetailPanel title="Description"><p>{realm.description}</p></DetailPanel>}
      <DetailPanel title="Tenants in realm">
        <ResourceTable
          items={realmTenants}
          getRowKey={(tenant) => tenant.id}
          emptyTitle="No tenants"
          emptyBody="No tenants are currently assigned to this realm."
          columns={[
            {
              key: "name",
              header: "Tenant",
              render: (tenant) => (
                <a className="tigrbl-link-button" href={`#/tenants/${encodeURIComponent(tenant.id)}`}>
                  <strong>{tenant.name}</strong>
                  <span>{tenant.slug} / {tenant.email}</span>
                </a>
              )
            },
            {
              key: "status",
              header: "Status",
              render: (tenant) => (
                <StatusBadge tone={tenant.is_active === false ? "warning" : "success"}>{tenantStatus(tenant)}</StatusBadge>
              )
            },
            { key: "id", header: "ID", render: (tenant) => <ShortId id={tenant.id} /> }
          ]}
        />
      </DetailPanel>
      <DetailPanel title="Realm administrators">
        <ResourceTable
          items={realmAdministrators}
          getRowKey={(identity) => identity.id}
          emptyTitle="No administrators"
          emptyBody="No administrators are visible for tenants in this realm."
          columns={[
            {
              key: "identity",
              header: "Identity",
              render: (identity) => (
                <a className="tigrbl-link-button" href={`#/identities/${encodeURIComponent(identity.id)}`}>
                  <strong>{identity.username}</strong>
                  <span>{identity.email}</span>
                </a>
              )
            },
            { key: "role", header: "Role", render: (identity) => identityRole(identity) },
            {
              key: "status",
              header: "Status",
              render: (identity) => (
                <StatusBadge tone={identity.is_active ? "success" : "warning"}>{identity.is_active ? "Active" : "Suspended"}</StatusBadge>
              )
            }
          ]}
        />
      </DetailPanel>
      <p><a href="#/realms">Back to realms</a></p>
    </div>
  );
}

export function TenantMemberPage({
  identities,
  realms,
  tenantId,
  tenants
}: {
  identities: Identity[];
  realms: Realm[];
  tenantId: string;
  tenants: Tenant[];
}) {
  const tenant = tenants.find((item) => item.id === tenantId) ?? null;
  if (!tenant) return <NotFoundDetail collectionHref="#/tenants" id={tenantId} title="Tenant detail" />;
  const realm = realms.find((item) => item.id === tenant.realm_id) ?? null;
  const tenantIdentities = identities.filter((identity) => identity.tenant_id === tenant.id);
  const tenantAdministrators = tenantIdentities.filter(isTenantAdministrator);

  return (
    <div className="tigrbl-page-stack">
      <PageHeader title={tenant.name} description="Tenant collection member detail." />
      <DetailPanel title="Tenant details">
        <div className="tigrbl-summary-grid">
          <div>
            <span className="tigrbl-label">Tenant</span>
            <strong>{tenant.name}</strong>
            <p>{tenant.slug} / {tenant.email}</p>
          </div>
          <div>
            <span className="tigrbl-label">Realm</span>
            <strong>{realm?.name ?? "Default realm"}</strong>
            <p>
              {realm ? <a href={`#/realms/${encodeURIComponent(realm.id)}`}>{realm.slug}</a> : tenant.realm_id ?? "default"}
            </p>
          </div>
          <div>
            <span className="tigrbl-label">Status</span>
            <StatusBadge tone={tenant.is_active === false ? "warning" : "success"}>{tenantStatus(tenant)}</StatusBadge>
          </div>
          <div>
            <span className="tigrbl-label">Identities</span>
            <strong>{tenantIdentities.length}</strong>
            <p>{tenantAdministrators.length} administrators</p>
          </div>
          <div>
            <span className="tigrbl-label">ID</span>
            <ShortId id={tenant.id} />
          </div>
        </div>
      </DetailPanel>
      <DetailPanel title="Tenant administrators">
        <ResourceTable
          items={tenantAdministrators}
          getRowKey={(identity) => identity.id}
          emptyTitle="No administrators"
          emptyBody="No tenant administrators are visible for this tenant."
          columns={[
            {
              key: "identity",
              header: "Identity",
              render: (identity) => (
                <a className="tigrbl-link-button" href={`#/identities/${encodeURIComponent(identity.id)}`}>
                  <strong>{identity.username}</strong>
                  <span>{identity.email}</span>
                </a>
              )
            },
            { key: "role", header: "Role", render: (identity) => identityRole(identity) },
            { key: "id", header: "ID", render: (identity) => <ShortId id={identity.id} /> }
          ]}
        />
      </DetailPanel>
      <DetailPanel title="Identities in tenant">
        <ResourceTable
          items={tenantIdentities}
          getRowKey={(identity) => identity.id}
          emptyTitle="No identities"
          emptyBody="No identities are visible for this tenant."
          columns={[
            {
              key: "identity",
              header: "Identity",
              render: (identity) => (
                <a className="tigrbl-link-button" href={`#/identities/${encodeURIComponent(identity.id)}`}>
                  <strong>{identity.username}</strong>
                  <span>{identity.email}</span>
                </a>
              )
            },
            { key: "role", header: "Role", render: (identity) => identityRole(identity) },
            {
              key: "status",
              header: "Status",
              render: (identity) => (
                <StatusBadge tone={identity.is_active ? "success" : "warning"}>{identity.is_active ? "Active" : "Suspended"}</StatusBadge>
              )
            }
          ]}
        />
      </DetailPanel>
      <p><a href="#/tenants">Back to tenants</a></p>
    </div>
  );
}

export function IdentityMemberPage({
  identities,
  identityId,
  realms,
  tenants
}: {
  identities: Identity[];
  identityId: string;
  realms: Realm[];
  tenants: Tenant[];
}) {
  const identity = identities.find((item) => item.id === identityId) ?? null;
  if (!identity) return <NotFoundDetail collectionHref="#/identities" id={identityId} title="Identity detail" />;
  const tenant = tenants.find((item) => item.id === identity.tenant_id) ?? null;
  const realm = tenant ? realms.find((item) => item.id === tenant.realm_id) ?? null : null;
  const roles = identityRoles(identity);

  return (
    <div className="tigrbl-page-stack">
      <PageHeader title={identity.username} description="Identity collection member detail." />
      <DetailPanel title="Identity details">
        <div className="tigrbl-summary-grid">
          <div>
            <span className="tigrbl-label">Identity</span>
            <strong>{identity.username}</strong>
            <p>{identity.email}</p>
          </div>
          <div>
            <span className="tigrbl-label">Tenant</span>
            <strong>{tenant?.name ?? identity.tenant_id}</strong>
            <p>{tenant ? <a href={`#/tenants/${encodeURIComponent(tenant.id)}`}>{tenant.slug}</a> : "tenant context"}</p>
          </div>
          <div>
            <span className="tigrbl-label">Realm</span>
            <strong>{realm?.name ?? tenant?.realm_id ?? "Default realm"}</strong>
            <p>{realm ? <a href={`#/realms/${encodeURIComponent(realm.id)}`}>{realm.slug}</a> : "realm context"}</p>
          </div>
          <div>
            <span className="tigrbl-label">Role</span>
            <StatusBadge tone={identity.is_superuser || identity.is_admin ? "success" : "info"}>{identityRole(identity)}</StatusBadge>
          </div>
          <div>
            <span className="tigrbl-label">Status</span>
            <StatusBadge tone={identity.is_active ? "success" : "warning"}>{identity.is_active ? "Active" : "Suspended"}</StatusBadge>
          </div>
          <div>
            <span className="tigrbl-label">Password</span>
            <StatusBadge tone={identity.must_change_password ? "warning" : "success"}>{identity.must_change_password ? "Must change" : "Current"}</StatusBadge>
          </div>
          <div>
            <span className="tigrbl-label">ID</span>
            <ShortId id={identity.id} />
          </div>
        </div>
      </DetailPanel>
      <DetailPanel title="Assigned roles">
        {roles.length ? (
          <div className="tigrbl-summary-grid">
            {roles.map((role) => (
              <div key={role}>
                <span className="tigrbl-label">Role</span>
                <StatusBadge tone={role.includes("admin") || role === "superuser" ? "success" : "info"}>{role}</StatusBadge>
              </div>
            ))}
          </div>
        ) : (
          <p>No explicit roles are visible for this identity.</p>
        )}
      </DetailPanel>
      <p><a href="#/identities">Back to identities</a></p>
    </div>
  );
}
