
import React, { useEffect, useState } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Icons } from '../constants';
import styles from './Dashboard.module.css';
import { Alert, TelemetryData } from '../types';
import { backendService } from '../services/backendService';

interface DashboardProps {
  tenant_id: string;
}

const Dashboard: React.FC<DashboardProps> = ({ tenant_id }) => {
  const [telemetry, set_telemetry] = useState<TelemetryData[]>([]);
  const [alerts, set_alerts] = useState<Alert[]>([]);

  const refresh = async () => {
    const [all_telemetry, all_alerts] = await Promise.all([
      backendService.getTelemetry(),
      backendService.getAlerts(),
    ]);
    set_telemetry(all_telemetry.filter((item) => item.timestamp).slice(-24));
    set_alerts(all_alerts.filter((alert) => alert.id).slice(0, 5));
  };

  useEffect(() => {
    void refresh();
  }, [tenant_id]);

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div>
          <h1 className={styles.title}>Neural Overview</h1>
          <p className={styles.subtitle}>Real-time gateway flux and cross-tenant traffic.</p>
        </div>
        <button className={styles.primaryButton} onClick={() => void refresh()}>Refresh Flux</button>
      </div>

      <div className={styles.statsGrid}>
        {[
          { label: 'Telemetry Samples', value: `${telemetry.length}`, delta: telemetry.length > 0 ? '+live' : '0', icon: Icons.Users },
          { label: 'Open Alerts', value: `${alerts.length}`, delta: alerts.length > 0 ? '+active' : '0', icon: Icons.Shield },
          { label: 'P99 Latency', value: telemetry.length > 0 ? `${Math.max(...telemetry.map((item) => item.latency))}ms` : 'n/a', delta: '-live', icon: Icons.Activity },
          { label: 'Total Errors', value: `${telemetry.reduce((acc, item) => acc + item.errors, 0)}`, delta: '+rolling', icon: Icons.Key },
        ].map((stat, i) => (
          <div key={i} className={styles.statCard}>
            <div className={styles.statHeader}>
               <span className={styles.statLabel}>{stat.label}</span>
               <div className={styles.statIcon}><stat.icon /></div>
            </div>
            <h3 className={styles.statValue}>{stat.value}</h3>
            <div className={styles.statDeltaRow}>
              <span className={stat.delta.startsWith('+') ? styles.statDeltaPositive : styles.statDeltaNegative}>{stat.delta}</span>
              <span className={styles.statDeltaBaseline}>BACKEND FEED</span>
            </div>
          </div>
        ))}
      </div>

      <div className={styles.chartGrid}>
        <div className={styles.chartCard}>
          <div className={styles.chartHeader}>
            <h3 className={styles.chartTitle}>Flux Volume / 24H</h3>
            <div className={styles.chartLegend}>
               <div className={styles.legendDot}></div>
               <span className={styles.legendText}>Requests</span>
            </div>
          </div>
          <div className={styles.chartBody}>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={telemetry}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#ebebe5" />
                <XAxis dataKey="timestamp" hide />
                <YAxis hide />
                <Tooltip />
                <Area type="monotone" dataKey="requests" stroke="#1a1a1a" strokeWidth={3} fillOpacity={0.05} fill="#1a1a1a" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className={styles.securityCard}>
          <h3 className={styles.securityTitle}>Security Pulse</h3>
          <div className={styles.securityList}>
            {alerts.map((alert) => (
              <div key={alert.id} className={styles.alertItem}>
                <div className={`${styles.alertBar} ${alert.severity === 'high' ? styles.alertBarHigh : styles.alertBarMedium}`}></div>
                <p className={styles.alertMessage}>{alert.message}</p>
                <p className={styles.alertTime}>T: {new Date(alert.timestamp).toLocaleTimeString()}</p>
              </div>
            ))}
          </div>
          <button className={styles.securityButton}>
            Open Security Vault
          </button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
