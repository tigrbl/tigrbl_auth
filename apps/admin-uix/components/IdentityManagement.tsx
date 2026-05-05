
import React, { useState } from 'react';
import { controlPlaneStateService, Identity } from '../services/controlPlaneStateService';
import { Icons } from '../constants';
import { UserStatus } from '../types';
import styles from './IdentityManagement.module.css';

const IdentityManagement: React.FC = () => {
  const [identities, set_identities] = useState<Identity[]>(controlPlaneStateService.get_identities());
  const [selected_id, set_selected_id] = useState<Identity | null>(null);
  const [show_add, set_show_add] = useState(false);
  const [form_data, set_form_data] = useState({
    full_name: '',
    email: '',
    provider: 'local' as const,
    mfa_enabled: false
  });

  const refresh = () => set_identities(controlPlaneStateService.get_identities());

  const handle_add = () => {
    if (!form_data.full_name || !form_data.email) return;
    controlPlaneStateService.add_identity({
      id: crypto.randomUUID(),
      full_name: form_data.full_name,
      email: form_data.email,
      provider: form_data.provider,
      mfa_enabled: form_data.mfa_enabled,
      created_at: new Date().toISOString().split('T')[0],
      roles: ['user'],
      status: UserStatus.ACTIVE
    });
    refresh();
    set_show_add(false);
    set_form_data({ full_name: '', email: '', provider: 'local', mfa_enabled: false });
  };

  const handle_delete = (id: string) => {
    if (confirm('Permanently redact this identity from the central pool? This action is irreversible.')) {
      controlPlaneStateService.delete_identity(id);
      refresh();
      set_selected_id(null);
    }
  };

  const handle_status_change = (id: string, status: UserStatus) => {
    const target = identities.find(i => i.id === id);
    if (target) {
      controlPlaneStateService.update_identity({ ...target, status });
      refresh();
      set_selected_id({ ...target, status });
    }
  };

  const handle_mfa_toggle = (id: string) => {
    const target = identities.find(i => i.id === id);
    if (target) {
      controlPlaneStateService.update_identity({ ...target, mfa_enabled: !target.mfa_enabled });
      refresh();
      set_selected_id({ ...target, mfa_enabled: !target.mfa_enabled });
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div>
          <h1 className={styles.title}>Identity Pool</h1>
          <p className={styles.subtitle}>Global subject directory and cross-namespace IDP master records.</p>
        </div>
        <div className={styles.headerActions}>
          <button onClick={() => refresh()} className={styles.buttonBase}>Sync Providers</button>
          <button onClick={() => set_show_add(true)} className={`${styles.buttonBase} ${styles.buttonPrimary}`}>Manual Provision</button>
        </div>
      </div>

      <div className={styles.layoutGrid}>
        <div className={styles.tableColumn}>
          <div className={styles.tableCard}>
            <table className={styles.table}>
              <thead>
                <tr className={styles.tableHeaderRow}>
                  <th className={styles.tableHeaderCell}>Subject Information</th>
                  <th className={styles.tableHeaderCell}>Auth Source</th>
                  <th className={styles.tableHeaderCell}>Status</th>
                  <th className={`${styles.tableHeaderCell} ${styles.tableHeaderCellRight}`}>Actions</th>
                </tr>
              </thead>
              <tbody className={styles.tableBody}>
                {identities.map((id) => (
                  <tr key={id.id} className={`${styles.tableRow} ${selected_id?.id === id.id ? styles.tableRowSelected : ''}`} onClick={() => set_selected_id(id)}>
                    <td className={styles.tableCell}>
                      <div className={styles.subjectInfo}>
                        <div className={`${styles.subjectAvatar} ${selected_id?.id === id.id ? styles.subjectAvatarActive : ''}`}>
                          {id.full_name[0]}
                        </div>
                        <div>
                          <p className={styles.subjectName}>{id.full_name}</p>
                          <p className={styles.subjectEmail}>{id.email}</p>
                        </div>
                      </div>
                    </td>
                    <td className={styles.tableCell}>
                      <span className={styles.providerBadge}>
                        {id.provider}
                      </span>
                    </td>
                    <td className={styles.tableCell}>
                      <span className={`${styles.statusBadge} ${
                        id.status === UserStatus.ACTIVE ? styles.statusActive :
                        id.status === UserStatus.SUSPENDED ? styles.statusSuspended : styles.statusPending
                      }`}>
                        {id.status}
                      </span>
                    </td>
                    <td className={`${styles.tableCell} ${styles.tableCellRight}`}>
                       <button onClick={(e) => { e.stopPropagation(); handle_delete(id.id); }} className={styles.deleteButton}>
                         <Icons.Activity />
                       </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className={styles.detailColumn}>
          {selected_id ? (
            <div className={styles.detailCard}>
               <div className={styles.detailHeader}>
                  <div className={styles.detailAvatar}>
                    {selected_id.full_name[0]}
                  </div>
                  <div className={styles.detailMeta}>
                    <p className={styles.detailMetaLabel}>Central State</p>
                    <span className={styles.detailMetaBadge}>Linked</span>
                  </div>
               </div>
               <h3 className={styles.detailName}>{selected_id.full_name}</h3>
               <p className={styles.detailId}>{selected_id.id}</p>

               <div className={styles.detailSections}>
                  <div>
                    <p className={styles.detailLabel}>Security Posture</p>
                    <div className={styles.detailRow}>
                      <span className={styles.detailValue}>MFA {selected_id.mfa_enabled ? 'Active' : 'Disabled'}</span>
                      <button onClick={() => handle_mfa_toggle(selected_id.id)} className={styles.detailToggle}>Toggle</button>
                    </div>
                  </div>
                  <div>
                    <p className={styles.detailLabel}>Global Roles</p>
                    <div className={styles.rolesList}>
                      {selected_id.roles.map(r => (
                        <span key={r} className={styles.roleBadge}>{r}</span>
                      ))}
                    </div>
                  </div>
                  <div>
                    <p className={styles.detailLabel}>Lifecycle Status</p>
                    <div className={styles.statusButtons}>
                       <button
                         onClick={() => handle_status_change(selected_id.id, UserStatus.ACTIVE)}
                         className={`${styles.statusButton} ${selected_id.status === UserStatus.ACTIVE ? styles.statusButtonActive : styles.statusButtonInactive}`}
                       >Active</button>
                       <button
                         onClick={() => handle_status_change(selected_id.id, UserStatus.SUSPENDED)}
                         className={`${styles.statusButton} ${selected_id.status === UserStatus.SUSPENDED ? styles.statusButtonSuspendedActive : styles.statusButtonInactive}`}
                       >Suspend</button>
                    </div>
                  </div>
               </div>

               <div className={styles.detailActions}>
                  <button className={styles.detailActionButton}>Audit Global Activity</button>
                  <button onClick={() => handle_delete(selected_id.id)} className={`${styles.detailActionButton} ${styles.detailActionDanger}`}>Revoke & Purge</button>
               </div>
            </div>
          ) : (
            <div className={styles.emptyState}>
               <div className={styles.emptyIcon}><Icons.Users /></div>
               <p className={styles.emptyText}>Select an identity to view administrative controls</p>
            </div>
          )}
        </div>
      </div>

      {show_add && (
        <div className={styles.modalOverlay}>
          <div className={styles.modal}>
            <h3 className={styles.modalTitle}>Provision Subject</h3>
            <div className={styles.modalBody}>
              <div>
                <label className={styles.formLabel}>Subject Full Name</label>
                <input
                  type="text"
                  value={form_data.full_name}
                  onChange={e => set_form_data({...form_data, full_name: e.target.value})}
                  className={styles.formInput}
                />
              </div>
              <div>
                <label className={styles.formLabel}>E-Mail Address</label>
                <input
                  type="email"
                  value={form_data.email}
                  onChange={e => set_form_data({...form_data, email: e.target.value})}
                  className={styles.formInput}
                />
              </div>
              <div className={styles.modalActions}>
                <button onClick={() => set_show_add(false)} className={`${styles.modalButton} ${styles.modalButtonCancel}`}>Abort</button>
                <button onClick={handle_add} className={`${styles.modalButton} ${styles.modalButtonPrimary}`}>Provision</button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default IdentityManagement;
