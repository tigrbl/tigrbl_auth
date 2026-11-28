import { UserStatus, type Alert } from '../types';
import { readLocal, storageKeyFor, writeLocal } from './persistence';

export type Identity = {
  id: string;
  email: string;
  full_name: string;
  provider: 'google' | 'github' | 'local';
  mfa_enabled: boolean;
  created_at: string;
  roles: string[];
  status: UserStatus;
};

export type AbuseRule = {
  id: string;
  title: string;
  desc: string;
  active: boolean;
};

export type TrafficProfile = {
  id: string;
  label: string;
  current: number;
  limit: number;
  burst: number;
  color: string;
};

type SystemState = {
  lockdown: boolean;
};

const STORAGE_KEYS = {
  identities: storageKeyFor('identities'),
  abuse_rules: storageKeyFor('abuse-rules'),
  traffic_profiles: storageKeyFor('traffic-profiles'),
  system: storageKeyFor('system'),
};

let identities = readLocal<Identity[]>(STORAGE_KEYS.identities, []);
let abuse_rules = readLocal<AbuseRule[]>(STORAGE_KEYS.abuse_rules, []);
let traffic_profiles = readLocal<TrafficProfile[]>(STORAGE_KEYS.traffic_profiles, []);
let system_state = readLocal<SystemState>(STORAGE_KEYS.system, { lockdown: false });

const saveCollection = <T>(key: string, value: T) => {
  writeLocal(key, value);
};

export const controlPlaneStateService = {
  get_lockdown: () => system_state.lockdown,
  set_lockdown: (val: boolean) => {
    system_state = { ...system_state, lockdown: val };
    saveCollection(STORAGE_KEYS.system, system_state);
  },

  get_identities: () => [...identities],
  add_identity: (identity: Identity) => {
    identities = [...identities, identity];
    saveCollection(STORAGE_KEYS.identities, identities);
  },
  update_identity: (identity: Identity) => {
    identities = identities.map((item) => (item.id === identity.id ? identity : item));
    saveCollection(STORAGE_KEYS.identities, identities);
  },
  delete_identity: (id: string) => {
    identities = identities.filter((identity) => identity.id !== id);
    saveCollection(STORAGE_KEYS.identities, identities);
  },

  get_abuse_rules: () => [...abuse_rules],
  toggle_abuse_rule: (id: string) => {
    abuse_rules = abuse_rules.map((rule) => (rule.id === id ? { ...rule, active: !rule.active } : rule));
    saveCollection(STORAGE_KEYS.abuse_rules, abuse_rules);
  },

  get_traffic_profiles: () => [...traffic_profiles],
  update_traffic_profile: (profile: TrafficProfile) => {
    traffic_profiles = traffic_profiles.map((item) => (item.id === profile.id ? profile : item));
    saveCollection(STORAGE_KEYS.traffic_profiles, traffic_profiles);
  },

  normalize_alerts: (alerts: Alert[]): Alert[] => [...alerts],
};
