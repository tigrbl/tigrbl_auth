import { DetailPanel, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
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

export function RealmMemberPage({ realmId, realms }: { realmId: string; realms: Realm[] }) {
  const realm = realms.find((item) => item.id === realmId) ?? null;
  if (!realm) return <NotFoundDetail collectionHref="#/realms" id={realmId} title="Realm detail" />;

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
            <span className="tigrbl-label">ID</span>
            <ShortId id={realm.id} />
          </div>
        </div>
      </DetailPanel>
      {realm.description && <DetailPanel title="Description"><p>{realm.description}</p></DetailPanel>}
      <p><a href="#/realms">Back to realms</a></p>
    </div>
  );
}

export function TenantMemberPage({
  realms,
  tenantId,
  tenants
}: {
  realms: Realm[];
  tenantId: string;
  tenants: Tenant[];
}) {
  const tenant = tenants.find((item) => item.id === tenantId) ?? null;
  if (!tenant) return <NotFoundDetail collectionHref="#/tenants" id={tenantId} title="Tenant detail" />;
  const realm = realms.find((item) => item.id === tenant.realm_id) ?? null;

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
            <p>{realm?.slug ?? tenant.realm_id ?? "default"}</p>
          </div>
          <div>
            <span className="tigrbl-label">Status</span>
            <StatusBadge tone={tenant.is_active === false ? "warning" : "success"}>{tenantStatus(tenant)}</StatusBadge>
          </div>
          <div>
            <span className="tigrbl-label">ID</span>
            <ShortId id={tenant.id} />
          </div>
        </div>
      </DetailPanel>
      <p><a href="#/tenants">Back to tenants</a></p>
    </div>
  );
}

export function IdentityMemberPage({
  identities,
  identityId,
  tenants
}: {
  identities: Identity[];
  identityId: string;
  tenants: Tenant[];
}) {
  const identity = identities.find((item) => item.id === identityId) ?? null;
  if (!identity) return <NotFoundDetail collectionHref="#/identities" id={identityId} title="Identity detail" />;
  const tenant = tenants.find((item) => item.id === identity.tenant_id) ?? null;

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
            <p>{tenant?.slug ?? "tenant context"}</p>
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
      <p><a href="#/identities">Back to identities</a></p>
    </div>
  );
}
