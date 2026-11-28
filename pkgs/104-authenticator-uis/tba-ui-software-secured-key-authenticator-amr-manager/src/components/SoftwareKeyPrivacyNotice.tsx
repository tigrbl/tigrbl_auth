import React from 'react';
import { ShieldAlert, RefreshCw, Key, Info, HelpCircle } from 'lucide-react';

interface SoftwareKeyPrivacyNoticeProps {
  backupPolicy: 'allow' | 'block' | 'strict_evidence';
  exportPolicy: 'allow' | 'block';
}

export default function SoftwareKeyPrivacyNotice({
  backupPolicy,
  exportPolicy
}: SoftwareKeyPrivacyNoticeProps) {
  return (
    <div id="software-key-privacy-notice" className="bg-slate-50 border border-slate-200 rounded-xl p-4.5 space-y-4">
      <div className="flex gap-3">
        <div className="p-2 bg-amber-500/15 text-amber-600 rounded-lg shrink-0 h-9 w-9 flex items-center justify-center">
          <ShieldAlert className="w-5 h-5" />
        </div>
        <div className="space-y-1">
          <h5 className="font-bold text-slate-800 text-sm">Software Isolation vs. Hardware Isolation</h5>
          <p className="text-xs text-slate-500 leading-relaxed">
            Software-secured credentials (<code className="bg-slate-100 px-1 py-0.5 rounded text-indigo-600 font-mono text-[10.5px]">swk</code>) reside inside isolated OS process boundaries (like macOS Keychain CryptoKit or Windows CNG NCrypt). While they prevent general memory scraping, they lack the hardware-enforced physical extraction blocks of Secure Enclaves (<code className="bg-slate-100 px-1 py-0.5 rounded text-emerald-600 font-mono text-[10.5px]">hwk</code>).
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5 pt-1.5">
        <div className="bg-white border border-slate-200/80 rounded-lg p-3 text-xs space-y-1.5">
          <div className="flex items-center gap-1.5 font-bold text-slate-700">
            <RefreshCw className="w-3.5 h-3.5 text-slate-500" />
            <span>Active Backup Policy Constraints</span>
          </div>
          <p className="text-slate-500 text-[11px] leading-normal">
            {backupPolicy === 'block' && 'Keystore export/backup is BLOCKED. If you clear this platform cache or format the drive, these specific key keys will be permanently lost and require full re-enrollment.'}
            {backupPolicy === 'allow' && 'Keystore backup is PERMITTED. Keys can be exported inside platform-specific recovery bundles.'}
            {backupPolicy === 'strict_evidence' && 'Keystore backup is STRICTLY CONDITIONED on verified attestation proofs submitted to the server gateway.'}
          </p>
        </div>

        <div className="bg-white border border-slate-200/80 rounded-lg p-3 text-xs space-y-1.5">
          <div className="flex items-center gap-1.5 font-bold text-slate-700">
            <Key className="w-3.5 h-3.5 text-slate-500" />
            <span>Extraction & Exportability Posture</span>
          </div>
          <p className="text-slate-500 text-[11px] leading-normal">
            {exportPolicy === 'block'
              ? 'Private key material is marked non-exportable at creation. Local APIs will sign assertions but refuse to release raw binary PKCS#8 or SEC1 private components.'
              : 'Extraction is permitted for specific cli/developer tools. Use extreme caution to avoid committing key files to source control.'}
          </p>
        </div>
      </div>

      <div className="text-[10px] text-slate-400 bg-slate-100/60 p-2.5 rounded-lg flex items-center gap-1.5 font-medium border border-slate-200/40">
        <Info className="w-3.5 h-3.5 text-slate-400 shrink-0" />
        <span>Assurance Model Enforces: Verified Software attestations will map to an Authenticator Method Reference (AMR) of "swk".</span>
      </div>
    </div>
  );
}
