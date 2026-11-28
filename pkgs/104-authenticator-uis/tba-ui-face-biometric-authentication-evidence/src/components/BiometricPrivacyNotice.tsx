/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { ShieldCheck, Info, FileText, Download, Check, AlertTriangle, ArrowRight } from 'lucide-react';
import { CONSENT_TEXTS } from '../mockData';

interface BiometricPrivacyNoticeProps {
  onAccept: (consentVersion: string) => void;
  onDecline: () => void;
  initialStatus?: 'accepted' | 'declined' | 'withdrawn';
}

export const BiometricPrivacyNotice: React.FC<BiometricPrivacyNoticeProps> = ({
  onAccept,
  onDecline,
  initialStatus = 'declined'
}) => {
  const [downloaded, setDownloaded] = useState(false);
  const [hasScrolledToBottom, setHasScrolledToBottom] = useState(false);

  const handleScroll = (e: React.UIEvent<HTMLDivElement>) => {
    const target = e.currentTarget;
    if (target.scrollHeight - target.scrollTop <= target.clientHeight + 40) {
      setHasScrolledToBottom(true);
    }
  };

  const downloadConsent = () => {
    const textContent = `
=== BIOMETRIC PRIVACY AND CONSENT RECORD ===
Version: ${CONSENT_TEXTS.version}
Legal Basis: ${CONSENT_TEXTS.legalBasis}
Title: ${CONSENT_TEXTS.title}

1. PURPOSE OF PROCESSING
${CONSENT_TEXTS.purpose}

2. SECURE PROCESSING & BIOMETRIC DATA BOUNDARY
${CONSENT_TEXTS.processingBoundary}

3. DATA RETENTION & CRYPTOGRAPHIC ERASURE
${CONSENT_TEXTS.retention}

4. THIRD-PARTY SHARING RESTRICTIONS
${CONSENT_TEXTS.sharing}

5. EQUIVALENT ALTERNATIVES
${CONSENT_TEXTS.alternatives}

Generated at: ${new Date().toISOString()}
Status: APPROVED / ACCEPTED BY SUBJECT
===========================================
`;
    const blob = new Blob([textContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `biometric-consent-${CONSENT_TEXTS.version}.txt`;
    link.click();
    URL.revokeObjectURL(url);
    setDownloaded(true);
  };

  return (
    <div id="biometric-privacy-notice-card" className="bg-white border border-gray-200 rounded-2xl shadow-sm p-6 max-w-2xl mx-auto">
      {/* Header */}
      <div className="flex items-start gap-4 mb-5">
        <div className="p-3 bg-indigo-50 text-indigo-600 rounded-xl">
          <ShieldCheck className="w-6 h-6" />
        </div>
        <div>
          <h2 className="text-xl font-bold text-gray-900 tracking-tight">{CONSENT_TEXTS.title}</h2>
          <p className="text-xs font-mono text-gray-500 mt-0.5">
            Document Reference: <span className="text-indigo-600 font-semibold">{CONSENT_TEXTS.version}</span> • Legal Framework: Active Compliance
          </p>
        </div>
      </div>

      {/* Legal Framework Sub-Header */}
      <div className="bg-gray-50 border-l-4 border-indigo-500 p-3 rounded-r-lg mb-5 flex items-center gap-3">
        <Info className="w-5 h-5 text-indigo-600 shrink-0" />
        <p className="text-xs text-gray-700">
          <strong className="text-gray-900">Legal Basis:</strong> {CONSENT_TEXTS.legalBasis}
        </p>
      </div>

      {/* Main Notice Scroll Box */}
      <div 
        onScroll={handleScroll}
        className="max-h-[260px] overflow-y-auto border border-gray-200 rounded-xl p-4 mb-5 text-sm leading-relaxed text-gray-600 space-y-4 bg-gray-50/50 scrollbar-thin"
      >
        <div>
          <h4 className="font-semibold text-gray-900 mb-1 flex items-center gap-1.5 text-xs uppercase tracking-wider text-gray-500">
            1. Purpose & Core Processing
          </h4>
          <p className="text-gray-700 text-xs sm:text-sm">{CONSENT_TEXTS.purpose}</p>
        </div>

        <div>
          <h4 className="font-semibold text-gray-900 mb-1 flex items-center gap-1.5 text-xs uppercase tracking-wider text-gray-500">
            2. Biometric Isolation Boundary
          </h4>
          <div className="bg-amber-50/50 border border-amber-200 rounded-lg p-2.5 text-amber-900 text-xs sm:text-sm space-y-1.5">
            <p className="font-medium text-amber-900 flex items-center gap-1">
              <AlertTriangle className="w-4 h-4 shrink-0 text-amber-600" /> Secure Processing Commitment
            </p>
            <p className="text-amber-800 text-xs">{CONSENT_TEXTS.processingBoundary}</p>
          </div>
        </div>

        <div>
          <h4 className="font-semibold text-gray-900 mb-1 flex items-center gap-1.5 text-xs uppercase tracking-wider text-gray-500">
            3. Lifecycle Deletion & Shg
          </h4>
          <p className="text-gray-700 text-xs sm:text-sm">{CONSENT_TEXTS.retention}</p>
          <p className="text-gray-700 text-xs sm:text-sm mt-2">{CONSENT_TEXTS.sharing}</p>
        </div>

        <div>
          <h4 className="font-semibold text-gray-900 mb-1 flex items-center gap-1.5 text-xs uppercase tracking-wider text-gray-500">
            4. Alternative Auth Mechanisms
          </h4>
          <p className="text-gray-700 text-xs sm:text-sm">{CONSENT_TEXTS.alternatives}</p>
        </div>
      </div>

      {/* Consent Action Checklist / Download */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4 py-3 border-t border-b border-gray-100 mb-6">
        <div className="flex items-center gap-2.5">
          <FileText className="w-5 h-5 text-gray-400 shrink-0" />
          <div className="text-left">
            <p className="text-xs text-gray-500 font-medium">Downloadable Record</p>
            <p className="text-xs text-gray-900">Download a local signed copy of this agreement</p>
          </div>
        </div>
        <button
          type="button"
          onClick={downloadConsent}
          className="flex items-center justify-center gap-2 px-3.5 py-2 border border-gray-200 rounded-xl text-xs font-semibold text-gray-700 hover:bg-gray-50 transition"
        >
          {downloaded ? <Check className="w-4 h-4 text-green-600" /> : <Download className="w-4 h-4" />}
          {downloaded ? 'Downloaded Consent Text' : 'Download Consent Text'}
        </button>
      </div>

      {/* Scrolling Cue */}
      {!hasScrolledToBottom && (
        <p className="text-center text-xs text-indigo-600 animate-pulse mb-4">
          Please scroll through the complete notice to unlock enrollment actions.
        </p>
      )}

      {/* Decision Triggers */}
      <div className="flex flex-col sm:flex-row items-stretch justify-end gap-3">
        <button
          type="button"
          onClick={onDecline}
          className="px-4 py-2.5 border border-gray-200 hover:border-gray-300 rounded-xl text-sm font-semibold text-gray-700 hover:bg-gray-50 transition"
        >
          Decline & Use Alternative Method
        </button>
        <button
          type="button"
          disabled={!hasScrolledToBottom && !downloaded}
          onClick={() => onAccept(CONSENT_TEXTS.version)}
          className={`flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold text-white transition ${
            (hasScrolledToBottom || downloaded)
              ? 'bg-indigo-600 hover:bg-indigo-700 shadow-sm cursor-pointer'
              : 'bg-indigo-400/75 cursor-not-allowed text-indigo-50/95'
          }`}
        >
          I Provide Informed Consent
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>

      {/* Accessible Alternative Disclaimer */}
      <p className="text-[11px] text-gray-400 text-center mt-4 leading-relaxed">
        By continuing, you authorize local facial sample collection in the secure native biometric sandbox. No template is generated unless validation succeed. Declining will route you to standard security key mechanisms.
      </p>
    </div>
  );
};
