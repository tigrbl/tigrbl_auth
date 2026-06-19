
import React, { useEffect, useState } from 'react';
import { Icons } from '../constants';
import { OAuthClient, PolicyGate, Tenant } from '../types';
import styles from './TenantDetail.module.css';
import { backendService } from '../services/backendService';

interface TenantDetailProps {
  tenant: Tenant;
  on_back: () => void;
}

const TenantDetail: React.FC<TenantDetailProps> = ({ tenant, on_back }) => {
  const [clients, set_clients] = useState<OAuthClient[]>([]);
  const [policies, set_policies] = useState<PolicyGate[]>([]);

  useEffect(() => {
    const load = async () => {
      const [client_list, policy_list] = await Promise.all([
        backendService.getClients(tenant.id),
        backendService.getPolicies(tenant.id),
      ]);
      set_clients(client_list);
      set_policies(policy_list);
    };

    void load();
  }, [tenant.id]);

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div className={styles.headerInfo}>
          <button onClick={on_back} className={styles.backButton}>
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
          </button>
          <div>
            <h1 className={styles.title}>{tenant.name}</h1>
            <p className={styles.subtitle}>Namespace Overview: {tenant.slug}</p>
          </div>
        </div>
        <div className={styles.headerActions}>
           <button className={styles.buttonBase}>Audit Trail</button>
           <button className={`${styles.buttonBase} ${styles.buttonPrimary}`}>Isolate Namespace</button>
        </div>
      </div>

      <div className={styles.layoutGrid}>
        <div className={styles.leftColumn}>
          <div className={styles.infoCard}>
            <h3 className={styles.infoTitle}>Identity Isolation</h3>
            <div className={styles.infoList}>
              <div>
                <p className={styles.infoLabel}>Tenant Unique ID</p>
                <p className={styles.infoValue}>{tenant.id}</p>
              </div>
              <div>
                <p className={styles.infoLabel}>Description</p>
                <p className={styles.infoValueItalic}>"{tenant.description || 'No tenant manifest provided.'}"</p>
              </div>
              <div className={styles.infoSection}>
                <p className={styles.infoLabel}>Provisioned Date</p>
                <p className={styles.infoValue}>{tenant.created_at || 'ARCHIVE_DATA'}</p>
              </div>
            </div>
          </div>

          <div className={styles.inventoryCard}>
             <h3 className={styles.inventoryTitle}>Asset Inventory</h3>
             <div className={styles.inventoryGrid}>
                <div className={styles.inventoryItem}>
                   <div>
                     <p className={styles.inventoryValue}>{policies.length}</p>
                     <p className={styles.inventoryLabel}>Policy Manifests</p>
                   </div>
                   <div className={styles.inventoryIcon}><Icons.Terminal /></div>
                </div>
                <div className={styles.inventoryItem}>
                   <div>
                     <p className={styles.inventoryValue}>{clients.length}</p>
                     <p className={styles.inventoryLabel}>OAuth Applications</p>
                   </div>
                   <div className={styles.inventoryIcon}><Icons.Globe /></div>
                </div>
             </div>
          </div>
        </div>

        <div className={styles.rightColumn}>
           <div className={styles.pulseCard}>
              <h3 className={styles.pulseTitle}>Namespace Security Pulse</h3>
              <div className={styles.pulseBody}>
                 <div className={styles.pulseIcon}><Icons.Activity /></div>
                 <p className={styles.pulseText}>Awaiting Live Telemetry Flux...</p>
                 <p className={styles.pulseMeta}>Cluster: us-east-neural-01</p>
              </div>
           </div>

           <div className={styles.statsGrid}>
              <div className={styles.statsCard}>
                 <h4 className={`${styles.statsTitle} ${styles.statsTitleRed}`}>Active Policies</h4>
                 <div className={styles.statsList}>
                    {policies.length > 0 ? policies.slice(0, 3).map(p => (
                      <div key={p.id} className={styles.statsRow}>
                        <span>{p.name}</span>
                        <span className={styles.statsMeta}>v{p.version}</span>
                      </div>
                    )) : <p className={styles.statsEmpty}>Zero manifests deployed.</p>}
                 </div>
              </div>
              <div className={styles.statsCard}>
                 <h4 className={`${styles.statsTitle} ${styles.statsTitleBlue}`}>Registered Clients</h4>
                 <div className={styles.statsList}>
                    {clients.length > 0 ? clients.slice(0, 3).map(c => (
                      <div key={c.id} className={styles.statsRow}>
                        <span>{c.name}</span>
                        <span className={styles.statsMeta}>{c.type}</span>
                      </div>
                    )) : <p className={styles.statsEmpty}>Zero clients registered.</p>}
                 </div>
              </div>
           </div>
        </div>
      </div>
    </div>
  );
};

export default TenantDetail;
