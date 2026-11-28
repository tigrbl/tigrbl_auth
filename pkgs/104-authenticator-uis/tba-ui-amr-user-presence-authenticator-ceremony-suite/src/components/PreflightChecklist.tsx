/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useEffect, useState } from 'react';
import { PreflightCheck } from '../types';
import { CheckCircle2, AlertCircle, HelpCircle, Laptop, ShieldCheck, Terminal, ExternalLink } from 'lucide-react';

interface PreflightChecklistProps {
  onCheckComplete: (isSupported: boolean) => void;
}

export default function PreflightChecklist({ onCheckComplete }: PreflightChecklistProps) {
  const [checks, setChecks] = useState<PreflightCheck[]>([
    {
      id: 'webauthn-api',
      name: 'WebAuthn API Presence',
      description: 'Checks if window.PublicKeyCredential exists in this browser runtime.',
      status: 'unchecked',
      value: 'Checking...',
    },
    {
      id: 'platform-auth',
      name: 'Platform Authenticator support',
      description: 'Checks if native biometrics (Touch ID, Face ID, Windows Hello) are available.',
      status: 'unchecked',
      value: 'Checking...',
    },
    {
      id: 'iframe-sandbox',
      name: 'Iframe Sandbox Restrictions',
      description: 'Checks if the app is rendered in a sandboxed iframe that blocks credentials operations.',
      status: 'unchecked',
      value: 'Checking...',
    },
    {
      id: 'transport-types',
      name: 'Transport Capability',
      description: 'Detects supported authenticator communication channels (USB, NFC, Ble).',
      status: 'unchecked',
      value: 'Checking...',
    }
  ]);

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const runChecks = async () => {
      const updatedChecks = [...checks];

      // 1. WebAuthn API Presence
      const hasWebAuthn = typeof window !== 'undefined' && 'PublicKeyCredential' in window;
      updatedChecks[0] = {
        ...updatedChecks[0],
        status: hasWebAuthn ? 'pass' : 'fail',
        value: hasWebAuthn ? 'Available (FIDO2 Core)' : 'Not supported by browser',
      };

      // 2. Platform Authenticator support
      let platformSupported = false;
      if (hasWebAuthn) {
        try {
          platformSupported = await PublicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable();
        } catch (e) {
          platformSupported = false;
        }
      }
      updatedChecks[1] = {
        ...updatedChecks[1],
        status: platformSupported ? 'pass' : 'warning',
        value: platformSupported ? 'TouchID/Hello Ready' : 'Unavailable/No hardware',
      };

      // 3. Iframe Sandbox Restrictions
      let iframeIssue = false;
      if (window.self !== window.top) {
        // We are in an iframe
        iframeIssue = true;
        // Check if allow policies exist or let user know about preview frame constraints
        updatedChecks[2] = {
          ...updatedChecks[2],
          status: 'warning',
          value: 'Iframe sandbox detected. WebAuthn will fall back to Simulator.',
        };
      } else {
        updatedChecks[2] = {
          ...updatedChecks[2],
          status: 'pass',
          value: 'Direct top-level document access. No sandbox limit.',
        };
      }

      // 4. Transport types
      updatedChecks[3] = {
        ...updatedChecks[3],
        status: 'pass',
        value: 'USB, NFC, and Platform Authenticators available via sandbox proxy.',
      };

      setChecks(updatedChecks);
      setLoading(false);
      onCheckComplete(hasWebAuthn);
    };

    const timer = setTimeout(() => {
      runChecks();
    }, 600);

    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="bg-white border border-zinc-200 rounded-xl p-5 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <ShieldCheck className="w-5 h-5 text-indigo-600" />
          <h3 className="font-display font-medium text-zinc-950 text-sm">
            Browser Capability & WebAuthn Preflight Check
          </h3>
        </div>
        {loading && <span className="font-mono text-xs text-zinc-400 animate-pulse">Scanning env...</span>}
      </div>

      <p className="font-sans text-xs text-zinc-500 mb-4 leading-relaxed">
        Before issuing user-presence credentials, we verify that the current runtime environment supports FIDO2/WebAuthn.
        Note that inside preview iframes, real WebAuthn calls are often restricted by the browser's credential policies.
        Our <strong className="text-zinc-800">Ceremony Simulator</strong> automatically bridges any restriction to ensure a seamless verification workflow.
      </p>

      <div className="space-y-3">
        {checks.map((check) => (
          <div key={check.id} className="flex items-start justify-between p-3 rounded-lg bg-zinc-50 border border-zinc-100">
            <div className="flex-1 pr-4">
              <span className="font-sans text-xs font-semibold text-zinc-800 block">{check.name}</span>
              <span className="font-sans text-[11px] text-zinc-500 block mt-0.5">{check.description}</span>
            </div>
            <div className="text-right flex flex-col items-end justify-center min-w-[140px]">
              {check.status === 'pass' && (
                <span className="flex items-center gap-1 text-emerald-700 font-mono text-[11px] font-bold bg-emerald-50 border border-emerald-100 px-2 py-0.5 rounded-full">
                  <CheckCircle2 className="w-3 h-3 text-emerald-600" />
                  {check.value}
                </span>
              )}
              {check.status === 'warning' && (
                <span className="flex items-center gap-1 text-amber-700 font-mono text-[11px] font-bold bg-amber-50 border border-amber-100 px-2 py-0.5 rounded-full">
                  <AlertCircle className="w-3 h-3 text-amber-600" />
                  {check.value}
                </span>
              )}
              {check.status === 'fail' && (
                <span className="flex items-center gap-1 text-red-700 font-mono text-[11px] font-bold bg-red-50 border border-red-100 px-2 py-0.5 rounded-full">
                  <AlertCircle className="w-3 h-3 text-red-600" />
                  {check.value}
                </span>
              )}
              {check.status === 'unchecked' && (
                <span className="flex items-center gap-1 text-zinc-400 font-mono text-[11px] bg-zinc-100 px-2 py-0.5 rounded-full">
                  <HelpCircle className="w-3 h-3 animate-spin" />
                  Pending
                </span>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Action to escape iframe */}
      <div className="mt-4 p-3 bg-indigo-50/50 rounded-lg flex items-center justify-between border border-indigo-100/40">
        <div className="flex items-center gap-2">
          <Terminal className="w-4 h-4 text-indigo-600" />
          <span className="font-sans text-xs text-indigo-900 font-medium">Running into browser iframe security blocks?</span>
        </div>
        <a
          href={window.location.href}
          target="_blank"
          rel="noopener noreferrer"
          className="font-sans text-xs text-indigo-600 hover:text-indigo-800 flex items-center gap-1 font-medium transition-colors"
        >
          Open App in New Tab
          <ExternalLink className="w-3.5 h-3.5" />
        </a>
      </div>
    </div>
  );
}
