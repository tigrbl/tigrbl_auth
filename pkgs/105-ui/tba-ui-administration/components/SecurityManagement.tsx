
import React, { useState, useEffect } from 'react';
import { controlPlaneStateService } from '../services/controlPlaneStateService';
import { backendService } from '../services/backendService';
import { Alert } from '../types';
import { Icons } from '../constants';
import styles from './SecurityManagement.module.css';

const SecurityManagement: React.FC = () => {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [isLockdown, setIsLockdown] = useState(controlPlaneStateService.get_lockdown());

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

  const handleLockdownToggle = () => {
    const newVal = !isLockdown;
    controlPlaneStateService.set_lockdown(newVal);
    setIsLockdown(newVal);
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div>
          <h1 className={styles.title}>Security Analysis</h1>
          <p className={styles.subtitle}>Real-time threat vectors, pulse monitors, and platform isolation.</p>
        </div>
        <button
          onClick={handleLockdownToggle}
          className={`${styles.lockdownButton} ${isLockdown ? styles.lockdownActive : styles.lockdownInactive}`}
        >
          {isLockdown ? 'TERMINATE LOCKDOWN' : 'EMERGENCY LOCKDOWN'}
        </button>
      </div>

      <div className={styles.layoutGrid}>
        <div className={styles.mainColumn}>
           <div className={styles.feedCard}>
             <div className={styles.feedHeader}>
                <h3 className={styles.feedTitle}>Neural Threat Feed</h3>
                <span className={styles.feedStatus}>STREAMING: ACTIVE</span>
             </div>
             <div className={styles.feedList}>
               {alerts.map(alert => (
                 <div key={alert.id} className={styles.feedItem}>
                   <div className={styles.feedItemContent}>
                     <div className={`${styles.feedIcon} ${
                       alert.severity === 'high' ? styles.feedIconHigh :
                       alert.severity === 'medium' ? styles.feedIconMedium : styles.feedIconLow
                     }`}>
                       <Icons.Shield />
                     </div>
                     <div className={styles.feedBody}>
                       <div className={styles.feedMeta}>
                         <span className={styles.feedSeverity}>{alert.severity} SEVERITY_LINK</span>
                         <span className={styles.feedTimestamp}>{alert.timestamp}</span>
                       </div>
                       <p className={styles.feedMessage}>{alert.message}</p>
                       <div className={styles.feedActions}>
                         <button className={styles.feedAction}>INVESTIGATE</button>
                         <button className={`${styles.feedAction} ${styles.feedActionMuted}`}>LOG_DUMP</button>
                       </div>
                     </div>
                   </div>
                 </div>
               ))}
             </div>
           </div>
        </div>

        <div className={styles.sideColumn}>
           <div className={styles.riskCard}>
              <h3 className={styles.riskTitle}>Risk Assessment</h3>
              <div className={styles.riskScore}>
                <span className={styles.riskValue}>94</span>
                <span className={styles.riskUnit}>/ 100 Health</span>
              </div>
              <p className={styles.riskSummary}>
                Current platform surface is optimal. 3 dormant risks identified in secondary clusters.
              </p>
              <div className={styles.riskList}>
                 {[
                   { label: 'Mandatory MFA', active: true },
                   { label: 'IP Fencing', active: false },
                   { label: 'Entropy Scan', active: true },
                 ].map((item, i) => (
                   <div key={i} className={styles.riskRow}>
                     <span className={styles.riskLabel}>{item.label}</span>
                     <div className={`${styles.riskToggle} ${item.active ? styles.riskToggleActive : styles.riskToggleInactive}`}>
                        <div className={`${styles.riskDot} ${item.active ? styles.riskDotActive : styles.riskDotInactive}`}></div>
                     </div>
                   </div>
                 ))}
              </div>
           </div>

           <div className={styles.mitigationCard}>
              <div className={styles.mitigationIcon}>
                <Icons.Activity />
              </div>
              <h3 className={styles.mitigationTitle}>Active Mitigations</h3>
              <div className={styles.mitigationList}>
                 <div className={styles.mitigationItem}>
                    <p className={styles.mitigationName}>WAF_L7_GATE</p>
                    <p className={styles.mitigationMeta}>Status: Filtered (12.4k/s)</p>
                 </div>
                 <div className={styles.mitigationItem}>
                    <p className={styles.mitigationName}>BOT_REJECTION_01</p>
                    <p className={styles.mitigationMeta}>Status: Nominal (0.2% Block)</p>
                 </div>
              </div>
           </div>
        </div>
      </div>
    </div>
  );
};

export default SecurityManagement;
