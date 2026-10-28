import React from 'react';
import { CeremonySession, AuthenticatorMethod } from '../types';
import { Shield, Key, FileCode, CheckCircle2, Copy, Terminal } from 'lucide-react';

interface EvidenceProps {
  session: CeremonySession;
  methodsUsed: AuthenticatorMethod[];
  onReset: () => void;
}

export const IndependenceEvidenceSummary: React.FC<EvidenceProps> = ({ session, methodsUsed, onReset }) => {
  const getGroupLabel = (method: AuthenticatorMethod) => {
    switch (method) {
      case 'passkey':
      case 'smartcard':
        return 'Group Hardware (FIDO2 / Cryptographic Key)';
      case 'totp':
        return 'Group Software (HMAC Application)';
      case 'push':
        return 'Group Mobile App (OOB Push Callback)';
      case 'sms':
      case 'voice':
        return 'Group Telecom (Cellular Trunk OTP)';
      case 'email':
        return 'Group Cloud Infra (Mail Relay)';
    }
  };

  const amrList = session.amrEmitted.length > 0 ? session.amrEmitted : ['mca', ...methodsUsed];

  return (
    <div className="bg-zinc-950/60 rounded-xl border border-zinc-800 p-5 space-y-5" id="independence-evidence-summary">
      <div className="text-center space-y-2 py-3 border-b border-zinc-900">
        <div className="inline-flex items-center justify-center bg-emerald-500/10 text-emerald-400 p-3 rounded-full border border-emerald-500/20 animate-bounce">
          <Shield className="h-7 w-7" />
        </div>
        <h3 className="font-semibold text-zinc-100 text-lg">Multi-Channel Authentication Verified</h3>
        <p className="text-xs text-zinc-400 max-w-sm mx-auto">
          The cryptographic verification engine confirmed that multiple independent, disjoint channels were successfully completed.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Certificate / Session Info */}
        <div className="bg-zinc-900/40 rounded-xl border border-zinc-800 p-4 space-y-3">
          <h4 className="text-xs font-semibold text-zinc-300 flex items-center gap-2 uppercase tracking-wider font-mono">
            <Key className="h-3.5 w-3.5 text-purple-400" />
            MCA Assurance Evidence
          </h4>

          <div className="space-y-2.5 text-xs">
            <div className="flex justify-between items-center py-1 border-b border-zinc-950">
              <span className="text-zinc-500 font-mono">Status</span>
              <span className="inline-flex items-center gap-1 text-emerald-400 font-semibold">
                <CheckCircle2 className="h-3 w-3" /> MCA COMPLETE
              </span>
            </div>
            <div className="flex justify-between items-center py-1 border-b border-zinc-950">
              <span className="text-zinc-500 font-mono">Subject</span>
              <span className="text-zinc-300 font-mono">{session.subject}</span>
            </div>
            <div className="flex justify-between items-center py-1 border-b border-zinc-950">
              <span className="text-zinc-500 font-mono">Tenant Identifier</span>
              <span className="text-zinc-300 font-mono truncate max-w-[130px]">{session.tenantId}</span>
            </div>
            <div className="flex justify-between items-center py-1 border-b border-zinc-950">
              <span className="text-zinc-500 font-mono">Correlation Token</span>
              <span className="text-zinc-300 font-mono truncate max-w-[130px]">{session.id}</span>
            </div>
            <div className="flex justify-between items-center py-1">
              <span className="text-zinc-500 font-mono">Device Context</span>
              <span className="text-zinc-300">{session.deviceOs} ({session.location})</span>
            </div>
          </div>
        </div>

        {/* AMR Cryptographic Details */}
        <div className="bg-zinc-900/40 rounded-xl border border-zinc-800 p-4 space-y-3">
          <h4 className="text-xs font-semibold text-zinc-300 flex items-center gap-2 uppercase tracking-wider font-mono">
            <FileCode className="h-3.5 w-3.5 text-indigo-400" />
            Authentication Method Reference (AMR)
          </h4>

          <div className="space-y-3">
            <div>
              <span className="text-[10px] text-zinc-500 uppercase font-bold tracking-wider font-mono block mb-1.5">
                Emitted AMR Claims List:
              </span>
              <div className="flex flex-wrap gap-1.5">
                {amrList.map((val) => (
                  <span
                    key={val}
                    className="px-2.5 py-1 bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 rounded-md font-mono text-[11px] font-semibold"
                  >
                    {val}
                  </span>
                ))}
              </div>
            </div>

            <div className="space-y-1.5 pt-1">
              <span className="text-[10px] text-zinc-500 uppercase font-bold tracking-wider font-mono block">
                Verified Independent Groups:
              </span>
              <div className="space-y-1">
                {methodsUsed.map((m, i) => (
                  <div key={m + i} className="flex items-center gap-1.5 text-[11px] font-mono text-zinc-400">
                    <span className="h-1 w-1 bg-emerald-400 rounded-full" />
                    <span>{getGroupLabel(m)}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Cryptographic Proof Output */}
      <div className="bg-zinc-900/60 rounded-xl border border-zinc-800 p-3 space-y-2">
        <div className="flex items-center justify-between">
          <span className="text-2xs font-mono text-zinc-500 uppercase font-bold flex items-center gap-1.5">
            <Terminal className="h-3.5 w-3.5 text-zinc-400" /> Server-Signed Evidence Envelope (MCA Signature)
          </span>
          <span className="text-2xs font-mono text-emerald-500/90 bg-emerald-500/10 px-1.5 py-0.5 rounded-md border border-emerald-500/20">
            Validated Signature
          </span>
        </div>
        <pre className="text-[9px] font-mono text-emerald-400/80 bg-black/40 p-2.5 rounded-lg overflow-x-auto leading-relaxed">
          {`{
  "alg": "RS256",
  "kid": "mca-verifier-key-2026",
  "payload": {
    "sub": "${session.subject}",
    "iss": "mca-orchestrator",
    "iat": 1784111578,
    "exp": 1784111878,
    "amr": ${JSON.stringify(amrList)},
    "mca_evidence": {
      "channels": ${JSON.stringify(methodsUsed)},
      "correlation_id": "${session.id}",
      "client_ip": "${session.ipAddress}",
      "tenant_id": "${session.tenantId}",
      "policy_decision": "INDEPENDENT_CHANNELS_VALIDATED"
    }
  },
  "signature": "SGVsbG8gZnJvbSB0aGUgb3JjaGVzdHJhdG9yLiB0aGlzIGlzIGEgc2lnbmVkIGV2aWRlbmNlIGVudmVsb3BlLg=="
}`}
        </pre>
      </div>

      <div className="flex justify-end">
        <button
          onClick={onReset}
          className="bg-zinc-100 hover:bg-zinc-200 text-zinc-950 text-xs font-semibold px-4 py-2 rounded-xl transition"
        >
          Restart Multi-Channel Ceremony
        </button>
      </div>
    </div>
  );
};
