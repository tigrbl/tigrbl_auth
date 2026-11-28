/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { ShieldCheck, UserCheck, Key, FileText, Info, HelpCircle, ShieldAlert, CheckCircle2 } from 'lucide-react';
import { UserEnterpriseIdentity } from '../types';

interface EnterpriseIdentityProjectionProps {
  identity: UserEnterpriseIdentity;
  onLink: () => void;
  onUnlink: () => void;
  onTriggerMfaStepUp?: () => void;
}

export default function EnterpriseIdentityProjection({
  identity,
  onLink,
  onUnlink,
  onTriggerMfaStepUp,
}: EnterpriseIdentityProjectionProps) {
  const [showUnlinkWarning, setShowUnlinkWarning] = useState(false);

  const isLinked = !!identity.linkedAt;

  const handleUnlinkClick = () => {
    setShowUnlinkWarning(true);
  };

  const confirmUnlink = () => {
    setShowUnlinkWarning(false);
    onUnlink();
  };

  return (
    <div id="enterprise-identity-projection" className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
      {/* Projection Header */}
      <div className="p-6 bg-slate-900 text-white flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-blue-600/20 border border-blue-400/20 flex items-center justify-center text-blue-400">
            <UserCheck className="w-5 h-5" />
          </div>
          <div>
            <h3 className="font-display font-semibold text-base leading-tight">Mapped Enterprise Identity</h3>
            <p className="text-xs text-slate-400">Security Principal Projection</p>
          </div>
        </div>
        <div className="flex flex-col items-end">
          <span className={`text-[10px] font-mono font-semibold px-2 py-0.5 rounded uppercase ${
            identity.status === 'active' ? 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/20' :
            identity.status === 'degraded' ? 'bg-amber-500/15 text-amber-400 border border-amber-500/20' :
            'bg-rose-500/15 text-rose-400 border border-rose-500/20'
          }`}>
            Status: {identity.status}
          </span>
          <span className="text-[9px] text-slate-400 mt-1">Assurance: {identity.assuranceLevel}</span>
        </div>
      </div>

      {/* Identity core variables */}
      <div className="p-6 space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-3 bg-slate-50 border border-slate-100 rounded-lg">
            <span className="text-[10px] font-mono text-slate-400 uppercase">User Principal Name (UPN)</span>
            <p className="text-sm font-semibold text-slate-800 mt-1 font-mono break-all">{identity.upn}</p>
          </div>

          <div className="p-3 bg-slate-50 border border-slate-100 rounded-lg">
            <span className="text-[10px] font-mono text-slate-400 uppercase">sAMAccountName</span>
            <p className="text-sm font-semibold text-slate-800 mt-1 font-mono">{identity.samAccountName}</p>
          </div>

          <div className="p-3 bg-slate-50 border border-slate-100 rounded-lg md:col-span-2">
            <span className="text-[10px] font-mono text-slate-400 uppercase">Active Directory SID (Security ID)</span>
            <p className="text-xs font-semibold text-slate-700 mt-1 font-mono break-all">{identity.sid}</p>
          </div>

          <div className="p-3 bg-slate-50 border border-slate-100 rounded-lg">
            <span className="text-[10px] font-mono text-slate-400 uppercase">Display Name</span>
            <p className="text-sm font-semibold text-slate-800 mt-1">{identity.displayName}</p>
          </div>

          <div className="p-3 bg-slate-50 border border-slate-100 rounded-lg">
            <span className="text-[10px] font-mono text-slate-400 uppercase">Registered Directory Email</span>
            <p className="text-sm font-semibold text-slate-800 mt-1 break-all">{identity.email}</p>
          </div>
        </div>

        {/* Evidence & Provenance claims */}
        <div className="space-y-3">
          <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wider flex items-center gap-1.5">
            <ShieldCheck className="w-4 h-4 text-slate-400" />
            WIA Ceremony Token Evidence
          </h4>

          {identity.lastAuthEvidence ? (
            <div className="bg-slate-50 border border-slate-100 rounded-xl p-4 space-y-3 text-xs">
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                <div>
                  <span className="text-slate-400 block">AMR Registry</span>
                  <span className="font-mono text-blue-700 font-semibold">{identity.lastAuthEvidence.amr.join(', ')}</span>
                </div>
                <div>
                  <span className="text-slate-400 block">Negotiated SPN</span>
                  <span className="font-mono text-slate-700 font-medium truncate block">{identity.lastAuthEvidence.spnUsed}</span>
                </div>
                <div>
                  <span className="text-slate-400 block">Ticket Freshness</span>
                  <span className="font-mono text-slate-700">{identity.lastAuthEvidence.ticketFreshnessSeconds}s ago</span>
                </div>
                <div>
                  <span className="text-slate-400 block">Channel Bound</span>
                  <span className="font-semibold text-emerald-600 flex items-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5" /> Bound (EPA)
                  </span>
                </div>
                <div className="col-span-2">
                  <span className="text-slate-400 block">Authentication Timestamp</span>
                  <span className="font-mono text-slate-600">{new Date(identity.lastAuthEvidence.authTime).toLocaleString()}</span>
                </div>
              </div>
            </div>
          ) : (
            <div className="p-3 bg-slate-50 border border-slate-100 rounded-xl text-xs text-slate-500 italic">
              No active WIA session metadata recorded. Perform a workstation negotiation to collect secure evidence.
            </div>
          )}
        </div>

        {/* Directory Memberships */}
        <div className="space-y-3">
          <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wider flex items-center gap-1.5">
            <Key className="w-4 h-4 text-slate-400" />
            Security Group Memberships
          </h4>
          <div className="flex flex-wrap gap-2">
            {identity.memberOf.map((grp, idx) => (
              <span key={idx} className="bg-slate-100 border border-slate-200/60 rounded px-2 py-1 text-xs font-mono text-slate-700">
                {grp}
              </span>
            ))}
          </div>
        </div>

        {/* Link / Unlink controls */}
        <div className="border-t border-slate-100 pt-6 space-y-4">
          {showUnlinkWarning ? (
            <div className="p-4 bg-rose-50 border border-rose-200 rounded-xl space-y-3">
              <div className="flex gap-2 text-rose-800">
                <ShieldAlert className="w-5 h-5 text-rose-600 shrink-0" />
                <div>
                  <h5 className="font-semibold text-sm">Are you sure you want to unlink?</h5>
                  <p className="text-xs mt-0.5 text-rose-700 leading-relaxed">
                    Unlinking removes the automatic, single-click Windows credential mapping. You will be required to log in with backup passwords and MFA codes next time.
                  </p>
                </div>
              </div>
              <div className="flex gap-2 justify-end">
                <button
                  onClick={() => setShowUnlinkWarning(false)}
                  className="px-3 py-1.5 bg-white border border-slate-200 rounded text-xs font-medium text-slate-700 hover:bg-slate-50 cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  onClick={confirmUnlink}
                  id="btn-confirm-unlink"
                  className="px-3 py-1.5 bg-rose-600 hover:bg-rose-700 text-white rounded text-xs font-semibold cursor-pointer"
                >
                  Confirm Unlink Identity
                </button>
              </div>
            </div>
          ) : (
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <span className="text-xs text-slate-400 block font-mono">TAKEOVER MITIGATION CHECK</span>
                {isLinked ? (
                  <p className="text-xs text-slate-600 mt-1 leading-relaxed">
                    Identity linked securely at <span className="font-mono text-slate-900 font-semibold">{identity.linkedAt}</span>.
                  </p>
                ) : (
                  <p className="text-xs text-amber-600 font-medium mt-1">
                    Identity is not currently active for single-sign on mapping. Confirmation required.
                  </p>
                )}
              </div>

              <div className="flex gap-2">
                {isLinked ? (
                  <>
                    {onTriggerMfaStepUp && (
                      <button
                        onClick={onTriggerMfaStepUp}
                        className="py-2 px-3 border border-slate-200 hover:bg-slate-50 text-slate-700 rounded-lg text-xs font-medium cursor-pointer"
                      >
                        Step-Up Verification
                      </button>
                    )}
                    <button
                      onClick={handleUnlinkClick}
                      id="btn-unlink-identity"
                      className="py-2 px-4 bg-rose-50 hover:bg-rose-100 text-rose-700 border border-rose-200/60 rounded-lg text-xs font-semibold cursor-pointer transition-colors"
                    >
                      Unlink Workstation Account
                    </button>
                  </>
                ) : (
                  <button
                    onClick={onLink}
                    id="btn-link-identity"
                    className="py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-semibold cursor-pointer transition-colors shadow-sm shadow-blue-500/10"
                  >
                    Confirm & Link Enterprise Identity
                  </button>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
