import React from 'react';
import { ShieldCheck, ShieldAlert, Cpu, Terminal, Disc } from 'lucide-react';

export interface KeystoreOption {
  id: string;
  name: string;
  isSoftwareSecured: boolean;
  evidenceModel: string;
  description: string;
  latencyExpectation: string;
}

export const KEYSTORE_OPTIONS: KeystoreOption[] = [
  {
    id: 'macos_keychain',
    name: 'macOS Keychain (CryptoKit)',
    isSoftwareSecured: true,
    evidenceModel: 'OS Keystore Metadata Statement (v2)',
    description: 'Hardware-guarded process boundary via Apple CryptoKit frameworks. Rejects raw private key exports.',
    latencyExpectation: '10 - 15ms'
  },
  {
    id: 'windows_cng',
    name: 'Windows CNG (NCrypt)',
    isSoftwareSecured: true,
    evidenceModel: 'Windows NCrypt Isolation Attestation',
    description: 'Microsoft Cryptography Next Generation isolation. Runs key operations inside Local Security Authority (LSA) isolated host.',
    latencyExpectation: '15 - 25ms'
  },
  {
    id: 'linux_systemd',
    name: 'Linux Secret Service (systemd-creds)',
    isSoftwareSecured: true,
    evidenceModel: 'Kernel LUKS Keyring Attestation',
    description: 'Binds credentials directly to systemd-creds with kernel-level encryption key rings and file integrity blocks.',
    latencyExpectation: '5 - 10ms'
  },
  {
    id: 'openssl_cli',
    name: 'CLI Secure Keyring (OpenSSL Engine)',
    isSoftwareSecured: true,
    evidenceModel: 'JWKS Upload Verification Attestation',
    description: 'Developer CLI sandbox using OpenSSL engine wrappers. Permits key portability but logs extraction warnings.',
    latencyExpectation: '2 - 5ms'
  },
  {
    id: 'unverified_browser',
    name: 'Browser Session Keyring (IndexedDB)',
    isSoftwareSecured: false,
    evidenceModel: 'None (Self-Asserted browser container)',
    description: 'Legacy web-app session keyring. Stored locally inside IndexedDB state. No tamper or extraction resistance.',
    latencyExpectation: '1 - 2ms'
  }
];

interface KeyStorePickerProps {
  selectedId: string;
  onChange: (id: string) => void;
}

export default function KeyStorePicker({
  selectedId,
  onChange
}: KeyStorePickerProps) {
  return (
    <div id="keystore-picker" className="space-y-4">
      <div className="space-y-1">
        <label className="text-xs font-bold text-slate-500 uppercase tracking-wider block">Select Isolation Keystore Provider</label>
        <p className="text-xs text-slate-500 leading-relaxed">
          The selected provider governs how private keys are isolated and what evidence statements are returned for server-side AMR validation.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {KEYSTORE_OPTIONS.map((option) => {
          const isSelected = option.id === selectedId;
          const isSecured = option.isSoftwareSecured;

          return (
            <button
              key={option.id}
              id={`btn-keystore-opt-${option.id}`}
              type="button"
              onClick={() => onChange(option.id)}
              className={`p-4 rounded-xl border text-left transition-all ${
                isSelected
                  ? 'bg-indigo-50/80 border-indigo-500 ring-2 ring-indigo-500/10'
                  : 'bg-white border-slate-200 hover:border-slate-300 hover:bg-slate-50'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="font-bold text-sm text-slate-800 flex items-center gap-1.5">
                  {option.id === 'openssl_cli' ? (
                    <Terminal className="w-4 h-4 text-slate-500 shrink-0" />
                  ) : option.id === 'unverified_browser' ? (
                    <Disc className="w-4 h-4 text-amber-500 shrink-0" />
                  ) : (
                    <Cpu className="w-4 h-4 text-indigo-500 shrink-0" />
                  )}
                  {option.name}
                </span>

                {isSecured ? (
                  <span className="inline-flex items-center gap-0.5 bg-emerald-50 text-emerald-700 px-1.5 py-0.5 rounded text-[9px] font-extrabold uppercase border border-emerald-100">
                    <ShieldCheck className="w-3 h-3" /> Securable
                  </span>
                ) : (
                  <span className="inline-flex items-center gap-0.5 bg-amber-50 text-amber-700 px-1.5 py-0.5 rounded text-[9px] font-extrabold uppercase border border-amber-100">
                    <ShieldAlert className="w-3 h-3" /> Unverified
                  </span>
                )}
              </div>

              <p className="text-xs text-slate-500 mt-2 leading-relaxed">{option.description}</p>

              <div className="text-[10px] text-slate-400 font-mono mt-3 flex items-center justify-between pt-2 border-t border-slate-100 font-semibold">
                <span>Evidence: <span className="text-slate-600">{option.evidenceModel}</span></span>
                <span>Latency ~ {option.latencyExpectation}</span>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
