
import React from 'react';
import { Icons } from '../constants';
import styles from './Sidebar.module.css';

interface SidebarProps {
  active_tab: string;
  set_active_tab: (tab: string) => void;
  is_admin: boolean;
}

const Sidebar: React.FC<SidebarProps> = ({ active_tab, set_active_tab, is_admin }) => {
  const menu_items = [
    { section: 'Core Logic', items: [
      { id: 'dashboard', label: 'Dashboard', icon: Icons.Dashboard },
      { id: 'tenants', label: 'Tenants Control', icon: Icons.Settings },
      { id: 'identities', label: 'Identity Pool', icon: Icons.Users },
    ]},
    { section: 'Infrastructure', items: [
      { id: 'services', label: 'Service Mesh', icon: Icons.Activity },
      { id: 'clients', label: 'OAuth Clients', icon: Icons.Globe },
      { id: 'policies', label: 'Policy Gates', icon: Icons.Terminal },
    ]},
    { section: 'Operations', items: [
      { id: 'security', label: 'Security Analysis', icon: Icons.Key },
      { id: 'abuse', label: 'Abuse Mitigation', icon: Icons.Activity },
    ]}
  ];

  const admin_items = {
    section: 'Administration',
    items: [
      { id: 'platform_settings', label: 'System Config', icon: Icons.Settings },
      { id: 'audit_logs', label: 'Global Audit', icon: Icons.Terminal },
      { id: 'tenancy_stats', label: 'Tenancy Metrics', icon: Icons.Dashboard },
    ]
  };

  return (
    <nav className={styles.nav}>
      {menu_items.map((group, idx) => (
        <div key={idx} className={styles.section}>
          <div className={styles.sectionTitle}>{group.section}</div>
          <div className={styles.sectionList}>
            {group.items.map((item) => {
              const Icon = item.icon;
              const is_active = active_tab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => set_active_tab(item.id)}
                  className={`${styles.menuButton} ${is_active ? styles.menuButtonActiveAdmin : styles.menuButtonInactive}`}
                >
                  <Icon />
                  <span className={styles.menuLabel}>
                    {item.label}
                  </span>
                </button>
              );
            })}
          </div>
        </div>
      ))}

      {is_admin && (
        <div className={styles.section}>
          <div className={styles.adminSectionTitle}>{admin_items.section}</div>
          <div className={styles.sectionList}>
            {admin_items.items.map((item) => {
              const Icon = item.icon;
              const is_active = active_tab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => set_active_tab(item.id)}
                  className={`${styles.menuButton} ${is_active ? styles.menuButtonActive : styles.menuButtonInactive}`}
                >
                  <Icon />
                  <span className={styles.menuLabel}>
                    {item.label}
                  </span>
                </button>
              );
            })}
          </div>
        </div>
      )}

      <div className={styles.footer}>
        <div className={styles.profileCard}>
           <div className={`${styles.profileBadge} ${is_admin ? styles.profileBadgeAdmin : styles.profileBadgeDefault}`}>
             {is_admin ? 'SU' : 'AD'}
           </div>
           <div className={styles.profileDetails}>
              <p className={styles.profileName}>{is_admin ? 'SUPERADMIN.ROOT' : 'ADMIN.ROOT'}</p>
              <p className={styles.profileMeta}>{is_admin ? 'tigrbl_auth Platform' : 'Namespace Access'}</p>
           </div>
        </div>
      </div>
    </nav>
  );
};

export default Sidebar;
