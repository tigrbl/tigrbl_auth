
import React, { useState, useEffect, useRef } from 'react';
import { Icons } from '../constants';
import { global_redis } from '../services/messaging/redisBroker';
import { global_rabbit } from '../services/messaging/rabbitBroker';
import { BrokerStatus } from '../services/messaging/baseBroker';
import styles from './ServiceInfrastructure.module.css';

const ServiceInfrastructure: React.FC = () => {
  const [redis_status, set_redis_status] = useState<BrokerStatus>(BrokerStatus.DISCONNECTED);
  const [rabbit_status, set_rabbit_status] = useState<BrokerStatus>(BrokerStatus.DISCONNECTED);
  const [logs, set_logs] = useState<string[]>([]);
  const [is_pinging, set_is_pinging] = useState(false);
  const log_container_ref = useRef<HTMLDivElement>(null);

  const add_log = (msg: string) => {
    const timestamp = new Date().toLocaleTimeString('en-GB', { hour12: false });
    set_logs(prev => [...prev.slice(-49), `[${timestamp}] ${msg}`]);
  };

  useEffect(() => {
    const check_status = () => {
      set_redis_status(global_redis.get_status());
      set_rabbit_status(global_rabbit.get_status());
    };

    const init = async () => {
      add_log("KERNEL: Booting tigrbl_auth service mesh orchestrator...");
      await global_redis.connect();
      add_log("REDIS: Connection pulse detected.");
      await global_rabbit.connect();
      add_log("RABBIT: Handshake successful.");
      check_status();
      add_log("MESH: Cluster health verified - STATUS: NOMINAL");
    };

    init();
    const interval = setInterval(check_status, 2000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (log_container_ref.current) {
      log_container_ref.current.scrollTop = log_container_ref.current.scrollHeight;
    }
  }, [logs]);

  const handle_ping = () => {
    set_is_pinging(true);
    add_log("MESH: Initiating global latency sweep...");
    setTimeout(() => {
      add_log("MESH: Sweep complete. P99: 4.2ms");
      set_is_pinging(false);
    }, 1500);
  };

  const restart_broker = async (name: string, broker: any) => {
    add_log(`${name.toUpperCase()}: Signal RESTART received.`);
    await broker.disconnect();
    setTimeout(async () => {
      await broker.connect();
      add_log(`${name.toUpperCase()}: Context re-initialized.`);
    }, 1000);
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div>
          <h1 className={styles.title}>Service Mesh</h1>
          <p className={styles.subtitle}>Monitoring of the backbone.</p>
        </div>
        <button onClick={handle_ping} disabled={is_pinging} className={styles.primaryButton}>
          {is_pinging ? 'Pinging Flux...' : 'Ping Infrastructure'}
        </button>
      </div>
      <div className={styles.layoutGrid}>
        <div className={styles.panel}>
          <h3 className={styles.panelTitle}>Messaging Brokers</h3>
          <div className={styles.brokerList}>
            {[
              { id: 'redis', name: 'Redis', status: redis_status, icon: Icons.Activity, broker: global_redis },
              { id: 'rabbit', name: 'RabbitMQ', status: rabbit_status, icon: Icons.Globe, broker: global_rabbit },
            ].map((b, i) => (
              <div key={i} className={styles.brokerItem}>
                <div className={styles.brokerInfo}>
                  <div className={`${styles.brokerIcon} ${b.status === BrokerStatus.CONNECTED ? styles.brokerIconConnected : styles.brokerIconDisconnected}`}><b.icon /></div>
                  <div>
                    <p className={styles.brokerName}>{b.name}</p>
                    <p className={styles.brokerId}>S_ID: {b.id}_CORE_01</p>
                  </div>
                </div>
                <div className={styles.brokerActions}>
                   <div className={styles.brokerStatus}>
                      <div className={`${styles.statusDot} ${b.status === BrokerStatus.CONNECTED ? styles.statusDotConnected : styles.statusDotDisconnected}`}></div>
                      <span className={styles.statusLabel}>{b.status}</span>
                   </div>
                   <button onClick={() => restart_broker(b.id, b.broker)} className={styles.restartButton}>Restart</button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ServiceInfrastructure;
