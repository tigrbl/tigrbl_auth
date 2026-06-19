export const STORAGE_PREFIX = 'tigrbl_auth_admin_uix';

export const storageKeyFor = (suffix: string) => `${STORAGE_PREFIX}:${suffix}`;

type StoreConfig = {
  keyPath: string;
};

const DB_NAME = 'tigrbl_auth_admin_uix_db';
const DB_VERSION = 1;

const STORE_CONFIG: Record<string, StoreConfig> = {
  tenants: { keyPath: 'id' },
  identities: { keyPath: 'id' },
  users: { keyPath: 'id' },
  clients: { keyPath: 'id' },
  policies: { keyPath: 'id' },
  abuse_rules: { keyPath: 'id' },
  traffic_profiles: { keyPath: 'id' },
  policy_control_plane: { keyPath: 'id' },
  policy_sync: { keyPath: 'id' },
  system: { keyPath: 'key' },
};

let dbPromise: Promise<IDBDatabase> | null = null;

const canUseIndexedDb = () => typeof indexedDB !== 'undefined';

const openDatabase = () => {
  if (!canUseIndexedDb()) {
    return null;
  }

  if (!dbPromise) {
    dbPromise = new Promise((resolve, reject) => {
      const request = indexedDB.open(DB_NAME, DB_VERSION);

      request.onupgradeneeded = () => {
        const db = request.result;
        Object.entries(STORE_CONFIG).forEach(([storeName, config]) => {
          if (!db.objectStoreNames.contains(storeName)) {
            db.createObjectStore(storeName, { keyPath: config.keyPath });
          }
        });
      };

      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  return dbPromise;
};

const withStore = async <T>(
  storeName: keyof typeof STORE_CONFIG,
  mode: IDBTransactionMode,
  callback: (store: IDBObjectStore) => void,
): Promise<T | null> => {
  const dbPromiseLocal = openDatabase();
  if (!dbPromiseLocal) {
    return null;
  }

  const db = await dbPromiseLocal;

  return new Promise((resolve, reject) => {
    const transaction = db.transaction(storeName, mode);
    const store = transaction.objectStore(storeName);

    callback(store);

    transaction.oncomplete = () => resolve(null);
    transaction.onerror = () => reject(transaction.error);
    transaction.onabort = () => reject(transaction.error);
  });
};

export const persistCollection = async <T extends { id: string }>(
  storeName: keyof typeof STORE_CONFIG,
  records: T[],
): Promise<void> => {
  await withStore(storeName, 'readwrite', (store) => {
    store.clear();
    records.forEach((record) => store.put(record));
  });
};

export const persistRecord = async <T>(
  storeName: keyof typeof STORE_CONFIG,
  record: T,
): Promise<void> => {
  await withStore(storeName, 'readwrite', (store) => {
    store.put(record);
  });
};

export const readLocal = <T>(key: string, fallback: T): T => {
  if (typeof localStorage === 'undefined') {
    return fallback;
  }

  const raw = localStorage.getItem(key);
  if (!raw) {
    localStorage.setItem(key, JSON.stringify(fallback));
    return fallback;
  }

  try {
    return JSON.parse(raw) as T;
  } catch (error) {
    console.warn(`[storage] Failed to parse ${key}, resetting.`, error);
    localStorage.setItem(key, JSON.stringify(fallback));
    return fallback;
  }
};

export const writeLocal = <T>(key: string, value: T): void => {
  if (typeof localStorage === 'undefined') {
    return;
  }

  localStorage.setItem(key, JSON.stringify(value));
};
