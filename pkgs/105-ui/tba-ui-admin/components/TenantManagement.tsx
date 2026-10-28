
import React, { useState } from 'react';
import { Icons } from '../constants';
import { Tenant } from '../types';
import styles from './TenantManagement.module.css';
import { backendService } from '../services/backendService';
import type { DelegatedAdminScope } from '../services/governancePolicy';
import { humanizeError } from '../services/errorMessages';

interface TenantManagementProps {
  tenants: Tenant[];
  delegated_scope?: DelegatedAdminScope | null;
  on_refresh?: () => Promise<void>;
  on_select_tenant: (tenant: Tenant) => void;
}

const TenantManagement: React.FC<TenantManagementProps> = ({ tenants, delegated_scope, on_refresh, on_select_tenant }) => {
  const [show_create, set_show_create] = useState(false);
  const [new_tenant, set_new_tenant] = useState({ name: '', slug: '', email: '' });
  const [feedback, set_feedback] = useState<{ tone: 'success' | 'error'; message: string } | null>(null);
  const [form_error, set_form_error] = useState<string | null>(null);
  const [is_submitting, set_is_submitting] = useState(false);

  const handle_create = async () => {
    const name = new_tenant.name.trim();
    const slug = new_tenant.slug.trim().toLowerCase();
    const email = new_tenant.email.trim().toLowerCase();

    set_form_error(null);
    set_feedback(null);

    if (!name || !slug || !email) {
      set_form_error('Display name, slug, and tenant contact email are required.');
      return;
    }

    const duplicate = tenants.find((tenant) => (
      tenant.slug.toLowerCase() === slug
      || tenant.name.trim().toLowerCase() === name.toLowerCase()
      || tenant.email?.trim().toLowerCase() === email
    ));
    if (duplicate) {
      set_form_error(`Tenant ${duplicate.name} already uses this slug, name, or email.`);
      return;
    }

    set_is_submitting(true);
    try {
      const created = await backendService.createTenant({ name, slug, email });
      set_show_create(false);
      set_new_tenant({ name: '', slug: '', email: '' });
      set_feedback({ tone: 'success', message: `Tenant ${created.name} was provisioned.` });
      await on_refresh?.();
    } catch (error) {
      const message = humanizeError(error, 'Failed to provision tenant.');
      set_form_error(message);
      set_feedback({ tone: 'error', message });
    } finally {
      set_is_submitting(false);
    }
  };

  const handle_delete = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (confirm('Permanently delete this tenant and its associated records? This action cannot be undone.')) {
      await backendService.deleteTenant(id);
      await on_refresh?.();
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div>
          <h1 className={styles.title}>Tenants</h1>
          <p className={styles.subtitle}>Create, select, and delete tenant records.</p>
          {delegated_scope && (
            <p className={styles.subtitle}>
              Scoped delegated view for {delegated_scope.subject}: {tenants.length} visible tenant{tenants.length === 1 ? '' : 's'}.
            </p>
          )}
        </div>
        <button
          onClick={() => {
            set_form_error(null);
            set_show_create(true);
          }}
          className={styles.primaryButton}
        >
          Create Tenant
        </button>
      </div>

      {feedback && (
        <div
          className={`${styles.feedback} ${feedback.tone === 'success' ? styles.feedbackSuccess : styles.feedbackError}`}
          role={feedback.tone === 'error' ? 'alert' : 'status'}
          aria-live="polite"
        >
          {feedback.message}
        </div>
      )}

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
                 <p className={styles.cardMeta}>SLUG: {tenant.slug}</p>
              </div>
            </div>

            <p className={styles.cardDescription}>
              {tenant.email || tenant.description || 'No tenant contact email has been configured.'}
            </p>

            <div className={styles.cardFooter}>
              <div className={styles.status}>
                  <div className={styles.statusDot}></div>
                  <span className={styles.statusText}>Selectable</span>
               </div>
               <Icons.Activity />
            </div>
          </div>
        ))}
      </div>

      {show_create && (
        <div className={styles.modalOverlay}>
          <div className={styles.modal}>
            <h3 className={styles.modalTitle}>Create Tenant</h3>
            <div className={styles.modalBody}>
              {form_error && (
                <div className={styles.formError} role="alert" aria-live="assertive">
                  {form_error}
                </div>
              )}
              <div>
                <label className={styles.formLabel}>Display Name</label>
                <input type="text" value={new_tenant.name} onChange={e => set_new_tenant({...new_tenant, name: e.target.value})} className={styles.formInput} placeholder="E.g. Engineering Sandbox" />
              </div>
              <div>
                <label className={styles.formLabel}>Slug / Identifier</label>
                <input type="text" value={new_tenant.slug} onChange={e => set_new_tenant({...new_tenant, slug: e.target.value.toLowerCase().replace(/\s+/g, '-')})} className={`${styles.formInput} ${styles.formInputMono}`} placeholder="eng-sandbox" />
              </div>
              <div>
                <label className={styles.formLabel}>Tenant Contact Email</label>
                <input type="email" value={new_tenant.email} onChange={e => set_new_tenant({...new_tenant, email: e.target.value.trim().toLowerCase()})} className={styles.formInput} placeholder="eng-sandbox@example.com" />
              </div>
              <div className={styles.modalActions}>
                <button
                  onClick={() => {
                    set_form_error(null);
                    set_show_create(false);
                  }}
                  className={`${styles.modalButton} ${styles.modalButtonCancel}`}
                  disabled={is_submitting}
                >
                  Abort
                </button>
                <button
                  onClick={() => void handle_create()}
                  className={`${styles.modalButton} ${styles.modalButtonPrimary}`}
                  disabled={is_submitting}
                >
                  {is_submitting ? 'Creating...' : 'Create'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TenantManagement;
