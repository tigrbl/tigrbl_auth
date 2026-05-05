
import React, { useState } from 'react';
import { controlPlaneStateService } from '../services/controlPlaneStateService';
import { Icons } from '../constants';
import styles from './AbuseManagement.module.css';

const AbuseManagement: React.FC = () => {
  const [rules, setRules] = useState(controlPlaneStateService.get_abuse_rules());
  const [profiles, setProfiles] = useState(controlPlaneStateService.get_traffic_profiles());

  const handleToggleRule = (id: string) => {
    controlPlaneStateService.toggle_abuse_rule(id);
    setRules(controlPlaneStateService.get_abuse_rules());
  };

  const updateProfile = (id: string, field: string, val: number) => {
    const prof = profiles.find(p => p.id === id);
    if (prof) {
      const updated = { ...prof, [field]: val };
      controlPlaneStateService.update_traffic_profile(updated);
      setProfiles(controlPlaneStateService.get_traffic_profiles());
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div>
          <h1 className={styles.title}>Abuse Mitigation</h1>
          <p className={styles.subtitle}>Heuristic traffic shaping and real-time anomaly rejection across the mesh.</p>
        </div>
        <button className={styles.primaryButton}>Force Flush Cache</button>
      </div>

      <div className={styles.layoutGrid}>
        <div className={styles.profilesPanel}>
          <div className={styles.panelHeader}>
             <h3 className={styles.panelTitle}>Traffic Control Profiles</h3>
             <span className={styles.panelStatus}>ENFORCEMENT: ACTIVE</span>
          </div>
          <div className={styles.profileList}>
            {profiles.map((limit) => {
              const usagePercent = Math.min((limit.current / limit.limit) * 100, 100);
              return (
                <div key={limit.id} className={styles.profileGroup}>
                  <div className={styles.profileHeader}>
                    <div className={styles.profileInfo}>
                      <div className={styles.profileSwatch} style={{ backgroundColor: limit.color }}></div>
                      <div>
                        <p className={styles.profileLabel}>{limit.label}</p>
                        <p className={styles.profileId}>ID: {limit.id}</p>
                      </div>
                    </div>
                    <div className={styles.profileStats}>
                       <p className={styles.profileValue}>{limit.current.toLocaleString()}</p>
                       <p className={styles.profileValueLabel}>Current Ops/Sec</p>
                    </div>
                  </div>

                  <div className={styles.profileCard}>
                    <div className={styles.progressTrack}>
                      <div
                        className={styles.progressBar}
                        style={{
                          width: `${usagePercent}%`,
                          backgroundColor: limit.color,
                          boxShadow: usagePercent > 90 ? '0 0 10px rgba(255,45,0,0.5)' : 'none'
                        }}
                      ></div>
                    </div>

                    <div className={styles.sliderGrid}>
                      <div className={styles.sliderBlock}>
                        <div className={styles.sliderHeader}>
                           <label className={styles.sliderLabel}>Soft Limit</label>
                           <span className={styles.sliderValue}>{limit.limit.toLocaleString()}</span>
                        </div>
                        <input
                          type="range"
                          min="100"
                          max="20000"
                          step="100"
                          value={limit.limit}
                          onChange={(e) => updateProfile(limit.id, 'limit', parseInt(e.target.value))}
                          className={styles.sliderInput}
                        />
                      </div>
                      <div className={styles.sliderBlock}>
                        <div className={styles.sliderHeader}>
                           <label className={styles.sliderLabel}>Burst Threshold</label>
                           <span className={styles.sliderValue}>{limit.burst.toLocaleString()}</span>
                        </div>
                        <input
                          type="range"
                          min="500"
                          max="50000"
                          step="500"
                          value={limit.burst}
                          onChange={(e) => updateProfile(limit.id, 'burst', parseInt(e.target.value))}
                          className={styles.sliderInput}
                        />
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <div className={styles.rulesPanel}>
          <div className={styles.rulesCard}>
            <h3 className={styles.rulesTitle}>Heuristic Guard Rules</h3>
            <div className={styles.rulesList}>
              {rules.map((rule) => (
                <div
                  key={rule.id}
                  onClick={() => handleToggleRule(rule.id)}
                  className={`${styles.ruleItem} ${rule.active ? styles.ruleItemActive : styles.ruleItemInactive}`}
                >
                  <div className={styles.ruleBody}>
                    <p className={`${styles.ruleTitle} ${rule.active ? styles.ruleTitleActive : styles.ruleTitleInactive}`}>{rule.title}</p>
                    <p className={styles.ruleDesc}>{rule.desc}</p>
                  </div>
                  <div className={`${styles.ruleToggle} ${rule.active ? styles.ruleToggleActive : styles.ruleToggleInactive}`}>
                    <div className={`${styles.ruleToggleDot} ${rule.active ? styles.ruleToggleDotActive : styles.ruleToggleDotInactive}`}></div>
                  </div>
                </div>
              ))}
            </div>
            <div className={styles.engineCard}>
               <p className={styles.engineTitle}>Neural Anomaly Detection Engine</p>
               <div className={styles.engineStatus}>
                  <div className={styles.enginePing}></div>
                  <span className={styles.engineText}>Synchronized with Edge-01</span>
               </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AbuseManagement;
