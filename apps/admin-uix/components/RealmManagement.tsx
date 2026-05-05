
import React, { useState } from 'react';
import { Icons } from '../constants';
import { Realm } from '../types';
import styles from './RealmManagement.module.css';
import { backendService } from '../services/backendService';

interface RealmManagementProps {
  realms: Realm[];
  on_refresh?: () => Promise<void>;
  on_select_realm: (realm: Realm) => void;
}

const RealmManagement: React.FC<RealmManagementProps> = ({ realms, on_refresh, on_select_realm }) => {
  const [show_create, set_show_create] = useState(false);
  const [new_realm, set_new_realm] = useState({ name: '', slug: '', description: '' });

  const handle_create = async () => {
    if (!new_realm.name || !new_realm.slug) return;
    await backendService.createRealm({
      name: new_realm.name,
      slug: new_realm.slug,
      description: new_realm.description || undefined,
    });
    set_show_create(false);
    set_new_realm({ name: '', slug: '', description: '' });
    await on_refresh?.();
  };

  const handle_delete = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (confirm('Permanently purge this namespace and all associated objects? This action cannot be undone.')) {
      await backendService.deleteRealm(id);
      await on_refresh?.();
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div>
          <h1 className={styles.title}>Realm Control</h1>
          <p className={styles.subtitle}>Provision, isolate, and architect multi-tenant namespaces.</p>
        </div>
        <button onClick={() => set_show_create(true)} className={styles.primaryButton}>Provision New Realm</button>
      </div>

      <div className={styles.layoutGrid}>
        {realms.map(realm => (
          <div
            key={realm.id}
            onClick={() => on_select_realm(realm)}
            className={styles.card}
          >
            <div className={styles.cardActions}>
               <button onClick={(e) => void handle_delete(realm.id, e)} className={styles.deleteButton}>&times;</button>
            </div>

            <div className={styles.cardHeader}>
              <div className={styles.cardAvatar}>
                {realm.name[0]}
              </div>
              <div>
                 <h3 className={styles.cardTitle}>{realm.name}</h3>
                 <p className={styles.cardMeta}>NAMESPACE: {realm.slug}</p>
              </div>
            </div>

            <p className={styles.cardDescription}>
              {realm.description || 'General purpose security namespace for Aegis infrastructure.'}
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
                <input type="text" value={new_realm.name} onChange={e => set_new_realm({...new_realm, name: e.target.value})} className={styles.formInput} placeholder="E.g. Engineering Sandbox" />
              </div>
              <div>
                <label className={styles.formLabel}>Slug / Identifier</label>
                <input type="text" value={new_realm.slug} onChange={e => set_new_realm({...new_realm, slug: e.target.value.toLowerCase().replace(/\s+/g, '-')})} className={`${styles.formInput} ${styles.formInputMono}`} placeholder="eng-sandbox" />
              </div>
              <div>
                <label className={styles.formLabel}>Objective Description</label>
                <textarea value={new_realm.description} onChange={e => set_new_realm({...new_realm, description: e.target.value})} className={styles.formTextarea} placeholder="Primary namespace for development assets." />
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

export default RealmManagement;
