/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { BiometricEvidence } from '../types';
import { ShieldCheck, ShieldAlert, Key, Clock, Award, ShieldAlert as Lock, Activity } from 'lucide-react';

interface ActiveSessionContextProps {
  evidence: BiometricEvidence | null;
  onClearSession: () => void;
}

export const ActiveSessionContext: React.FC<ActiveSessionContextProps> = ({
  evidence,
  onClearSession
}) => {
  const getAssuranceLevel = () => {
    if (!evidence) {
      return {
        level: 'NONE / STANDALONE CREDENTIALS',
        badgeColor: 'bg-gray-100 text-gray-700 border-gray-200',
        title: 'Unauthenticated or Weak Assurance',
        desc: 'No certified face biometric verification exists in active session tokens.',
        icon: Lock,
        iconColor: 'text-gray-400'
      };
    }

    if (evidence.provenance === 'face_verified') {
      return {
        level: 'CRITICAL ASSURANCE (DIRECT FACE)',
        badgeColor: 'bg-green-100 text-green-900 border-green-300',
        title: 'Direct Hardware Secure Enclave Attested',
        desc: 'Phishing-resistant direct-captured face verification is active in current session headers.',
        icon: ShieldCheck,
        iconColor: 'text-green-600'
      };
    }

    if (evidence.provenance === 'upstream_face_trusted') {
      return {
        level: 'HIGH ASSURANCE (FEDERATED FACE)',
        badgeColor: 'bg-indigo-100 text-indigo-900 border-indigo-300',
        title: 'Federated Face Evidence Accepted',
        desc: 'Upstream certified face recognition claims mapped correctly to tenant validation rules.',
        icon: Award,
        iconColor: 'text-indigo-600'
      };
    }

    // Generic WebAuthn UV
    return {
      level: 'MODERATE ASSURANCE (GENERIC UV)',
      badgeColor: 'bg-amber-100 text-amber-900 border-amber-300',
      title: 'Browser Local User Gesture Accepted',
      desc: 'WebAuthn user verification flag processed. True biometric modality remains unknown.',
      icon: Key,
      iconColor: 'text-amber-600'
    };
  };

  const assurance = getAssuranceLevel();
  const Icon = assurance.icon;

  return (
    <div id="active-session-context-summary" className="bg-slate-900 text-white rounded-2xl p-5 shadow-md border border-slate-800 text-left">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        
        {/* Title details */}
        <div className="flex items-start gap-3.5">
          <div className={`p-2.5 rounded-xl bg-slate-800 ${assurance.iconColor}`}>
            <Icon className="w-5.5 h-5.5" />
          </div>
          <div>
            <div className="flex flex-wrap items-center gap-2">
              <span className={`text-[9px] font-bold font-mono tracking-wider px-2 py-0.5 rounded border uppercase ${assurance.badgeColor}`}>
                {assurance.level}
              </span>
              {evidence && (
                <span className="text-[10px] text-indigo-300 font-mono flex items-center gap-1">
                  <Activity className="w-3.5 h-3.5" /> Freshness: {evidence.freshnessSeconds}s old
                </span>
              )}
            </div>
            <h4 className="text-sm font-bold text-slate-100 mt-1">{assurance.title}</h4>
            <p className="text-slate-400 text-xs mt-0.5 leading-relaxed">{assurance.desc}</p>
          </div>
        </div>

        {/* Clear/Reset mock session button */}
        {evidence && (
          <button
            type="button"
            onClick={onClearSession}
            className="text-[10px] font-bold text-slate-400 hover:text-white border border-slate-700 hover:border-slate-500 rounded-lg px-2.5 py-1.5 font-mono uppercase shrink-0 transition"
          >
            Clear Active Context
          </button>
        )}
      </div>

      {/* Active AMR values verification tray */}
      <div className="pt-3.5 flex flex-wrap items-center gap-x-6 gap-y-2 text-[11px] text-slate-400">
        <div>
          Session ID: <span className="text-indigo-300 font-mono">sess-e20fea675118</span>
        </div>
        <div>
          Active AMR Array: <span className="text-slate-200 font-mono font-semibold bg-slate-800 px-1.5 py-0.5 rounded">
            {evidence ? `["${evidence.amr}"]` : '[]'}
          </span>
        </div>
        {evidence && (
          <>
            <div>
              Issuer ID: <span className="text-slate-200 font-mono">{evidence.issuer}</span>
            </div>
            <div className="flex items-center gap-1">
              <Clock className="w-3.5 h-3.5 text-slate-500" />
              Assurance Exp: <span className="text-slate-200 font-mono">1 Hour Max</span>
            </div>
          </>
        )}
      </div>
    </div>
  );
};
