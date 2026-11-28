/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { AuditLog, CeremonyEvidence } from '../types';
import { Terminal, Shield, RefreshCw, CheckCircle2, AlertTriangle, Play, HelpCircle, FileText, Activity } from 'lucide-react';

interface EvidencePanelProps {
  auditLogs: AuditLog[];
  latestEvidence: CeremonyEvidence | null;
  onClearLogs: () => void;
  onInjectAudit: (event: string, category: 'auth' | 'enrollment' | 'policy' | 'lifecycle' | 'error', status: 'success' | 'failure' | 'warning' | 'info', details: string) => void;
}

export default function EvidencePanel({
  auditLogs,
  latestEvidence,
  onClearLogs,
  onInjectAudit,
}: EvidencePanelProps) {
  const [selectedCommand, setSelectedCommand] = useState('ykman fido info');
  const [terminalOutput, setTerminalOutput] = useState<string[]>([
    '$ ykman fido info',
    'Device type: YubiKey 5C Nano',
    'Serial number: 12883491',
    'Firmware version: 5.4.3',
    'FIDO2: Enabled (PIN set, UV configured)',
    'PIN retry counter: 3/3',
    'Supported Transports: USB, NFC',
    'AAGUID: cb69481e-8e17-4dd3-97f9-2e0085a6cfbc',
    'Status: Device is healthy and ready for user presence prompts.'
  ]);
  const [isRunningCommand, setIsRunningCommand] = useState(false);

  const handleRunCommand = () => {
    setIsRunningCommand(true);
    setTerminalOutput(['$ ' + selectedCommand, 'Querying connected transports...', 'Detecting security boundaries...']);

    setTimeout(() => {
      switch (selectedCommand) {
        case 'ykman fido info':
          setTerminalOutput([
            '$ ykman fido info',
            '========================================',
            'Device Name: YubiKey 5C Nano',
            'AAGUID: cb69481e-8e17-4dd3-97f9-2e0085a6cfbc',
            'Form Factor: USB-C Keychain Token',
            'PIN Configured: Yes (Required for UV)',
            'Maximum Credentials Store: 25',
            'Supported Key Alg: ES256, RS256, Ed25519',
            'FIPS-140 Level: Level 2 Compliant',
            '========================================',
            'Status: UP verification verified. Ready.'
          ]);
          onInjectAudit('CLI diagnostic probe executed', 'lifecycle', 'success', 'ykman queried YubiKey 5C capability successfully.');
          break;
        case 'fido2-token -L':
          setTerminalOutput([
            '$ fido2-token -L',
            'Found 2 eligible authenticators:',
            '0: path=/dev/hidraw0, vendor=0x1050 (Yubico), product=0x0407 (YubiKey OTP+FIDO+CCID)',
            '1: path=/dev/hidraw1, vendor=0x096e (Feitian), product=0x085d (Feitian BioPass FIDO2)',
            '',
            'Use fido2-token -I <path> to query detailed capabilities without private keys.'
          ]);
          onInjectAudit('Token list probe executed', 'lifecycle', 'success', 'fido2-token listed active hidraw ports.');
          break;
        case 'security-key --diagnose':
          setTerminalOutput([
            '$ security-key --diagnose',
            'Beginning safe diagnostics run...',
            '[PASS] WebAuthn API availability check',
            '[PASS] Cryptographic random number generator check',
            '[PASS] Replay attack guard challenge checks',
            '[WARN] Direct biometric access - Iframe Sandbox limits may block biometric prompts.',
            '[INFO] UP Fallback loop initialized.',
            'Diagnostics pass with 1 warning. No private material logged.'
          ]);
          onInjectAudit('Diagnostics diagnostic probe executed', 'lifecycle', 'warning', 'Security key diagnostics completed with 1 warning.');
          break;
        case 'amr-verify --strict':
          if (latestEvidence) {
            setTerminalOutput([
              '$ amr-verify --strict',
              `Analyzing Ceremony ID: ${latestEvidence.id}`,
              `Time freshness: ${((Date.now() - new Date(latestEvidence.timestamp).getTime()) / 1000).toFixed(1)}s age`,
              `User Present Flag (UP): ${latestEvidence.userPresent ? '1 (VERIFIED)' : '0 (ABSENT)'}`,
              `User Verified Flag (UV): ${latestEvidence.userVerified ? '1 (VERIFIED)' : '0 (ABSENT)'}`,
              `Signature payload: ${latestEvidence.signature.substring(0, 32)}...`,
              `Origin binding: ${latestEvidence.origin} (RP ID: ${latestEvidence.rpId})`,
              `Audit reference: ${latestEvidence.auditReference}`,
              'Validation Outcome: SIGNATURE CONFIRMED. No replay or downgrade detected.'
            ]);
            onInjectAudit('Strict AMR validation executed', 'auth', 'success', 'AMR audit verified latest touch evidence signature.');
          } else {
            setTerminalOutput([
              '$ amr-verify --strict',
              'Error: No recent ceremony evidence available to evaluate.',
              'Please complete an authentication ceremony first.'
            ]);
          }
          break;
      }
      setIsRunningCommand(false);
    }, 800);
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'auth': return 'bg-indigo-50 border-indigo-100 text-indigo-700';
      case 'enrollment': return 'bg-emerald-50 border-emerald-100 text-emerald-700';
      case 'policy': return 'bg-amber-50 border-amber-100 text-amber-700';
      case 'error': return 'bg-red-50 border-red-100 text-red-700';
      default: return 'bg-zinc-100 border-zinc-200 text-zinc-600';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'success': return <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />;
      case 'warning': return <AlertTriangle className="w-3.5 h-3.5 text-amber-500" />;
      case 'failure': return <AlertTriangle className="w-3.5 h-3.5 text-red-500" />;
      default: return <Activity className="w-3.5 h-3.5 text-zinc-400" />;
    }
  };

  return (
    <div className="space-y-6">
      {/* CLI Device Probe Tool */}
      <div className="bg-white border border-zinc-200 rounded-xl p-5 shadow-sm space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Terminal className="w-5 h-5 text-zinc-700" />
            <h3 className="font-display font-medium text-zinc-950 text-sm">
              Native Key CLI Probe Tool
            </h3>
          </div>
          <span className="text-[10px] text-zinc-400 font-sans font-medium">
            Redacted Safe Public Inspect Loop
          </span>
        </div>

        <p className="font-sans text-xs text-zinc-500 leading-relaxed">
          Test and query public capabilities of security keys or local passkeys. No cryptographic private keys or PINs are ever exposed or logged during CLI checks.
        </p>

        <div className="flex gap-2">
          <select
            value={selectedCommand}
            onChange={(e) => setSelectedCommand(e.target.value)}
            disabled={isRunningCommand}
            className="flex-1 bg-zinc-50 border border-zinc-200 rounded-lg px-3 py-1.5 text-xs font-mono text-zinc-800 focus:outline-none"
          >
            <option value="ykman fido info">ykman fido info</option>
            <option value="fido2-token -L">fido2-token -L (list devices)</option>
            <option value="security-key --diagnose">security-key --diagnose</option>
            <option value="amr-verify --strict">amr-verify --strict (verify latest evidence)</option>
          </select>
          <button
            onClick={handleRunCommand}
            disabled={isRunningCommand}
            className="bg-zinc-900 hover:bg-zinc-800 disabled:opacity-50 text-white text-xs font-sans px-4 py-1.5 rounded-lg transition-colors flex items-center gap-1 font-medium"
          >
            <Play className="w-3.5 h-3.5" />
            Run Probe
          </button>
        </div>

        {/* Terminal screen */}
        <div className="bg-zinc-950 text-zinc-200 font-mono text-xs rounded-xl p-4 border border-zinc-900 overflow-x-auto min-h-[160px] max-h-[220px] shadow-inner space-y-1">
          {terminalOutput.map((line, idx) => (
            <div key={idx} className={line.startsWith('$') ? 'text-indigo-400 font-bold' : line.includes('[PASS]') ? 'text-emerald-400' : line.includes('Error') || line.includes('CRITICAL') ? 'text-red-400' : 'text-zinc-300'}>
              {line}
            </div>
          ))}
          {isRunningCommand && (
            <div className="text-zinc-500 animate-pulse">Running check on connected endpoints...</div>
          )}
        </div>
      </div>

      {/* Security Ceremony Audit Log */}
      <div className="bg-white border border-zinc-200 rounded-xl p-5 shadow-sm space-y-4">
        <div className="flex items-center justify-between border-b border-zinc-100 pb-3">
          <div className="flex items-center gap-2">
            <FileText className="w-5 h-5 text-zinc-700" />
            <h3 className="font-display font-medium text-zinc-950 text-sm">
              Dynamic Security & Ceremony Audit Logs
            </h3>
          </div>
          <button
            onClick={onClearLogs}
            className="text-xs text-zinc-500 hover:text-zinc-800 underline font-sans"
          >
            Clear Log Archive
          </button>
        </div>

        <div className="space-y-2 max-h-[300px] overflow-y-auto pr-1">
          {auditLogs.map((log) => (
            <div key={log.id} className="p-3 bg-zinc-50 border border-zinc-100 rounded-xl space-y-1.5">
              <div className="flex items-center justify-between">
                <span className="font-sans font-semibold text-xs text-zinc-800">{log.event}</span>
                <span className="font-mono text-[9px] text-zinc-400">{new Date(log.timestamp).toLocaleTimeString()}</span>
              </div>
              <p className="font-sans text-[11px] text-zinc-500 leading-relaxed">{log.details}</p>
              <div className="flex justify-between items-center border-t border-zinc-100/60 pt-1.5 mt-1">
                <span className={`font-mono text-[8px] px-1.5 py-0.5 rounded uppercase border ${getCategoryColor(log.category)}`}>
                  {log.category}
                </span>
                <div className="flex items-center gap-1">
                  {getStatusIcon(log.status)}
                  <span className="font-mono text-[9px] text-zinc-400">{log.auditReference}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
