import React from 'react';
import { KeyOriginPolicy, SoftwareKeyCredential } from '../types';
import { ShieldCheck, ShieldAlert, CheckCircle, AlertTriangle, Cpu } from 'lucide-react';

interface PolicyImpactPreviewProps {
  policy: KeyOriginPolicy;
  activeCredentials: SoftwareKeyCredential[];
}

export default function PolicyImpactPreview({
  policy,
  activeCredentials
}: PolicyImpactPreviewProps) {
  // Check compliance for each key
  const evaluatedKeys = activeCredentials.map((key) => {
    // Determine store slug
    let storeSlug = 'unverified_browser';
    const providerLower = key.keyStoreProvider.toLowerCase();
    if (providerLower.includes('macos')) {
      storeSlug = 'macos_keychain';
    } else if (providerLower.includes('windows')) {
      storeSlug = 'windows_cng';
    } else if (providerLower.includes('linux')) {
      storeSlug = 'linux_systemd';
    } else if (providerLower.includes('cli') || providerLower.includes('openssl')) {
      storeSlug = 'openssl_cli';
    }

    const storeAllowed = policy.allowedStores.includes(storeSlug);
    const algAllowed = policy.allowedAlgorithms.includes(key.algorithm);
    
    // Backup checks
    let backupAllowed = true;
    if (policy.backupPolicy === 'block' && key.backupPosture === 'permitted') {
      backupAllowed = false;
    } else if (policy.backupPolicy === 'strict_evidence' && !key.hasVerifiedEvidence) {
      backupAllowed = false;
    }

    // Export checks
    let exportAllowed = true;
    if (policy.exportPolicy === 'block' && key.exportPosture === 'permitted') {
      exportAllowed = false;
    }

    const compliant = storeAllowed && algAllowed && backupAllowed && exportAllowed;

    return {
      key,
      storeAllowed,
      algAllowed,
      backupAllowed,
      exportAllowed,
      compliant
    };
  });

  const compliantCount = evaluatedKeys.filter((k) => k.compliant).length;
  const nonCompliantCount = evaluatedKeys.length - compliantCount;

  return (
    <div id="policy-impact-preview" className="space-y-4">
      <span className="text-xs font-semibold text-slate-300 block">Real-Time Impact Simulation</span>

      <div className="bg-slate-900/40 border border-slate-800 rounded-xl p-4 space-y-4">
        <div className="flex items-center justify-between">
          <div className="text-xs text-slate-400 font-medium">Compliance Coverage</div>
          <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase font-mono ${
            nonCompliantCount > 0 ? 'bg-amber-950 text-amber-400 border border-amber-900/40' : 'bg-emerald-950 text-emerald-400 border border-emerald-900/40'
          }`}>
            {compliantCount} / {evaluatedKeys.length} COMPLIANT
          </span>
        </div>

        <div className="h-2 w-full bg-slate-950 rounded-full overflow-hidden flex">
          <div
            className="bg-emerald-500 h-full transition-all duration-300"
            style={{ width: `${(compliantCount / (evaluatedKeys.length || 1)) * 100}%` }}
          />
          <div
            className="bg-amber-500 h-full transition-all duration-300"
            style={{ width: `${(nonCompliantCount / (evaluatedKeys.length || 1)) * 100}%` }}
          />
        </div>

        <div className="space-y-2.5 max-h-[180px] overflow-y-auto pr-1">
          {evaluatedKeys.map(({ key, storeAllowed, algAllowed, backupAllowed, exportAllowed, compliant }) => (
            <div key={key.id} className="p-2.5 bg-slate-950/40 rounded-lg border border-slate-850 flex items-center justify-between text-xs">
              <div className="space-y-0.5 max-w-[70%]">
                <span className="font-bold text-slate-200 block truncate">{key.name}</span>
                <span className="text-[10px] text-slate-500 block truncate font-mono">id: {key.id}</span>
              </div>

              <div className="flex items-center gap-2">
                {compliant ? (
                  <span className="inline-flex items-center gap-1 bg-emerald-950 text-emerald-400 px-1.5 py-0.5 rounded text-[9px] font-extrabold uppercase border border-emerald-900/50">
                    <CheckCircle className="w-2.5 h-2.5" /> compliant
                  </span>
                ) : (
                  <span className="inline-flex items-center gap-1 bg-amber-950 text-amber-400 px-1.5 py-0.5 rounded text-[9px] font-extrabold uppercase border border-amber-900/50">
                    <AlertTriangle className="w-2.5 h-2.5" /> violating
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>

        {nonCompliantCount > 0 && (
          <div className="bg-amber-950/20 border border-amber-900/30 rounded-lg p-3 text-[11px] leading-relaxed text-amber-300 flex gap-2">
            <AlertTriangle className="w-4 h-4 text-amber-500 shrink-0 mt-0.5" />
            <span>
              Configuring stricter constraints will mark <strong>{nonCompliantCount} key(s)</strong> as non-compliant. Server gateways will refuse signature proofs generated by these active configurations until updated.
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
