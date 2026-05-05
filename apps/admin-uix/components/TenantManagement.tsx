
import React, { useState } from 'react';
import { Icons } from '../constants';
import { Tenant } from '../types';
import styles from './TenantManagement.module.css';
import { backendService } from '../services/backendService';

interface TenantManagementProps {
  tenants: Tenant[];
  on_refresh?: () => Promise<void>;
  on_select_tenant: (tenant: Tenant) => void;
}

const TenantManagement: React.FC<TenantManagementProps> = ({ tenants, on_refresh, on_select_tenant }) => {
  const [show_create, set_show_create] = useState(false);
  const [new_tenant, set_new_tenant] = useState({ name: '', slug: '', description: '' });

  const handle_create = async () => {
    if (!new_tenant.name || !new_tenant.slug) return;
    await backendService.createTenant({
      name: new_tenant.name,
      slug: new_tenant.slug,
      description: new_tenant.description || undefined,
    });
    set_show_create(false);
    set_new_tenant({ name: '', slug: '', description: '' });
    await on_refresh?.();
  };

  const handle_delete = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (confirm('Permanently purge this namespace and all associated objects? This action cannot be undone.')) {
      await backendService.deleteTenant(id);
      await on_refresh?.();
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div>
          <h1 className={styles.title}>Tenant Control</h1>
          <p className={styles.subtitle}>Provision, isolate, and architect multi-tenant namespaces.</p>
        </div>
        <button onClick={() => set_show_create(true)} className={styles.primaryButton}>Provision New Tenant</button>
      </div>

      <div className={styles.layoutGrid}>
        {tenants.map(tenant => (
          <div
            key={tenant.id}
            onClick={() => on_select_tenant(tenant)}
            className={styles.card}
          >
            <div className={styles.cardActions}>
               <button onClick={(e) => void handle_delete(tenant.id, e)} className={styles.deleteButton}>&times;</button>
            </div>

            <div className={styles.cardHeader}>
              <div className={styles.cardAvatar}>
                {tenant.name[0]}
              </div>
              <div>
                 <h3 className={styles.cardTitle}>{tenant.name}</h3>
                 <p className={styles.cardMeta}>NAMESPACE: {tenant.slug}</p>
              </div>
            </div>

            <p className={styles.cardDescription}>
              {tenant.description || 'General purpose security namespace for tigrbl_auth infrastructure.'}
            </p>

            <div className={styles.cardFooter}>
               <div className={styles.status}>
                  <div className={styles.statusDot}></div>
                  <span className={styles.statusText}>Active Status</span>
               </div>
               <Icons.Activity />
            </div>
          </div>
        ))}
      </div>

      {show_create && (
        <div className={styles.modalOverlay}>
          <div className={styles.modal}>
            <h3 className={styles.modalTitle}>Architect Namespace</h3>
            <div className={styles.modalBody}>
              <div>
                <label className={styles.formLabel}>Display Name</label>
                <input type="text" value={new_tenant.name} onChange={e => set_new_tenant({...new_tenant, name: e.target.value})} className={styles.formInput} placeholder="E.g. Engineering Sandbox" />
              </div>
              <div>
                <label className={styles.formLabel}>Slug / Identifier</label>
                <input type="text" value={new_tenant.slug} onChange={e => set_new_tenant({...new_tenant, slug: e.target.value.toLowerCase().replace(/\s+/g, '-')})} className={`${styles.formInput} ${styles.formInputMono}`} placeholder="eng-sandbox" />
              </div>
              <div>
                <label className={styles.formLabel}>Objective Description</label>
                <textarea value={new_tenant.description} onChange={e => set_new_tenant({...new_tenant, description: e.target.value})} className={styles.formTextarea} placeholder="Primary namespace for development assets." />
              </div>
              <div className={styles.modalActions}>
                <button onClick={() => set_show_create(false)} className={`${styles.modalButton} ${styles.modalButtonCancel}`}>Abort</button>
                <button onClick={() => void handle_create()} className={`${styles.modalButton} ${styles.modalButtonPrimary}`}>Provision</button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TenantManagement;
