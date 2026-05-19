import React, { useEffect, useState } from 'react';
import { Icons } from '../constants';
import { backendService } from '../services/backendService';
import type { Tenant, TenantJwksKeyInput, TenantJwksPublicationView as TenantJwksPublication } from '../types';
import styles from './TenantJwksPublicationView.module.css';

type TenantJwksPublicationViewProps = {
  tenant: Tenant;
};

const lifecycles = ['active', 'next', 'retired'];

const TenantJwksPublicationView: React.FC<TenantJwksPublicationViewProps> = ({ tenant }) => {
  const [view, setView] = useState<TenantJwksPublication | null>(null);
  const [loading, setLoading] = useState(true);
  const [mutating, setMutating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [draft, setDraft] = useState<TenantJwksKeyInput>({
    kid: '',
    status: 'active',
    alg: 'EdDSA',
    kty: 'OKP',
    use: 'sig',
    crv: 'Ed25519',
    publish: true,
  });

  const loadView = () => backendService.getTenantJwksPublication(tenant)
    .then((nextView) => {
      setView(nextView);
      return nextView;
    });

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    setView(null);

    void backendService.getTenantJwksPublication(tenant)
      .then((nextView) => {
        if (!cancelled) {
          setView(nextView);
        }
      })
      .catch((caught) => {
        if (!cancelled) {
          setError(caught instanceof Error ? caught.message : 'Tenant JWKS publication is unavailable.');
        }
      })
      .finally(() => {
        if (!cancelled) {
          setLoading(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [tenant.id, tenant.slug]);

  const status = view?.publication_status ?? 'not_published';

  const runMutation = async (action: () => Promise<void>) => {
    setMutating(true);
    setError(null);
    try {
      await action();
      await loadView();
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : 'Tenant JWKS key mutation failed.');
    } finally {
      setMutating(false);
    }
  };

  const submitKey = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!draft.kid.trim()) {
      setError('kid is required.');
      return;
    }
    await runMutation(() => backendService.createTenantJwksKey(tenant, {
      ...draft,
      kid: draft.kid.trim(),
      x: draft.x?.trim() || undefined,
      n: draft.n?.trim() || undefined,
      e: draft.e?.trim() || undefined,
    }));
    setDraft((current) => ({ ...current, kid: '', x: '', n: '', e: '' }));
  };

  return (
    <section className={styles.surface}>
      <div className={styles.header}>
        <div>
          <div className={styles.eyebrow}>Tenant JWKS</div>
          <h1 className={styles.title}>{tenant.name}</h1>
        </div>
        <div className={styles.status}>
          <span className={`${styles.dot} ${status === 'published' ? '' : styles.dotMuted}`} />
          {status.replace('_', ' ')}
        </div>
      </div>

      {error && <div className={styles.error}>{error}</div>}

      {loading && <div className={styles.empty}>Loading tenant key publication state...</div>}

      {!loading && view && (
        <>
          <div className={styles.actionBar}>
            <button
              className={styles.button}
              disabled={mutating}
              type="button"
              onClick={() => void runMutation(() => backendService.seedTenantJwksKey(tenant))}
            >
              Seed key
            </button>
          </div>

          <form className={styles.keyForm} onSubmit={(event) => void submitKey(event)}>
            <label>
              <span className={styles.label}>kid</span>
              <input value={draft.kid} onChange={(event) => setDraft({ ...draft, kid: event.target.value })} />
            </label>
            <label>
              <span className={styles.label}>status</span>
              <select value={draft.status} onChange={(event) => setDraft({ ...draft, status: event.target.value })}>
                <option value="active">active</option>
                <option value="next">next</option>
                <option value="retired">retired</option>
              </select>
            </label>
            <label>
              <span className={styles.label}>alg</span>
              <input value={draft.alg} onChange={(event) => setDraft({ ...draft, alg: event.target.value })} />
            </label>
            <label>
              <span className={styles.label}>kty</span>
              <input value={draft.kty} onChange={(event) => setDraft({ ...draft, kty: event.target.value })} />
            </label>
            <label>
              <span className={styles.label}>crv</span>
              <input value={draft.crv} onChange={(event) => setDraft({ ...draft, crv: event.target.value })} />
            </label>
            <label>
              <span className={styles.label}>x / n</span>
              <input value={draft.x ?? draft.n ?? ''} onChange={(event) => setDraft({ ...draft, x: event.target.value, n: undefined })} />
            </label>
            <label className={styles.checkLabel}>
              <input checked={draft.publish !== false} type="checkbox" onChange={(event) => setDraft({ ...draft, publish: event.target.checked })} />
              <span>Publish</span>
            </label>
            <button className={styles.button} disabled={mutating} type="submit">Create key</button>
          </form>

          <div className={styles.metaGrid}>
            <div className={styles.metaCell}>
              <div className={styles.label}>Issuer</div>
              <div className={styles.value}>{view.issuer}</div>
            </div>
            <div className={styles.metaCell}>
              <div className={styles.label}>JWKS URI</div>
              <div className={styles.value}>{view.jwks_uri}</div>
            </div>
          </div>

          <div className={styles.countRow}>
            {lifecycles.map((lifecycle) => (
              <div className={styles.countCell} key={lifecycle}>
                <div className={styles.label}>{lifecycle}</div>
                <div className={styles.count}>{view.keys_by_lifecycle[lifecycle]?.length ?? 0}</div>
              </div>
            ))}
          </div>

          <div className={styles.metaCell}>
            <div className={styles.label}>Parity</div>
            <div className={styles.value}>{view.parity_indicator}</div>
          </div>

          {view.keys.length === 0 ? (
            <div className={styles.empty}>No publishable tenant JWKS keys are visible.</div>
          ) : (
            <div className={styles.tableWrap}>
              <table className={styles.table}>
                <thead>
                  <tr>
                    <th>kid</th>
                    <th>alg</th>
                    <th>kty</th>
                    <th>crv</th>
                    <th>use</th>
                    <th>lifecycle</th>
                    <th>public</th>
                    <th>actions</th>
                  </tr>
                </thead>
                <tbody>
                  {view.keys.map((key) => (
                    <tr key={`${key.lifecycle}-${key.kid}`}>
                      <td>{key.kid}</td>
                      <td>{key.alg}</td>
                      <td>{key.kty}</td>
                      <td>{key.crv ?? '-'}</td>
                      <td>{key.use}</td>
                      <td><span className={styles.pill}>{key.lifecycle}</span></td>
                      <td>{key.public ? 'yes' : 'no'}</td>
                      <td>
                        <div className={styles.rowActions}>
                          {key.lifecycle !== 'retired' && (
                            <button
                              className={styles.smallButton}
                              disabled={mutating}
                              type="button"
                              onClick={() => void runMutation(() => backendService.updateTenantJwksKey(tenant, { kid: key.kid, status: 'retired', publish: false }))}
                            >
                              Retire
                            </button>
                          )}
                          <button
                            className={styles.smallButton}
                            disabled={mutating}
                            type="button"
                            onClick={() => void runMutation(() => backendService.deleteTenantJwksKey(tenant, key.kid))}
                          >
                            Delete
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}

      {!loading && !view && !error && (
        <div className={styles.empty}>
          <Icons.Key />
          Tenant key publication state is unavailable.
        </div>
      )}
    </section>
  );
};

export default TenantJwksPublicationView;
