
import React, { useState, useEffect } from 'react';
import { Icons } from '../constants';
import { UserStatus, User } from '../types';
import styles from './UserManagement.module.css';
import { backendService } from '../services/backendService';

interface UserManagementProps {
  tenant_id: string;
}

const UserManagement: React.FC<UserManagementProps> = ({ tenant_id }) => {
  const [users, set_users] = useState<User[]>([]);
  const [show_invite, set_show_invite] = useState(false);
  const [invite_email, set_invite_email] = useState('');
  const [invite_role, set_invite_role] = useState('L1_USER');

  const load_users = async () => {
    const list = await backendService.getUsers(tenant_id);
    set_users(list);
  };

  useEffect(() => {
    void load_users();
  }, [tenant_id]);

  const handle_invite = async () => {
    if (!invite_email) return;
    const new_user: User = {
      id: crypto.randomUUID(),
      tenant_id: tenant_id,
      username: invite_email.split('@')[0],
      email: invite_email,
      roles: [invite_role.toLowerCase()],
      status: UserStatus.PENDING,
      last_login: new Date().toISOString(),
    };
    await backendService.createUser(new_user);
    await load_users();
    set_show_invite(false);
    set_invite_email('');
  };

  const handle_delete = async (id: string) => {
    if (confirm('Evict this entity from the tenant? Session tokens will be invalidated.')) {
      await backendService.deleteUser(id);
      await load_users();
    }
  };

  const handle_status_toggle = async (user: User) => {
    const updated = {
      ...user,
      status: user.status === UserStatus.ACTIVE ? UserStatus.SUSPENDED : UserStatus.ACTIVE,
    };
    await backendService.updateUser(updated);
    await load_users();
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div>
          <h1 className={styles.title}>Tenant Members</h1>
          <p className={styles.subtitle}>Onboard, invite, and audit identity access.</p>
        </div>
        <div className={styles.headerActions}>
          <button className={styles.buttonBase}>Bulk Sync</button>
          <button onClick={() => set_show_invite(true)} className={`${styles.buttonBase} ${styles.buttonPrimary}`}>Invite Entity</button>
        </div>
      </div>

      <div className={styles.tableCard}>
        <table className={styles.table}>
          <thead>
            <tr className={styles.tableHeaderRow}>
              <th className={styles.tableHeaderCell}>Identity / Subject</th>
              <th className={styles.tableHeaderCell}>Status</th>
              <th className={styles.tableHeaderCell}>Logic Role</th>
              <th className={styles.tableHeaderCell}>Last Pulse</th>
              <th className={`${styles.tableHeaderCell} ${styles.tableHeaderCellRight}`}>Settings</th>
            </tr>
          </thead>
          <tbody className={styles.tableBody}>
            {users.map((user) => (
              <tr key={user.id} className={styles.tableRow}>
                <td className={styles.tableCell}>
                  <div className={styles.userInfo}>
                    <div className={styles.userAvatar}>
                      {user.username.slice(0, 1).toUpperCase()}
                    </div>
                    <div>
                      <p className={styles.userName}>{user.username}</p>
                      <p className={styles.userEmail}>{user.email}</p>
                    </div>
                  </div>
                </td>
                <td className={styles.tableCell}>
                  <button
                    onClick={() => void handle_status_toggle(user)}
                    className={`${styles.statusButton} ${
                      user.status === UserStatus.ACTIVE ? styles.statusActive :
                      user.status === UserStatus.SUSPENDED ? styles.statusSuspended : styles.statusPending
                    }`}
                  >
                    {user.status}
                  </button>
                </td>
                <td className={styles.tableCell}>
                  <div className={styles.rolesList}>
                    {user.roles.map(role => (
                      <span key={role} className={styles.roleBadge}>
                        {role}
                      </span>
                    ))}
                  </div>
                </td>
                <td className={styles.tableCell}>
                  <span className={styles.lastLogin}>{user.last_login}</span>
                </td>
                <td className={`${styles.tableCell} ${styles.tableCellRight}`}>
                  <div className={styles.rowActions}>
                    <button className={styles.rowActionButton}>
                      <Icons.Settings />
                    </button>
                    <button onClick={() => void handle_delete(user.id)} className={`${styles.rowActionButton} ${styles.rowActionDelete}`}>
                      <Icons.Activity />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {show_invite && (
        <div className={styles.modalOverlay}>
          <div className={styles.modal}>
            <h3 className={styles.modalTitle}>Invite New Entity</h3>
            <div className={styles.modalBody}>
              <div>
                <label className={styles.formLabel}>Primary Email</label>
                <input
                  type="email"
                  value={invite_email}
                  onChange={e => set_invite_email(e.target.value)}
                  placeholder="neural-subject-01@domain.io"
                  className={styles.formInput}
                />
              </div>
              <div>
                <label className={styles.formLabel}>Default Tier</label>
                <select
                  value={invite_role}
                  onChange={e => set_invite_role(e.target.value)}
                  className={styles.formSelect}
                >
                  <option value="L1_USER">L1_USER</option>
                  <option value="L2_OPERATOR">L2_OPERATOR</option>
                  <option value="L3_ADMIN">L3_ADMIN</option>
                </select>
              </div>
            </div>
            <div className={styles.modalActions}>
              <button onClick={() => set_show_invite(false)} className={`${styles.modalButton} ${styles.modalButtonCancel}`}>Abort</button>
              <button onClick={() => void handle_invite()} className={`${styles.modalButton} ${styles.modalButtonPrimary}`}>Send Invite</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default UserManagement;
