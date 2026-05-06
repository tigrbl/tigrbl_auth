
import React, { useState, useEffect } from 'react';
import { Icons } from '../constants';
import { OAuthClient } from '../types';
import styles from './ClientManagement.module.css';
import { backendService } from '../services/backendService';
import {
  authorizeClientMutation,
  exposeClientRecord,
  type DelegatedAdminScope,
} from '../services/governancePolicy';

interface ClientManagementProps {
  tenant_id: string;
  delegated_scope?: DelegatedAdminScope | null;
}

const is_uuid = (value: string) => /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(value);

type ManagedClient = Pick<OAuthClient, 'id' | 'tenant_id' | 'name' | 'client_id' | 'type' | 'redirect_uris'> & Partial<OAuthClient>;

const ClientManagement: React.FC<ClientManagementProps> = ({ tenant_id, delegated_scope }) => {
  const [clients, set_clients] = useState<ManagedClient[]>([]);
  const [show_modal, set_show_modal] = useState(false);
  const [editing_client, set_editing_client] = useState<ManagedClient | null>(null);
  const [show_secret, set_show_secret] = useState<Record<string, boolean>>({});
  const [form_data, set_form_data] = useState<Partial<OAuthClient>>({
    name: '',
    client_id: '',
    type: 'public',
    redirect_uris: ['']
  });

  const load_clients = async () => {
    const list = await backendService.getClients(tenant_id);
    set_clients(
      list.map((client) => ({
        ...client,
        ...exposeClientRecord(client, 'admin', delegated_scope),
      })),
    );
  };

  useEffect(() => {
    void load_clients();
  }, [tenant_id]);

  const handle_save = async () => {
    if (!form_data.name || !form_data.client_id) return;
    if (!is_uuid(form_data.client_id)) {
      alert('Client ID must be a valid UUID for backend storage.');
      return;
    }

    const patch: Partial<OAuthClient> = {
      name: form_data.name,
      client_id: form_data.client_id,
      type: form_data.type as 'public' | 'confidential',
      redirect_uris: form_data.redirect_uris?.filter(u => u !== '') || []
    };

    if (editing_client) {
      const authorization = authorizeClientMutation(tenant_id, patch, delegated_scope, 'client.update');
      if (!authorization.allowed) {
        alert(authorization.reason);
        return;
      }
      const updated: OAuthClient = {
        ...editing_client,
        ...patch,
      };
      await backendService.updateClient(updated);
    } else {
      const createAuthorization = authorizeClientMutation(tenant_id, patch, delegated_scope, 'client.create');
      if (!createAuthorization.allowed) {
        alert(createAuthorization.reason);
        return;
      }
      const client: OAuthClient = {
        id: crypto.randomUUID(),
        tenant_id,
        name: patch.name ?? '',
        client_id: patch.client_id ?? '',
        type: patch.type as 'public' | 'confidential',
        redirect_uris: patch.redirect_uris ?? [],
        client_secret: form_data.type === 'confidential' ? 'sk_live_' + crypto.randomUUID().replace(/-/g, '').slice(0, 16) : undefined
      };
      await backendService.createClient(client);
    }

    await load_clients();
    set_show_modal(false);
    set_editing_client(null);
    set_form_data({ name: '', client_id: '', type: 'public', redirect_uris: [''] });
  };

  const handle_delete = async (id: string) => {
    const authorization = authorizeClientMutation(tenant_id, {}, delegated_scope, 'client.delete');
    if (!authorization.allowed) {
      alert(authorization.reason);
      return;
    }
    if (confirm('Permanently de-register this OAuth application? All session tokens will be invalidated immediately.')) {
      await backendService.deleteClient(id);
      await load_clients();
    }
  };

  const open_edit = (client: OAuthClient) => {
    set_editing_client(client);
    set_form_data({
      name: client.name,
      client_id: client.client_id,
      type: client.type,
      redirect_uris: client.redirect_uris.length > 0 ? [...client.redirect_uris] : ['']
    });
    set_show_modal(true);
  };

  const toggle_secret_visibility = (id: string) => {
    set_show_secret(prev => ({ ...prev, [id]: !prev[id] }));
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div>
          <h1 className={styles.title}>OAuth Clients</h1>
          <p className={styles.subtitle}>Provision OIDC compliant credentials for the namespace flux.</p>
          {delegated_scope && (
            <p className={styles.subtitle}>
              Delegated client scope for {delegated_scope.subject}: secrets and restricted fields remain redacted.
            </p>
          )}
        </div>
        <button onClick={() => { set_editing_client(null); set_form_data({ name: '', client_id: '', type: 'public', redirect_uris: [''] }); set_show_modal(true); }} className={styles.primaryButton}>Register Application</button>
      </div>

      <div className={styles.layoutGrid}>
        {clients.map(client => (
          <div key={client.id} className={styles.card}>
            <div className={styles.cardActions}>
               <button onClick={() => open_edit(client)} className={styles.actionButton}><Icons.Settings /></button>
               <button onClick={() => void handle_delete(client.id)} className={`${styles.actionButton} ${styles.actionButtonDelete}`}><Icons.Activity /></button>
            </div>

            <div className={styles.cardHeader}>
              <div className={styles.avatar}>
                {client.name[0]}
              </div>
              <div>
                <h3 className={styles.cardTitle}>{client.name}</h3>
                <span className={`${styles.typeBadge} ${client.type === 'confidential' ? styles.typeBadgeConfidential : styles.typeBadgePublic}`}>
                  {client.type}
                </span>
              </div>
            </div>

            <div className={styles.details}>
              <div>
                <p className={styles.label}>Application ID</p>
                <div className={styles.idRow}>
                  <p className={styles.idValue}>{client.client_id}</p>
                </div>
              </div>

              {client.type === 'confidential' && client.client_secret && (
                <div>
                  <div className={styles.secretHeader}>
                    <p className={styles.label}>Client Secret</p>
                    <button onClick={() => toggle_secret_visibility(client.id)} className={styles.secretToggle}>
                      {show_secret[client.id] ? 'Hide' : 'Reveal'}
                    </button>
                  </div>
                  <p className={styles.secretValue}>
                    {show_secret[client.id] ? client.client_secret : '••••••••••••••••'}
                  </p>
                </div>
              )}

              <div>
                <p className={styles.label}>Redirect URIs</p>
                <div className={styles.redirectList}>
                  {client.redirect_uris.map((uri, idx) => (
                    <p key={idx} className={styles.redirectItem}>{uri}</p>
                  ))}
                  {client.redirect_uris.length === 0 && <p className={styles.redirectEmpty}>No URIs defined.</p>}
                </div>
              </div>
            </div>

            <div className={styles.cardFooter}>
               <span className={styles.cardMeta}>REGISTERED: {client.created_at || 'ALPHA'}</span>
               <div className={styles.cardDots}>
                  <div className={styles.dot}></div>
                  <div className={styles.dot}></div>
                  <div className={styles.dot}></div>
               </div>
            </div>
          </div>
        ))}
      </div>

      {show_modal && (
        <div className={styles.modalOverlay}>
          <div className={styles.modal}>
            <h3 className={styles.modalTitle}>{editing_client ? 'Modify Registration' : 'New Application Record'}</h3>
            <div className={styles.modalBody}>
              <div className={styles.formGrid}>
                <div className={styles.formSpan}>
                  <label className={styles.formLabel}>Display Name</label>
                  <input type="text" value={form_data.name} onChange={e => set_form_data({...form_data, name: e.target.value})} className={styles.formInput} placeholder="E.g. Mobile App v2" />
                </div>
                <div>
                  <label className={styles.formLabel}>Client ID UUID</label>
                  <input type="text" value={form_data.client_id} onChange={e => set_form_data({...form_data, client_id: e.target.value})} className={`${styles.formInput} ${styles.formInputMono}`} placeholder="9f4f0fc7-fce0-4d67-a6b4-8f8bd7cdca5e" />
                </div>
                <div>
                  <label className={styles.formLabel}>Application Type</label>
                  <select value={form_data.type} onChange={e => set_form_data({...form_data, type: e.target.value as any})} className={styles.formSelect}>
                    <option value="public">Public (SPA/Mobile)</option>
                    <option value="confidential">Confidential (Server)</option>
                  </select>
                </div>
              </div>
              <div>
                <label className={styles.formLabel}>Permitted Redirect URIs (CSV)</label>
                <textarea
                  value={form_data.redirect_uris?.join(', ')}
                  onChange={e => set_form_data({...form_data, redirect_uris: e.target.value.split(',').map(s => s.trim())})}
                  className={styles.formTextarea}
                  placeholder="https://app.com/callback, http://localhost:3000"
                />
              </div>
            </div>
            <div className={styles.modalActions}>
              <button onClick={() => set_show_modal(false)} className={`${styles.modalButton} ${styles.modalButtonCancel}`}>Abort</button>
              <button onClick={() => void handle_save()} className={`${styles.modalButton} ${styles.modalButtonPrimary}`}>Commit Record</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ClientManagement;
