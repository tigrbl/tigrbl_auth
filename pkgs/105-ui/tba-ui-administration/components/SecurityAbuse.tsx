
import React, { useEffect, useState } from 'react';
import { Icons } from '../constants';
import { backendService } from '../services/backendService';
import { Alert } from '../types';
import styles from './SecurityAbuse.module.css';

const SecurityAbuse: React.FC = () => {
  const [alerts, setAlerts] = useState<Alert[]>([]);

  useEffect(() => {
    const loadAlerts = async () => {
      try {
        const result = await backendService.getAlerts();
        setAlerts(result);
      } catch (error) {
        console.error('Failed to load alerts', error);
        setAlerts([]);
      }
    };

    void loadAlerts();
  }, []);

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div>
          <h2 className={styles.title}>Abuse Guard & Security</h2>
          <p className={styles.subtitle}>Automated mitigation and incident response</p>
        </div>
        <div className={styles.headerActions}>
           <button className={styles.lockdownButton}>EMERGENCY LOCKDOWN</button>
        </div>
      </div>

      <div className={styles.layoutGrid}>
        <div className={styles.card}>
          <h3 className={styles.cardTitle}>Recent Security Events</h3>
          <div className={styles.eventList}>
            {alerts.map(alert => (
              <div key={alert.id} className={styles.eventItem}>
                <div className={`${styles.eventIcon} ${
                  alert.severity === 'high' ? styles.eventIconHigh :
                  alert.severity === 'medium' ? styles.eventIconMedium : styles.eventIconLow
                }`}>
                  <Icons.Shield />
                </div>
                <div className={styles.eventBody}>
                  <div className={styles.eventMeta}>
                    <span className={styles.eventSeverity}>{alert.severity} Risk</span>
                    <span className={styles.eventTime}>2 mins ago</span>
                  </div>
                  <p className={styles.eventMessage}>{alert.message}</p>
                  <div className={styles.eventActions}>
                    <button className={styles.eventAction}>Investigate</button>
                    <button className={`${styles.eventAction} ${styles.eventDismiss}`}>Dismiss</button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className={styles.sideColumn}>
          <div className={styles.card}>
            <h3 className={styles.rateCardTitle}>Rate Limit Config</h3>
            <div className={styles.rateList}>
              {[
                { label: 'Global API Rate', current: '5000 req/min', limit: '10000' },
                { label: 'Auth Attempts', current: '12 / min / ip', limit: '20' },
                { label: 'Token Exchange', current: '150 / sec', limit: '500' },
              ].map((item, i) => (
                <div key={i} className={styles.rateItem}>
                  <div>
                    <p className={styles.rateLabel}>{item.label}</p>
                    <p className={styles.rateValue}>{item.current}</p>
                  </div>
                  <div className={styles.rateMeta}>
                    <p className={styles.rateLimit}>Limit: {item.limit}</p>
                    <button className={styles.rateAdjust}>Adjust</button>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className={styles.card}>
            <h3 className={styles.rulesCardTitle}>Abuse Guard Rules</h3>
            <div className={styles.ruleList}>
              <label className={styles.ruleItem}>
                <span className={styles.ruleLabel}>Auto-block Credential Stuffing</span>
                <input type="checkbox" defaultChecked className={styles.ruleCheckbox} />
              </label>
              <label className={styles.ruleItem}>
                <span className={styles.ruleLabel}>Anomalous Geo-login Detection</span>
                <input type="checkbox" defaultChecked className={styles.ruleCheckbox} />
              </label>
              <label className={styles.ruleItem}>
                <span className={styles.ruleLabel}>Block Known Proxy/VPN Exit Nodes</span>
                <input type="checkbox" className={styles.ruleCheckbox} />
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SecurityAbuse;
