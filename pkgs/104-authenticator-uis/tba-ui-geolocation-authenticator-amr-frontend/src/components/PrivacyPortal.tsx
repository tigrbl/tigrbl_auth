import React, { useState } from 'react';
import { LocationSourceBadge } from './LocationSourceBadge';
import { 
  Shield, Eye, ShieldAlert, ShieldCheck, Trash2, Smartphone, 
  MapPin, AlertTriangle, CheckCircle, RefreshCw, Key, HelpCircle 
} from 'lucide-react';

interface PrivacyPortalProps {
  sessionContext: {
    userEmail: string;
    ipAddress: string;
    coarseRegion: string;
    isp: string;
    lastValidated: string;
    accuracy: number;
    auditReference: string;
  };
  consentList: any[];
  onRevokeConsent: (id: string) => void;
  onEnrollDevice: (deviceDetails: any) => void;
}

export const PrivacyPortal: React.FC<PrivacyPortalProps> = ({
  sessionContext,
  consentList,
  onRevokeConsent,
  onEnrollDevice
}) => {
  const [enrollName, setEnrollName] = useState('');
  const [enrollType, setEnrollType] = useState('mobile');
  const [alertTrusted, setAlertTrusted] = useState<boolean | null>(null);

  const handleEnroll = (e: React.FormEvent) => {
    e.preventDefault();
    if (!enrollName.trim()) return;
    onEnrollDevice({
      name: enrollName,
      type: enrollType,
      enrolledAt: new Date().toISOString()
    });
    setEnrollName('');
  };

  return (
    <div className="space-y-6" id="privacy-portal">
      {/* Active Session Context Detail */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm space-y-4">
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <div>
            <h3 className="text-sm font-bold text-slate-900 font-display">
              Active Security & Session Context
            </h3>
            <p className="text-xs text-slate-500">
              Your real-time security telemetry profile as recognized by corporate identity checks
            </p>
          </div>
          <span className="text-[10px] font-mono bg-slate-100 text-slate-600 px-2 py-1 rounded">
            AUDIT_ID: {sessionContext.auditReference}
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-xs">
          <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
            <span className="text-[9px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
              Connection IP Origin
            </span>
            <div className="font-semibold text-slate-800">{sessionContext.ipAddress}</div>
            <div className="text-[10px] text-slate-400 mt-0.5">{sessionContext.isp}</div>
          </div>

          <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
            <span className="text-[9px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
              Geographic Region
            </span>
            <div className="font-semibold text-slate-800">{sessionContext.coarseRegion}</div>
            <div className="text-[10px] text-amber-600 font-semibold mt-0.5">Approximate (Network)</div>
          </div>

          <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
            <span className="text-[9px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
              Telemetry Accuracy
            </span>
            <div className="font-semibold text-slate-800">&plusmn; {sessionContext.accuracy} meters</div>
            <div className="text-[10px] text-slate-400 mt-0.5">GPS Hardware coordinates</div>
          </div>

          <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
            <span className="text-[9px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
              Policy Outcome
            </span>
            <div className="font-semibold text-emerald-700 flex items-center gap-1">
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>Allow (Compliant)</span>
            </div>
            <div className="text-[10px] text-slate-400 mt-0.5">Last Checked: {new Date(sessionContext.lastValidated).toLocaleTimeString()}</div>
          </div>
        </div>
      </div>

      {/* P1: Security Anomalies / Unfamiliar Location Alerts */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm space-y-4">
        <div>
          <h3 className="text-sm font-bold text-slate-900 font-display">
            Active Security Incident Response Panel
          </h3>
          <p className="text-xs text-slate-500">
            Audit logs flag connections originating from unfamiliar geographic locations or anomalous ISP subnets.
          </p>
        </div>

        {alertTrusted === null ? (
          <div className="p-4 bg-amber-50 border border-amber-200 rounded-xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 animate-pulse">
            <div className="flex gap-3">
              <ShieldAlert className="w-5 h-5 text-amber-600 shrink-0 mt-0.5 sm:mt-0" />
              <div className="text-xs text-amber-800">
                <strong>Anomalous Connection Flagged:</strong> A sign-in was attempted from an unrecognized subnet in <strong>Paris, Ile-de-France</strong> using an Android browser.
                <div className="text-[10px] text-amber-600 font-mono mt-0.5">Time: 1 hour ago | ISP: Orange S.A. | CIDR: 82.231.0.0/16</div>
              </div>
            </div>

            <div className="flex gap-2 shrink-0">
              <button
                onClick={() => setAlertTrusted(true)}
                className="bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-[11px] px-3 py-1.5 rounded-lg transition-all"
              >
                I Recognize This Connection
              </button>
              <button
                onClick={() => setAlertTrusted(false)}
                className="bg-rose-600 hover:bg-rose-700 text-white font-semibold text-[11px] px-3 py-1.5 rounded-lg transition-all"
              >
                Flag & Lock Account
              </button>
            </div>
          </div>
        ) : alertTrusted === true ? (
          <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-xl flex items-center gap-2.5 text-xs text-emerald-800">
            <CheckCircle className="w-4.5 h-4.5 text-emerald-600 shrink-0" />
            <span>Orange S.A. (Paris, France) subnets added to your temporary travel profile. Session authorized.</span>
          </div>
        ) : (
          <div className="p-4 bg-rose-50 border border-rose-200 rounded-xl flex items-center gap-2.5 text-xs text-rose-800">
            <ShieldCheck className="w-4.5 h-4.5 text-rose-600 shrink-0" />
            <span>Account locked successfully. Session revoked, cryptographic access tokens flushed, and incident logged under IT Support ID: INC-88219.</span>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Consent Review & Withdrawal */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm space-y-4">
          <div>
            <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider font-mono">
              Precise-Location Consent Registry
            </h4>
            <p className="text-[11px] text-slate-400 mt-0.5">
              Review and revoke approved geographic consent agreements
            </p>
          </div>

          <div className="space-y-3">
            {consentList.length === 0 ? (
              <div className="text-center py-6 text-xs text-slate-400">
                No active geolocation consent agreements found.
              </div>
            ) : (
              consentList.map((c) => (
                <div key={c.id} className="border border-slate-150 rounded-lg p-3.5 space-y-3 hover:border-slate-300 transition-all">
                  <div className="flex items-start justify-between">
                    <div>
                      <span className="text-[10px] bg-indigo-50 border border-indigo-100 text-indigo-700 px-2 py-0.5 rounded-full font-mono font-semibold">
                        {c.precision}
                      </span>
                      <h5 className="text-xs font-semibold text-slate-800 mt-1.5">
                        {c.purpose}
                      </h5>
                    </div>
                    <button
                      title="Revoke Consent"
                      onClick={() => onRevokeConsent(c.id)}
                      className="p-1 hover:bg-rose-50 rounded text-rose-400 hover:text-rose-600 transition-colors"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>

                  <div className="grid grid-cols-2 gap-2 text-[10px] text-slate-500 font-mono">
                    <div>
                      <span className="text-slate-400 block">GRANTED_AT</span>
                      <span>{new Date(c.grantedAt).toLocaleDateString()}</span>
                    </div>
                    <div>
                      <span className="text-slate-400 block">RETAINED_FOR</span>
                      <span>{c.retention}</span>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Managed-Device Enrollment */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm space-y-4">
          <div>
            <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider font-mono">
              Managed Device Enrollment
            </h4>
            <p className="text-[11px] text-slate-400 mt-0.5">
              Register corporate posture devices to satisfy enterprise zone rules
            </p>
          </div>

          <form onSubmit={handleEnroll} className="space-y-3">
            <div>
              <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
                Device Model Name
              </label>
              <input
                type="text"
                placeholder="e.g. MacBook Pro M3 (Austinhq-Mac-4)"
                value={enrollName}
                onChange={(e) => setEnrollName(e.target.value)}
                className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-1.5 text-xs focus:outline-none focus:border-indigo-500"
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
                  Operating Platform
                </label>
                <select
                  value={enrollType}
                  onChange={(e) => setEnrollType(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 text-xs focus:outline-none"
                >
                  <option value="macOS">macOS Core</option>
                  <option value="iOS">iOS Device</option>
                  <option value="Windows">Windows Enterprise</option>
                  <option value="Android">Android MDM</option>
                </select>
              </div>

              <div className="flex items-end">
                <button
                  type="submit"
                  className="w-full bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold py-1.5 rounded-lg shadow-sm"
                >
                  Enroll Device Posture
                </button>
              </div>
            </div>
          </form>

          {/* Guidelines info */}
          <div className="bg-slate-50 border border-slate-100 rounded-lg p-3 text-[11px] text-slate-500 leading-normal flex gap-2">
            <Smartphone className="w-4 h-4 text-slate-400 shrink-0 mt-0.5" />
            <span>
              Device posture enrollment adds cryptographic hardware identifiers ontoRADIUS/802.1X maps, allowing background posture checks without GPS popups.
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
