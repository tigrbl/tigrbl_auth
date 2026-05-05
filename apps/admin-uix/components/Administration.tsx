
import React from 'react';
import styles from './Administration.module.css';

interface AdministrationProps {
  tab: string;
}

const Administration: React.FC<AdministrationProps> = ({ tab }) => {
  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div>
          <h1 className={styles.title}>
            {tab.replace('_', ' ')}
          </h1>
          <p className={styles.subtitle}>Platform-wide control and compliance observability.</p>
        </div>
      </div>

      <div className={styles.layoutGrid}>
        <div className={styles.primaryColumn}>
          <div className={styles.card}>
            <h3 className={styles.cardTitle}>Global Variables</h3>
            <div className={styles.variableList}>
              {[
                { key: 'AEGIS_KEY_ROTATION_PERIOD', val: '90d', type: 'SECURE' },
                { key: 'FLUX_CONCURRENCY_CAP', val: '50000', type: 'INFRA' },
                { key: 'AUDIT_RETENTION_DAYS', val: '365', type: 'POLICY' },
              ].map((v, i) => (
                <div key={i} className={styles.variableItem}>
                  <div>
                    <p className={styles.variableType}>{v.type}</p>
                    <p className={styles.variableKey}>{v.key}</p>
                  </div>
                  <div className={styles.variableActions}>
                    <span className={styles.variableValue}>{v.val}</span>
                    <button className={styles.variableButton}>Modify</button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className={styles.secondaryColumn}>
          <div className={styles.performanceCard}>
            <h3 className={styles.performanceTitle}>System Performance</h3>
            <div className={styles.performanceScore}>
              <span className={styles.performanceValue}>99.98</span>
              <span className={styles.performanceUnit}>% Uptime</span>
            </div>
            <div className={styles.performanceList}>
               <div className={styles.performanceRow}>
                  <span>Logic Clusters</span>
                  <span className={styles.performanceHighlight}>Healthy</span>
               </div>
               <div className={styles.performanceRow}>
                  <span>Broker Latency</span>
                  <span>1.2ms</span>
               </div>
               <div className={styles.performanceRow}>
                  <span>Storage Utilization</span>
                  <span>42%</span>
               </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Administration;
