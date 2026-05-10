import React, { useEffect, useState } from 'react';
import { Icons } from '../constants';
import { backendService } from '../services/backendService';
import type { Tenant, TenantJwksPublicationView as TenantJwksPublication } from '../types';
import styles from './TenantJwksPublicationView.module.css';

type TenantJwksPublicationViewProps = {
  tenant: Tenant;
};

const lifecycles = ['active', 'next', 'retired'];

const TenantJwksPublicationView: React.FC<TenantJwksPublicationViewProps> = ({ tenant }) => {
  const [view, setView] = useState<TenantJwksPublication | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

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
