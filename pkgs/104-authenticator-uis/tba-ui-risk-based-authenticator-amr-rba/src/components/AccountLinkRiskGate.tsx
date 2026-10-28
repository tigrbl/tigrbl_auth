/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { ShieldAlert, CheckCircle, AlertTriangle, Key, ShieldCheck, Mail } from 'lucide-react';
import { UserEnterpriseIdentity } from '../types';

interface AccountLinkRiskGateProps {
  localEmail: string;
  mappedIdentity: UserEnterpriseIdentity;
  onApprove: () => void;
  onReject: () => void;
}

export default function AccountLinkRiskGate({
  localEmail,
  mappedIdentity,
  onApprove,
  onReject,
}: AccountLinkRiskGateProps) {
  const [requireStepUp, setRequireStepUp] = useState<boolean>(true);
  const [stepUpVerified, setStepUpVerified] = useState<boolean>(false);
  const [disclaimerChecked, setDisclaimerChecked] = useState<boolean>(false);
  const [totpCode, setTotpCode] = useState<string>('');
  const [stepUpError, setStepUpError] = useState<string>('');

  const emailDomainsMatch = localEmail.split('@')[1] === mappedIdentity.email.split('@')[1];
  const userNamesMatch = localEmail.split('@')[0] === mappedIdentity.email.split('@')[0];

  const handleStepUpVerify = (e: React.FormEvent) => {
    e.preventDefault();
    if (!totpCode || totpCode.length < 6) {
      setStepUpError('Please enter a valid 6-digit confirmation code.');
      return;
    }
    // Simulate verification
    setStepUpVerified(true);
    setStepUpError('');
  };

  const isApprovedToLink = (!requireStepUp || stepUpVerified) && disclaimerChecked;

  return (
    <div id="account-link-risk-gate" className="w-full max-w-lg bg-white rounded-2xl border border-slate-200 shadow-xl overflow-hidden">
      <div className="p-6 bg-amber-50 border-b border-amber-200/60 flex gap-4">
        <div className="w-12 h-12 rounded-xl bg-amber-100 flex items-center justify-center shrink-0">
          <ShieldAlert className="w-6 h-6 text-amber-700" />
        </div>
        <div>
          <span className="text-[10px] font-mono font-semibold text-amber-800 uppercase bg-amber-100 px-1.5 py-0.5 rounded">
            Security Risk Assessment
          </span>
          <h3 className="font-display text-lg font-bold text-amber-950 mt-1.5 leading-tight">
            Confirm Enterprise Account Association
          </h3>
          <p className="text-xs text-amber-800 mt-1">
            An automatic Windows credential was detected. Verify association details before authorizing silent logins.
          </p>
        </div>
      </div>

      <div className="p-6 space-y-6">
        {/* Verification Matrix */}
        <div className="space-y-3">
          <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Identity Mapping Conformance</h4>

          <div className="space-y-2.5">
            {/* Domain check */}
            <div className="flex items-center justify-between p-3 rounded-lg border border-slate-200 bg-slate-50">
              <div className="flex gap-2 text-xs">
                <CheckCircle className="w-4 h-4 text-emerald-600 shrink-0" />
                <div>
                  <p className="font-semibold text-slate-800">Realm Domain Verified</p>
                  <p className="text-[11px] text-slate-500">Directory domain <span className="font-mono">{mappedIdentity.domain}</span> matches an active tenant.</p>
                </div>
              </div>
              <span className="text-[10px] bg-emerald-50 text-emerald-700 font-mono font-semibold px-2 py-0.5 rounded border border-emerald-200">PASS</span>
            </div>

            {/* Email mapping check */}
            <div className={`flex items-center justify-between p-3 rounded-lg border ${emailDomainsMatch ? 'border-slate-200 bg-slate-50' : 'border-amber-200 bg-amber-50/40'}`}>
              <div className="flex gap-2 text-xs">
                {emailDomainsMatch ? (
                  <CheckCircle className="w-4 h-4 text-emerald-600 shrink-0" />
                ) : (
                  <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" />
                )}
                <div>
                  <p className="font-semibold text-slate-800">Email Address Matching</p>
                  <p className="text-[11px] text-slate-500">
                    Local App Account (<span className="font-semibold">{localEmail}</span>) vs Workstation (<span className="font-semibold">{mappedIdentity.email}</span>)
                  </p>
                </div>
              </div>
              <span className={`text-[10px] font-mono font-semibold px-2 py-0.5 rounded border ${
                emailDomainsMatch ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : 'bg-amber-100 text-amber-700 border-amber-200'
              }`}>
                {emailDomainsMatch ? 'CONFIRMED' : 'NAME_MISMATCH'}
              </span>
            </div>
          </div>
        </div>

        {/* Step Up Re-authentication */}
        {requireStepUp && (
          <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 space-y-4">
            <div className="flex gap-2">
              <Key className="w-4 h-4 text-slate-500 mt-0.5" />
              <div>
                <h4 className="text-xs font-semibold text-slate-800">Step-Up Verification Required</h4>
                <p className="text-[11px] text-slate-500 leading-relaxed">
                  To protect against session hijacking, please verify your current app login session with your 2FA authentication code before linking.
                </p>
              </div>
            </div>

            {stepUpVerified ? (
              <div className="p-3 bg-emerald-50 border border-emerald-100 rounded-lg flex items-center gap-2 text-xs text-emerald-800 font-medium">
                <ShieldCheck className="w-5 h-5 text-emerald-600" />
                <span>Verification completed successfully. Takeover safeguards satisfied.</span>
              </div>
            ) : (
              <form onSubmit={handleStepUpVerify} className="flex gap-2 items-end">
                <div className="flex-1">
                  <label htmlFor="totp-code" className="block text-[10px] font-medium text-slate-500 uppercase tracking-wider mb-1.5">MFA / TOTP 6-Digit Code</label>
                  <input
                    type="text"
                    id="totp-code"
                    placeholder="123456"
                    maxLength={6}
                    value={totpCode}
                    onChange={(e) => setTotpCode(e.target.value.replace(/\D/g, ''))}
                    className="w-full px-3 py-2 rounded border border-slate-300 text-xs bg-white text-slate-800 outline-none focus:border-blue-500 font-mono text-center tracking-widest"
                  />
                </div>
                <button
                  type="submit"
                  id="btn-verify-step-up"
                  className="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded text-xs font-semibold cursor-pointer"
                >
                  Verify MFA
                </button>
              </form>
            )}

            {stepUpError && <p className="text-[11px] text-red-600">{stepUpError}</p>}
          </div>
        )}

        {/* Takeover Disclaimer */}
        <div className="flex gap-2.5 items-start">
          <input
            type="checkbox"
            id="chk-disclaimer"
            checked={disclaimerChecked}
            onChange={(e) => setDisclaimerChecked(e.target.checked)}
            className="w-4 h-4 mt-0.5 rounded text-blue-600 border-slate-300 focus:ring-blue-500 cursor-pointer"
          />
          <label htmlFor="chk-disclaimer" className="text-xs text-slate-600 leading-relaxed cursor-pointer select-none">
            I confirm that this Windows station identity (<span className="font-semibold font-mono">{mappedIdentity.upn}</span>) belongs to me and is authorized to sign into my account (<span className="font-semibold">{localEmail}</span>) automatically.
          </label>
        </div>

        {/* Form CTA Buttons */}
        <div className="flex gap-3 pt-3 border-t border-slate-100">
          <button
            onClick={onReject}
            id="btn-reject-link"
            className="flex-1 py-2.5 border border-slate-200 hover:bg-slate-50 text-slate-700 font-medium text-xs rounded-lg transition-all cursor-pointer text-center"
          >
            Decline Mapping
          </button>
          <button
            onClick={onApprove}
            disabled={!isApprovedToLink}
            id="btn-approve-link"
            className="flex-1 py-2.5 bg-amber-600 hover:bg-amber-700 disabled:bg-slate-200 disabled:text-slate-400 disabled:cursor-not-allowed text-white font-semibold text-xs rounded-lg transition-all cursor-pointer text-center"
          >
            Authorize Account Link
          </button>
        </div>
      </div>
    </div>
  );
}
