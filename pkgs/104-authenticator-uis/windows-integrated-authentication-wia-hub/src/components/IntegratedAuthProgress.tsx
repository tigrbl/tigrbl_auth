/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect } from 'react';
import { Loader2, Server, Laptop, ShieldCheck, Database, Key, X, AlertTriangle } from 'lucide-react';
import { SimConfig, SimMode } from '../types';

interface IntegratedAuthProgressProps {
  simConfig: SimConfig;
  onSuccess: (mappedAccount: string) => void;
  onFailure: (errorCode: SimMode, diagnosticMsg: string) => void;
  onCancel: () => void;
  spn: string;
}

export default function IntegratedAuthProgress({
  simConfig,
  onSuccess,
  onFailure,
  onCancel,
  spn,
}: IntegratedAuthProgressProps) {
  const [step, setStep] = useState<number>(0);
  const [timer, setTimer] = useState<number>(0);
  const [logs, setLogs] = useState<string[]>([]);
  const [showOsPrompt, setShowOsPrompt] = useState<boolean>(false);
  const [osUser, setOsUser] = useState<string>('');
  const [osPass, setOsPass] = useState<string>('');
  const [osPromptError, setOsPromptError] = useState<string>('');

  const activeMode = simConfig.activeMode;

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (!showOsPrompt) {
      interval = setInterval(() => {
        setTimer((t) => {
          if (t >= 100) {
            clearInterval(interval);
            return 100;
          }
          return t + 2.5; // bounded time simulation
        });
      }, 50 + simConfig.networkLatencyMs / 10);
    }
    return () => clearInterval(interval);
  }, [showOsPrompt, simConfig.networkLatencyMs]);

  // Handle steps and triggers based on simulated configuration
  useEffect(() => {
    const addLog = (msg: string) => {
      setLogs((prev) => [...prev, `[${new Date().toLocaleTimeString()}] ${msg}`]);
    };

    if (showOsPrompt) return;

    if (timer === 0) {
      addLog('Initiating SPN resolution for audience...');
      addLog(`Target SPN configured: ${spn}`);
      setStep(0);
    } else if (timer > 10 && timer <= 30 && step === 0) {
      addLog('Resolving browser zone and managed policy configurations...');
      if (simConfig.browserType === 'Safari_Private' || simConfig.browserType === 'Firefox_Unmanaged') {
        addLog('Policy warning: Host is not placed within trusted Intranet zone.');
      } else {
        addLog('Active Directory site-local zone confirmed.');
      }
      setStep(1);
    } else if (timer > 30 && timer <= 55 && step === 1) {
      addLog('Client attempting negotiate packet sequence (Negotiate/Kerberos/NTLM)...');
      addLog('Sending GET /api/authenticate with empty Authorization header...');
      addLog('Server returned 401 Unauthorized with Header: WWW-Authenticate: Negotiate');

      if (activeMode === 'proxy_stripped') {
        setTimeout(() => {
          onFailure('proxy_stripped', 'The HTTP Proxy stripped the WWW-Authenticate/Authorization headers in transit.');
        }, 1200);
        return;
      }
      setStep(2);
    } else if (timer > 55 && timer <= 80 && step === 2) {
      addLog('Contacting KDC (Key Distribution Center) for service ticket...');
      if (!simConfig.isCorpNetwork) {
        addLog('Network Error: Local KDC server is unreachable from external net.');
        setTimeout(() => {
          onFailure('unmanaged_device', 'The workstation is currently operating on an unmanaged or external network.');
        }, 1200);
        return;
      }

      if (activeMode === 'clock_skew') {
        addLog('KDC Error: Clock drift detected between workstation and KDC is > 300 seconds.');
        setTimeout(() => {
          onFailure('clock_skew', 'Kerberos Ticket validation failed because of workstation clock drift (skew exceeds 5 minutes).');
        }, 1200);
        return;
      }

      if (activeMode === 'trust_failure') {
        addLog('KDC Warning: Cross-realm trust authentication path broken.');
        setTimeout(() => {
          onFailure('trust_failure', 'Realm domain trust negotiation failed at KDC authentication exchange.');
        }, 1200);
        return;
      }

      if (activeMode === 'spn_failure') {
        addLog('KDC Error: KDC returned KRB_ERR_S_PRINCIPAL_UNKNOWN (Principal unknown).');
        setTimeout(() => {
          onFailure('spn_failure', `Service Principal Name ${spn} could not be resolved or mapped by the KDC.`);
        }, 1200);
        return;
      }

      if (activeMode === 'provider_timeout') {
        addLog('Connecting to Domain Controller... Connection Timeout.');
        setTimeout(() => {
          onFailure('provider_timeout', 'KDC Service provider or Active Directory domain controller timed out responding.');
        }, 1400);
        return;
      }

      if (activeMode === 'success_prompt') {
        addLog('KDC requested explicit interactive user validation.');
        addLog('Opening Windows session prompt...');
        setShowOsPrompt(true);
        return;
      }

      addLog('Client successfully retrieved Kerberos ticket (TGS) from KDC.');
      addLog('Encryption: AES256-CTS-HMAC-SHA1-96');
      setStep(3);
    } else if (timer >= 95 && step === 3) {
      addLog('Submitting base-64 encoded Negotiate Kerberos Token to Web SSO Service...');
      addLog('Authorization: Negotiate YIIFpQYJKoZIhvcSAQICAQB... (truncated)');

      // Process outcomes
      setTimeout(() => {
        switch (activeMode) {
          case 'success_auto':
            addLog('Kerberos ticket validated, token mapped to account: CORP\\j.doe');
            onSuccess('CORP\\j.doe');
            break;
          case 'unsupported_browser':
            onFailure('unsupported_browser', 'Browser does not support Negotiate or is restricted by device Group Policy.');
            break;
          case 'private_mode':
            onFailure('private_mode', 'Windows Integrated Authentication is blocked in Private/Incognito windows to prevent device tracking.');
            break;
          case 'domain_mismatch':
            onFailure('domain_mismatch', 'Workstation Active Directory Domain is not a verified or trusted tenant realm.');
            break;
          case 'ambiguous_mapping':
            onFailure('ambiguous_mapping', 'Multiple accounts match this workstation Security Identifier. Ambiguity resolution required.');
            break;
          case 'account_denied':
            onFailure('account_denied', 'Active Directory Account is disabled, expired, or locked out.');
            break;
          case 'credential_replay':
            onFailure('credential_replay', 'The authentication handshake was blocked due to an anti-replay token validation match.');
            break;
          default:
            onSuccess('CORP\\j.doe');
            break;
        }
      }, 800);
    }
  }, [timer, step, activeMode, simConfig, onSuccess, onFailure, spn, showOsPrompt]);

  const handleOsPromptSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!osUser || !osPass) {
      setOsPromptError('Please enter both domain username and password.');
      return;
    }

    if (simConfig.simulatePromptCancellation) {
      setOsPromptError('Windows Security: Authentication attempt cancelled by user.');
      return;
    }

    if (osUser.toLowerCase().includes('fail') || osPass === 'wrong') {
      setOsPromptError('Incorrect credentials or domain account locked.');
      return;
    }

    setLogs((prev) => [...prev, `[${new Date().toLocaleTimeString()}] OS prompt credentials verified. Resuming ceremony.`]);
    setShowOsPrompt(false);
    setTimer(85);
    setStep(3);
  };

  const handleOsPromptCancel = () => {
    setShowOsPrompt(false);
    onCancel();
  };

  return (
    <div id="integrated-auth-progress" className="w-full max-w-md bg-white rounded-2xl border border-slate-200 shadow-xl overflow-hidden relative">
      {/* OS Mock Credential Prompt overlay */}
      {showOsPrompt && (
        <div className="absolute inset-0 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-6 z-50">
          <div className="bg-[#f0f4f9] text-slate-800 rounded-lg shadow-2xl border border-slate-300 w-full max-w-xs overflow-hidden text-sm">
            <div className="bg-[#1d4ed8] text-white px-4 py-3 flex items-center justify-between">
              <span className="font-semibold text-xs tracking-tight flex items-center gap-1.5">
                <Laptop className="w-3.5 h-3.5" /> Windows Security
              </span>
              <button onClick={handleOsPromptCancel} className="text-white/80 hover:text-white cursor-pointer">
                <X className="w-4 h-4" />
              </button>
            </div>
            <form onSubmit={handleOsPromptSubmit} className="p-4 space-y-4">
              <div className="text-center pb-2">
                <p className="font-medium text-xs text-slate-800">Connecting to {spn}</p>
                <p className="text-[11px] text-slate-500">Enter your credentials to connect to your corporate network.</p>
              </div>

              {osPromptError && (
                <div className="p-2 bg-red-50 border border-red-200 rounded text-[11px] text-red-700 flex gap-1.5">
                  <AlertTriangle className="w-4 h-4 shrink-0 text-red-600" />
                  <span>{osPromptError}</span>
                </div>
              )}

              <div className="space-y-3">
                <div>
                  <label htmlFor="os-user" className="block text-[11px] font-medium text-slate-600 mb-1">Username (e.g. DOMAIN\username)</label>
                  <input
                    type="text"
                    id="os-user"
                    placeholder="CORP\username"
                    value={osUser}
                    onChange={(e) => setOsUser(e.target.value)}
                    className="w-full px-2 py-1.5 text-xs rounded border border-slate-300 bg-white outline-none focus:border-blue-500"
                  />
                </div>
                <div>
                  <label htmlFor="os-pass" className="block text-[11px] font-medium text-slate-600 mb-1">Password</label>
                  <input
                    type="password"
                    id="os-pass"
                    placeholder="••••••••"
                    value={osPass}
                    onChange={(e) => setOsPass(e.target.value)}
                    className="w-full px-2 py-1.5 text-xs rounded border border-slate-300 bg-white outline-none focus:border-blue-500"
                  />
                </div>
              </div>

              <div className="flex gap-2 justify-end pt-2">
                <button
                  type="submit"
                  className="px-4 py-1.5 bg-[#1d4ed8] hover:bg-blue-700 text-white rounded text-xs font-semibold cursor-pointer"
                >
                  OK
                </button>
                <button
                  type="button"
                  onClick={handleOsPromptCancel}
                  className="px-4 py-1.5 bg-slate-200 hover:bg-slate-300 text-slate-800 rounded text-xs cursor-pointer border border-slate-300"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Main progress body */}
      <div className="p-6 space-y-6">
        <div className="flex items-center justify-between border-b border-slate-100 pb-4">
          <div>
            <h3 className="font-display font-semibold text-slate-800 text-lg">Negotiate Handshake</h3>
            <p className="text-xs text-slate-400">AMR Method: wia (Kerberos-Negotiate)</p>
          </div>
          <div className="flex items-center gap-1 bg-blue-50 px-2 py-1 rounded text-[10px] font-mono text-blue-700">
            <Loader2 className="w-3 h-3 animate-spin text-blue-600" />
            <span>{(timer).toFixed(0)}%</span>
          </div>
        </div>

        {/* Visual Handshake Diagram */}
        <div className="bg-slate-50 border border-slate-200/60 rounded-xl p-4">
          <h4 className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider mb-4">Handshake Pipeline</h4>
          <div className="grid grid-cols-3 gap-2 relative">
            {/* Visual connector lines */}
            <div className="absolute top-5 left-1/6 right-1/6 h-[2px] bg-slate-200 -z-0">
              <div
                className="h-full bg-blue-500 transition-all duration-300"
                style={{ width: `${step === 0 ? '0%' : step === 1 ? '30%' : step === 2 ? '65%' : '100%'}` }}
              ></div>
            </div>

            {/* Client Workstation node */}
            <div className="flex flex-col items-center text-center z-10">
              <div className={`w-10 h-10 rounded-full flex items-center justify-center transition-all ${step >= 0 ? 'bg-blue-600 text-white ring-4 ring-blue-100' : 'bg-slate-200 text-slate-500'}`}>
                <Laptop className="w-5 h-5" />
              </div>
              <span className="text-[11px] font-medium text-slate-700 mt-2">Workstation</span>
              <span className="text-[9px] text-slate-400 font-mono">Client</span>
            </div>

            {/* Active Directory KDC node */}
            <div className="flex flex-col items-center text-center z-10">
              <div className={`w-10 h-10 rounded-full flex items-center justify-center transition-all ${step >= 2 ? 'bg-blue-600 text-white ring-4 ring-blue-100' : 'bg-slate-200 text-slate-500'}`}>
                <Key className="w-5 h-5" />
              </div>
              <span className="text-[11px] font-medium text-slate-700 mt-2">KDC (AD Realm)</span>
              <span className="text-[9px] text-slate-400 font-mono">Kerberos</span>
            </div>

            {/* SSO Web Gateway */}
            <div className="flex flex-col items-center text-center z-10">
              <div className={`w-10 h-10 rounded-full flex items-center justify-center transition-all ${step >= 3 ? 'bg-blue-600 text-white ring-4 ring-blue-100' : 'bg-slate-200 text-slate-500'}`}>
                <Server className="w-5 h-5" />
              </div>
              <span className="text-[11px] font-medium text-slate-700 mt-2">Web SSO</span>
              <span className="text-[9px] text-slate-400 font-mono">SSO Gateway</span>
            </div>
          </div>
        </div>

        {/* Console / Handshake log */}
        <div className="space-y-2">
          <div className="flex justify-between items-center">
            <span className="text-xs font-semibold text-slate-600 uppercase tracking-wider">Ceremony Log</span>
            <span className="text-[10px] text-slate-400 font-mono">Bound to SPN: {spn}</span>
          </div>
          <div className="h-32 rounded-lg bg-slate-950 p-3 overflow-y-auto font-mono text-[10px] text-slate-300 space-y-1.5 scrollbar-thin">
            {logs.map((log, i) => (
              <div key={i} className="leading-normal break-all">
                <span className="text-slate-500">&gt; </span>
                {log}
              </div>
            ))}
          </div>
        </div>

        {/* Bounded action fallback buttons */}
        <div className="space-y-3 pt-2">
          <div className="text-center">
            <p className="text-[11px] text-slate-400">Negotiate token processing is automatically bounded by a security timeout check.</p>
          </div>
          <div className="flex gap-3">
            <button
              onClick={onCancel}
              className="flex-1 py-2.5 px-4 border border-slate-200 hover:bg-slate-50 text-slate-700 font-medium text-xs rounded-lg transition-colors cursor-pointer text-center"
            >
              Use another method
            </button>
            <button
              onClick={onCancel}
              className="py-2.5 px-4 bg-slate-100 hover:bg-slate-200 text-slate-600 font-medium text-xs rounded-lg transition-colors cursor-pointer text-center"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
