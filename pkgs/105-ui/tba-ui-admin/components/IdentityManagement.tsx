import React, { useEffect, useMemo, useState } from 'react';
import { backendService } from '../services/backendService';
import { Icons } from '../constants';
import { Tenant, User, UserStatus } from '../types';
import type { AdminSessionState } from '../services/adminAuthService';
import styles from './IdentityManagement.module.css';
import { humanizeError } from '../services/errorMessages';

interface IdentityManagementProps {
  tenant: Tenant;
  session: AdminSessionState;
}

type ProvisionFormState = {
  username: string;
  email: string;
  password: string;
  is_admin: boolean;
  is_superuser: boolean;
  must_change_password: boolean;
};

const emptyForm = (): ProvisionFormState => ({
  username: '',
  email: '',
  password: '',
  is_admin: false,
  is_superuser: false,
  must_change_password: true,
});

const IdentityManagement: React.FC<IdentityManagementProps> = ({ tenant, session }) => {
  const [identities, set_identities] = useState<User[]>([]);
  const [selected_id, set_selected_id] = useState<User | null>(null);
  const [show_add, set_show_add] = useState(false);
  const [form_data, set_form_data] = useState<ProvisionFormState>(emptyForm);
  const [loading, set_loading] = useState(true);
  const [error, set_error] = useState<string | null>(null);
  const [saving, set_saving] = useState(false);

  const canManageAdmins = Boolean(session.is_superuser);

  const refresh = async () => {
    set_loading(true);
    set_error(null);
    try {
      const users = await backendService.getUsers(tenant.id);
      set_identities(users);
      set_selected_id((current) => users.find((item) => item.id === current?.id) ?? users[0] ?? null);
    } catch (nextError) {
      set_error(humanizeError(nextError, 'Failed to load users.'));
    } finally {
      set_loading(false);
    }
  };

  useEffect(() => {
    void refresh();
  }, [tenant.id]);

  const selectedSummary = useMemo(() => {
    if (!selected_id) {
      return null;
    }
    return {
      roleLabel: selected_id.is_superuser ? 'SUPERUSER' : selected_id.is_admin ? 'ADMIN' : 'USER',
      lastPulse: selected_id.updated_at ?? selected_id.created_at ?? 'not yet recorded',
    };
  }, [selected_id]);

  const handle_add = async () => {
    if (!form_data.username || !form_data.email || !form_data.password) {
      set_error('Username, email, and temporary password are required.');
      return;
    }
    set_saving(true);
    set_error(null);
    try {
      await backendService.createUser({
        tenant_id: tenant.id,
        username: form_data.username,
        email: form_data.email,
        password: form_data.password,
        is_admin: canManageAdmins ? form_data.is_admin : false,
        is_superuser: canManageAdmins ? form_data.is_superuser : false,
        must_change_password: form_data.must_change_password,
      });
      set_show_add(false);
      set_form_data(emptyForm());
      await refresh();
    } catch (nextError) {
      set_error(humanizeError(nextError, 'Failed to create user.'));
    } finally {
      set_saving(false);
    }
  };

  const handle_delete = async (id: string) => {
    if (!confirm('Delete this identity from the tenant directory?')) {
      return;
    }
    set_saving(true);
    set_error(null);
    try {
      await backendService.deleteUser(id);
      await refresh();
      if (selected_id?.id === id) {
        set_selected_id(null);
      }
    } catch (nextError) {
      set_error(humanizeError(nextError, 'Failed to delete user.'));
    } finally {
      set_saving(false);
    }
  };

  const handle_status_change = async (identity: User, nextStatus: UserStatus) => {
    set_saving(true);
    set_error(null);
    try {
      await backendService.updateUser(identity.id, {
        is_active: nextStatus === UserStatus.ACTIVE,
      });
      await refresh();
    } catch (nextError) {
      set_error(humanizeError(nextError, 'Failed to update user status.'));
    } finally {
      set_saving(false);
    }
  };

  const handleRoleToggle = async (identity: User, field: 'is_admin' | 'is_superuser') => {
    if (!canManageAdmins) {
      set_error('Only the bootstrap superuser can promote or demote administrators.');
      return;
    }
    set_saving(true);
    set_error(null);
    try {
      const nextValue = !Boolean(identity[field]);
      await backendService.updateUser(identity.id, {
        is_admin: field === 'is_admin' ? nextValue : Boolean(identity.is_admin),
        is_superuser: field === 'is_superuser' ? nextValue : Boolean(identity.is_superuser),
      });
      await refresh();
    } catch (nextError) {
      set_error(humanizeError(nextError, 'Failed to update administrative role.'));
    } finally {
      set_saving(false);
    }
  };

  const handlePasswordResetRequirement = async (identity: User) => {
    set_saving(true);
    set_error(null);
    try {
      await backendService.updateUser(identity.id, {
        must_change_password: !Boolean(identity.must_change_password),
      });
      await refresh();
    } catch (nextError) {
      set_error(humanizeError(nextError, 'Failed to update password policy.'));
    } finally {
      set_saving(false);
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div>
          <h1 className={styles.title}>Users</h1>
          <p className={styles.subtitle}>Create and manage user accounts for {tenant.name}.</p>
        </div>
        <div className={styles.headerActions}>
          <button onClick={() => void refresh()} className={styles.buttonBase}>Refresh Users</button>
          <button onClick={() => set_show_add(true)} className={`${styles.buttonBase} ${styles.buttonPrimary}`}>Create User</button>
        </div>
      </div>

      {error ? <div className={styles.emptyState}><p className={styles.emptyText}>{error}</p></div> : null}

      <div className={styles.layoutGrid}>
        <div className={styles.tableColumn}>
          <div className={styles.tableCard}>
            {loading ? (
              <div className={styles.emptyState}>
                <div className={styles.emptyIcon}><Icons.Users /></div>
                <p className={styles.emptyText}>Loading tenant identities...</p>
              </div>
            ) : (
              <table className={styles.table}>
                <thead>
                  <tr className={styles.tableHeaderRow}>
                    <th className={styles.tableHeaderCell}>User</th>
                    <th className={styles.tableHeaderCell}>Role</th>
                    <th className={styles.tableHeaderCell}>Status</th>
                    <th className={`${styles.tableHeaderCell} ${styles.tableHeaderCellRight}`}>Actions</th>
                  </tr>
                </thead>
                <tbody className={styles.tableBody}>
                  {identities.map((identity) => (
                    <tr key={identity.id} className={`${styles.tableRow} ${selected_id?.id === identity.id ? styles.tableRowSelected : ''}`} onClick={() => set_selected_id(identity)}>
                      <td className={styles.tableCell}>
                        <div className={styles.subjectInfo}>
                          <div className={`${styles.subjectAvatar} ${selected_id?.id === identity.id ? styles.subjectAvatarActive : ''}`}>
                            {identity.username.slice(0, 1).toUpperCase()}
                          </div>
                          <div>
                            <p className={styles.subjectName}>{identity.username}</p>
                            <p className={styles.subjectEmail}>{identity.email}</p>
                          </div>
                        </div>
                      </td>
                      <td className={styles.tableCell}>
                        <span className={styles.providerBadge}>
                          {identity.is_superuser ? 'superuser' : identity.is_admin ? 'admin' : 'user'}
                        </span>
                      </td>
                      <td className={styles.tableCell}>
                        <span className={`${styles.statusBadge} ${
                          identity.status === UserStatus.ACTIVE ? styles.statusActive :
                          identity.status === UserStatus.SUSPENDED ? styles.statusSuspended : styles.statusPending
                        }`}>
                          {identity.status}
                        </span>
                      </td>
                      <td className={`${styles.tableCell} ${styles.tableCellRight}`}>
                        <button onClick={(event) => { event.stopPropagation(); void handle_delete(identity.id); }} className={styles.deleteButton} disabled={saving}>
                          <Icons.Activity />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>

        <div className={styles.detailColumn}>
          {selected_id && selectedSummary ? (
            <div className={styles.detailCard}>
              <div className={styles.detailHeader}>
                <div className={styles.detailAvatar}>
                  {selected_id.username.slice(0, 1).toUpperCase()}
                </div>
                <div className={styles.detailMeta}>
                  <p className={styles.detailMetaLabel}>Directory State</p>
                  <span className={styles.detailMetaBadge}>{selectedSummary.roleLabel}</span>
                </div>
              </div>
              <h3 className={styles.detailName}>{selected_id.username}</h3>
              <p className={styles.detailId}>{selected_id.email}</p>

              <div className={styles.detailSections}>
                <div>
                  <p className={styles.detailLabel}>Administrative Roles</p>
                  <div className={styles.statusButtons}>
                    <button
                      onClick={() => void handleRoleToggle(selected_id, 'is_admin')}
                      className={`${styles.statusButton} ${selected_id.is_admin ? styles.statusButtonActive : styles.statusButtonInactive}`}
                      disabled={saving || !canManageAdmins}
                    >
                      Admin
                    </button>
                    <button
                      onClick={() => void handleRoleToggle(selected_id, 'is_superuser')}
                      className={`${styles.statusButton} ${selected_id.is_superuser ? styles.statusButtonSuspendedActive : styles.statusButtonInactive}`}
                      disabled={saving || !canManageAdmins}
                    >
                      Superuser
                    </button>
                  </div>
                </div>
                <div>
                  <p className={styles.detailLabel}>Lifecycle Status</p>
                  <div className={styles.statusButtons}>
                    <button
                      onClick={() => void handle_status_change(selected_id, UserStatus.ACTIVE)}
                      className={`${styles.statusButton} ${selected_id.status === UserStatus.ACTIVE ? styles.statusButtonActive : styles.statusButtonInactive}`}
                      disabled={saving}
                    >
                      Active
                    </button>
                    <button
                      onClick={() => void handle_status_change(selected_id, UserStatus.SUSPENDED)}
                      className={`${styles.statusButton} ${selected_id.status === UserStatus.SUSPENDED ? styles.statusButtonSuspendedActive : styles.statusButtonInactive}`}
                      disabled={saving}
                    >
                      Suspend
                    </button>
                  </div>
                </div>
                <div>
                  <p className={styles.detailLabel}>Credential Policy</p>
                  <div className={styles.detailRow}>
                    <span className={styles.detailValue}>
                      {selected_id.must_change_password ? 'Password rotation required on next login' : 'Password change requirement cleared'}
                    </span>
                    <button onClick={() => void handlePasswordResetRequirement(selected_id)} className={styles.detailToggle} disabled={saving}>
                      Toggle
                    </button>
                  </div>
                </div>
                <div>
                  <p className={styles.detailLabel}>Last Updated</p>
                  <span className={styles.detailValue}>{selectedSummary.lastPulse}</span>
                </div>
              </div>

              {!canManageAdmins ? (
                <div className={styles.detailActions}>
                  <button className={styles.detailActionButton} disabled>Admin promotion requires bootstrap superuser</button>
                </div>
              ) : null}
            </div>
          ) : (
            <div className={styles.emptyState}>
              <div className={styles.emptyIcon}><Icons.Users /></div>
              <p className={styles.emptyText}>Select a user to view administrative controls</p>
            </div>
          )}
        </div>
      </div>

      {show_add && (
        <div className={styles.modalOverlay}>
          <div className={styles.modal}>
            <h3 className={styles.modalTitle}>Create User</h3>
            <div className={styles.modalBody}>
              <div>
                <label className={styles.formLabel}>Username</label>
                <input
                  type="text"
                  value={form_data.username}
                  onChange={(event) => set_form_data({ ...form_data, username: event.target.value })}
                  className={styles.formInput}
                />
              </div>
              <div>
                <label className={styles.formLabel}>E-Mail Address</label>
                <input
                  type="email"
                  value={form_data.email}
                  onChange={(event) => set_form_data({ ...form_data, email: event.target.value })}
                  className={styles.formInput}
                />
              </div>
              <div>
                <label className={styles.formLabel}>Temporary Password</label>
                <input
                  type="password"
                  value={form_data.password}
                  onChange={(event) => set_form_data({ ...form_data, password: event.target.value })}
                  className={styles.formInput}
                />
              </div>
              <div className={styles.detailSections}>
                <label className={styles.detailRow}>
                  <span className={styles.detailValue}>Force password change on first login</span>
                  <input
                    type="checkbox"
                    checked={form_data.must_change_password}
                    onChange={(event) => set_form_data({ ...form_data, must_change_password: event.target.checked })}
                  />
                </label>
                <label className={styles.detailRow}>
                  <span className={styles.detailValue}>Grant administrator role</span>
                  <input
                    type="checkbox"
                    checked={form_data.is_admin}
                    disabled={!canManageAdmins}
                    onChange={(event) => set_form_data({ ...form_data, is_admin: event.target.checked })}
                  />
                </label>
                <label className={styles.detailRow}>
                  <span className={styles.detailValue}>Grant superuser role</span>
                  <input
                    type="checkbox"
                    checked={form_data.is_superuser}
                    disabled={!canManageAdmins}
                    onChange={(event) => set_form_data({ ...form_data, is_superuser: event.target.checked, is_admin: event.target.checked || form_data.is_admin })}
                  />
                </label>
              </div>
            </div>
            <div className={styles.modalActions}>
              <button onClick={() => set_show_add(false)} className={`${styles.modalButton} ${styles.modalButtonCancel}`}>Abort</button>
              <button onClick={() => void handle_add()} className={`${styles.modalButton} ${styles.modalButtonPrimary}`} disabled={saving}>
                Create
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default IdentityManagement;
