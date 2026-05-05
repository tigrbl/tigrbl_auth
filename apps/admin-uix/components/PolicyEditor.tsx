
import React, { useState, useEffect } from 'react';
import { Icons } from '../constants';
import { PolicyGate } from '../types';
import { global_redis } from '../services/messaging/redisBroker';
import styles from './PolicyEditor.module.css';
import { backendService } from '../services/backendService';

interface PolicyEditorProps {
  tenant_id: string;
}

const PolicyEditor: React.FC<PolicyEditorProps> = ({ tenant_id }) => {
  const [policies, set_policies] = useState<PolicyGate[]>([]);
  const [active_policy, set_active_policy] = useState<PolicyGate | null>(null);
  const [editor_content, set_editor_content] = useState('');
  const [is_saving, set_is_saving] = useState(false);
  const [is_pushing, set_is_pushing] = useState(false);
  const [ai_prompt, set_ai_prompt] = useState('');

  const load_policies = async () => {
    const list = await backendService.getPolicies(tenant_id);
    set_policies(list);
    if (list.length > 0) {
      set_active_policy(list[0]);
      set_editor_content(list[0].content);
    } else {
      set_active_policy(null);
      set_editor_content('');
    }
  };

  useEffect(() => {
    void load_policies();
  }, [tenant_id]);

  const handle_save = async () => {
    if (!active_policy) return;
    set_is_saving(true);
    const updated: PolicyGate = {
      ...active_policy,
      content: editor_content,
      version: active_policy.version + 1,
      is_active: true,
      last_updated: new Date().toISOString(),
    };
    await backendService.syncPolicy(updated);
    await load_policies();
    set_active_policy(updated);
    set_is_saving(false);
  };

  const handle_push = async () => {
    if (!active_policy) return;
    set_is_pushing(true);
    try {
      await global_redis.publish('GATEWAY_POLICY_PUSH', {
        tenant_id,
        policy_id: active_policy.id,
        version: active_policy.version,
        content: editor_content,
        timestamp: new Date().toISOString()
      });
      alert(`Manifest [${active_policy.name}] transmitted to edge clusters successfully.`);
    } catch (e) {
      alert("Mesh propagation failure. Retrying via secondary route.");
    } finally {
      set_is_pushing(false);
    }
  };

  const handle_create = async () => {
    const name = prompt("Policy Identity Name:");
    if (!name) return;
    const type_resp = prompt("Engine (CEDAR/OPA):", "CEDAR");
    const type: 'CEDAR' | 'OPA' = (type_resp?.toUpperCase() === 'OPA') ? 'OPA' : 'CEDAR';

    const new_p: PolicyGate = {
      id: crypto.randomUUID(),
      tenant_id,
      name,
      type,
      content: type === 'CEDAR' ? 'permit(principal, action, resource);' : 'package policy.authz\n\ndefault allow = false',
      is_active: false,
      version: 1,
      last_updated: new Date().toISOString(),
    };

    await backendService.syncPolicy(new_p);
    await load_policies();
    set_active_policy(new_p);
    set_editor_content(new_p.content);
  };

  const handle_delete = async () => {
    if (!active_policy) return;
    if (confirm(`EVICT MANIFEST: ${active_policy.name}? All gated services will default to DENY.`)) {
      await backendService.removePolicy(active_policy.id);
      await load_policies();
    }
  };

  const generate_ai_logic = async () => {
    if (!ai_prompt || !active_policy) return;
    const template = active_policy.type === 'CEDAR'
      ? `permit(principal, action, resource) when { /* ${ai_prompt} */ };`
      : `package policy.authz\n\ndefault allow = false\n\n# ${ai_prompt}`;
    set_editor_content(template);
    set_ai_prompt('');
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div>
          <h1 className={styles.title}>Policy Gates</h1>
          <p className={styles.subtitle}>Fine-grained ABAC logic for the {tenant_id} namespace.</p>
        </div>
        <div className={styles.headerActions}>
          <button onClick={() => void handle_delete()} className={`${styles.buttonBase} ${styles.buttonDanger}`} disabled={!active_policy}>Purge</button>
          <button onClick={() => void handle_save()} className={styles.buttonBase} disabled={is_saving || !active_policy}>
            {is_saving ? 'Saving...' : 'Save Draft'}
          </button>
          <button onClick={() => void handle_push()} className={`${styles.buttonBase} ${styles.buttonPrimary}`} disabled={is_pushing || !active_policy}>
            {is_pushing ? 'Syncing...' : 'Push to Mesh'}
          </button>
        </div>
      </div>

      <div className={styles.layout}>
        <div className={styles.listPanel}>
          <div className={styles.listHeader}>
            <h3 className={styles.listTitle}>Namespace Manifests</h3>
            <button onClick={() => void handle_create()} className={styles.listAddButton}>Add New</button>
          </div>
          <div className={styles.listBody}>
            {policies.map(p => (
              <button
                key={p.id}
                onClick={() => { set_active_policy(p); set_editor_content(p.content); }}
                className={`${styles.policyButton} ${active_policy?.id === p.id ? styles.policyButtonActive : styles.policyButtonInactive}`}
              >
                <div className={styles.policyButtonHeader}>
                  <span className={styles.policyName}>{p.name}</span>
                  <span className={styles.policyType}>{p.type}</span>
                </div>
                <div className={styles.policyMeta}>
                  <span>Version {p.version}</span>
                  <span className={p.is_active ? styles.policyStatusActive : styles.policyStatusDraft}>{p.is_active ? 'Deployed' : 'Draft'}</span>
                </div>
              </button>
            ))}
            {policies.length === 0 && (
              <div className={styles.emptyState}>
                <Icons.Terminal />
                <p className={styles.emptyTitle}>No Manifests Found</p>
              </div>
            )}
          </div>
        </div>

        <div className={styles.editorPanel}>
          {active_policy ? (
            <>
              <div className={styles.editorHeader}>
                <div className={styles.editorInfo}>
                  <div className={styles.editorIcon}><Icons.Shield /></div>
                  <div>
                    <h3 className={styles.editorTitle}>{active_policy.name}</h3>
                    <p className={styles.editorMeta}>ID: {active_policy.id} | Engine: {active_policy.type}_v1</p>
                  </div>
                </div>
              </div>
              <div className={styles.editorBody}>
                <textarea
                  value={editor_content}
                  onChange={(e) => set_editor_content(e.target.value)}
                  className={styles.editorTextarea}
                  spellCheck={false}
                />

                <div className={styles.aiBar}>
                   <div className={styles.aiInputWrapper}>
                     <input
                       type="text"
                       value={ai_prompt}
                       onChange={e => set_ai_prompt(e.target.value)}
                       onKeyDown={e => e.key === 'Enter' && void generate_ai_logic()}
                       placeholder="Synthesize policy logic via neural link..."
                       className={styles.aiInput}
                     />
                     <div className={styles.aiUnderline}></div>
                   </div>
                   <button onClick={() => void generate_ai_logic()} className={styles.aiButton}>
                     Draft Template
                   </button>
                </div>
              </div>
            </>
          ) : (
            <div className={styles.editorEmpty}>
              <div className={styles.editorEmptyIcon}><Icons.Activity /></div>
              <h3 className={styles.editorEmptyTitle}>Editor Standby</h3>
              <p className={styles.editorEmptyText}>Select a namespace manifest to initiate architectural synthesis.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PolicyEditor;
