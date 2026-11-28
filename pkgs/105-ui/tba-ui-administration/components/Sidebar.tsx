
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
      { section: 'Admin Workspace', items: [
      { id: 'dashboard', label: 'Dashboard', icon: Icons.Dashboard },
      { id: 'tenants', label: 'Tenants', icon: Icons.Settings },
      { id: 'identities', label: 'Identities', icon: Icons.Users },
      { id: 'tenant-jwks', label: 'Signing Keys', icon: Icons.Key },
    ]}
  ];

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

      <div className={styles.footer}>
        <div className={styles.profileCard}>
           <div className={`${styles.profileBadge} ${is_admin ? styles.profileBadgeAdmin : styles.profileBadgeDefault}`}>
             {is_admin ? 'SU' : 'AD'}
           </div>
           <div className={styles.profileDetails}>
              <p className={styles.profileName}>{is_admin ? 'Superuser Session' : 'Admin Session'}</p>
              <p className={styles.profileMeta}>{is_admin ? 'Platform administration' : 'Tenant administration'}</p>
           </div>
        </div>
      </div>
    </nav>
  );
};

export default Sidebar;
