import React, { useState, useRef, useEffect } from 'react';
import { SmartCard } from '../types';
import { Terminal, Shield, RefreshCw } from 'lucide-react';

interface CliDiagnosticsProps {
  cards: SmartCard[];
  readerConnected: boolean;
  selectedReaderName: string;
}

export const CliDiagnostics: React.FC<CliDiagnosticsProps> = ({
  cards,
  readerConnected,
  selectedReaderName,
}) => {
  const [history, setHistory] = useState<string[]>([
    'Initializing Smart Card CLI Diagnostic Interface v1.1.2...',
    'Operating System PKCS#11 / CryptoAPI Bridge: OK',
    'Type "help" to list available diagnostic instructions.',
    '',
  ]);
  const [inputVal, setInputVal] = useState('');
  const terminalEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    terminalEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [history]);

  const handleCommandSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const command = inputVal.trim();
    if (!command) return;

    const lowerCmd = command.toLowerCase();
    const newLines = [`$ ${command}`];

    if (lowerCmd === 'help') {
      newLines.push(
        'Available Smart-Card Diagnostic Commands:',
        '  sc-diag --list-readers      List all connected physical hardware CCID reader interfaces.',
        '  sc-diag --list-certs        Enumerate and project public certificate data visible in the PKCS#11 slots.',
        '  sc-diag --verify-chain [id] Construct and verify path trust chain up to registered Federal Root CA.',
        '  sc-diag --ocsp-check [id]   Contact real-time CRL/OCSP responders to verify card revocation status.',
        '  clear                       Clear the current screen buffer.',
        '  help                        Display this assistance matrix.'
      );
    } else if (lowerCmd === 'clear') {
      setHistory([]);
      setInputVal('');
      return;
    } else if (lowerCmd === 'sc-diag --list-readers' || lowerCmd === 'sc-diag -lr') {
      if (readerConnected) {
        newLines.push(
          'Found 1 active smart-card reader interface:',
          `  Slot [0]: ${selectedReaderName}`,
          '  Status: ACTIVE (Contact lines established)',
          '  Driver: PKCS#11 Generic CCID v2.4.0'
        );
      } else {
        newLines.push(
          'Searching local USB CCID interfaces...',
          '  [WARNING] No active smart card readers detected. Make sure your USB bus is polling.'
        );
      }
    } else if (lowerCmd === 'sc-diag --list-certs' || lowerCmd === 'sc-diag -lc') {
      newLines.push(`Discovered ${cards.length} certificate mappings across reader slots:`);
      cards.forEach((card, idx) => {
        newLines.push(
          `  [${idx + 1}] Label: ${card.label}`,
          `      Subject: ${card.subject.split(',')[0]}`,
          `      Serial:  ${card.serialNumber}`,
          `      EKU:     ${card.eku.join(', ')}`,
          `      Status:  ${card.status.toUpperCase()}`,
          ''
        );
      });
    } else if (lowerCmd.startsWith('sc-diag --verify-chain') || lowerCmd.startsWith('sc-diag -vc')) {
      const parts = command.split(' ');
      const targetArg = parts[2];
      const idx = parseInt(targetArg, 10) - 1;

      if (isNaN(idx) || idx < 0 || idx >= cards.length) {
        newLines.push(
          'Error: Invalid cert index. Specify slot index (e.g., "sc-diag --verify-chain 1")',
          'Use "sc-diag --list-certs" to check slot mapping numbers.'
        );
      } else {
        const card = cards[idx];
        newLines.push(
          `Constructing certificate path for Slot [${idx + 1}]...`,
          `  Target: ${card.subject.split(',')[0]}`,
          `  Issuer: ${card.issuer.split(',')[0]}`,
          '  Searching trust anchor authorities...'
        );

        if (card.status === 'expired') {
          newLines.push(
            '  [FAIL] Trust path evaluation breached.',
            `  Root Cause: Certificate validity boundary check failed (Expired on ${card.notAfter})`
          );
        } else if (card.eku.length === 1 && card.eku[0].includes('Secure Email')) {
          newLines.push(
            '  [FAIL] EKU profile rule mapping rejected.',
            '  Root Cause: Missing required OID: Client Authentication (1.3.6.1.5.5.7.3.2)'
          );
        } else {
          newLines.push(
            '  [PASS] Path construction completed.',
            '  Verified Issuer: Federal Common Policy CA G2 (FIPS-Compliant Root Anchor SHA-256)'
          );
        }
      }
    } else if (lowerCmd.startsWith('sc-diag --ocsp-check') || lowerCmd.startsWith('sc-diag -oc')) {
      const parts = command.split(' ');
      const targetArg = parts[2];
      const idx = parseInt(targetArg, 10) - 1;

      if (isNaN(idx) || idx < 0 || idx >= cards.length) {
        newLines.push(
          'Error: Invalid cert index. Specify slot index (e.g., "sc-diag --ocsp-check 1")',
          'Use "sc-diag --list-certs" to check slot mapping numbers.'
        );
      } else {
        const card = cards[idx];
        newLines.push(
          `Contacting real-time validation responder for Serial [${card.serialNumber}]...`,
          `  Responder: http://ocsp.disa.mil`,
          '  Querying CRL maps & OCSP signature validity...'
        );

        if (card.status === 'revoked') {
          newLines.push(
            '  [REVOKED] Status returned negative from FPKI authority.',
            '  Reason code: KeyCompromise / Unauthorized access privilege'
          );
        } else {
          newLines.push(
            '  [PASS] Responder signed affirmative status.',
            `  Status: ACTIVE (Nonce match verified, latency 12ms)`
          );
        }
      }
    } else {
      newLines.push(
        `Command not found: "${command}".`,
        'Type "help" to view list of active diagnostic scripts.'
      );
    }

    setHistory(prev => [...prev, ...newLines, '']);
    setInputVal('');
  };

  return (
    <div className="bg-slate-950 rounded-xl overflow-hidden shadow-lg border border-slate-800 flex flex-col h-[320px]" id="cli-console">
      {/* Console Header */}
      <div className="bg-slate-900 border-b border-slate-800 px-4 py-2.5 flex items-center justify-between select-none">
        <div className="flex items-center gap-2 text-slate-400">
          <Terminal className="w-4 h-4 text-indigo-400" />
          <span className="font-mono text-xs font-semibold text-slate-300">Smart-Card Diagnostic Shell (sc-diag)</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="text-[10px] font-mono text-slate-500">PKCS#11 Secure Socket Mode</span>
          <Shield className="w-3.5 h-3.5 text-indigo-500" />
        </div>
      </div>

      {/* Terminal Screen Buffer */}
      <div className="flex-1 overflow-y-auto p-4 font-mono text-xs text-indigo-300 space-y-1.5 scrollbar-thin scrollbar-thumb-slate-800">
        {history.map((line, idx) => (
          <div key={idx} className="whitespace-pre-wrap leading-relaxed">
            {line}
          </div>
        ))}
        <div ref={terminalEndRef} />
      </div>

      {/* Console Input */}
      <form onSubmit={handleCommandSubmit} className="bg-slate-900 border-t border-slate-800 px-4 py-2 flex items-center gap-2">
        <span className="font-mono text-xs text-indigo-400 select-none">$</span>
        <input
          type="text"
          value={inputVal}
          onChange={(e) => setInputVal(e.target.value)}
          placeholder="Type command (e.g. sc-diag --list-certs, help)..."
          className="flex-1 bg-transparent font-mono text-xs text-white border-none focus:outline-none focus:ring-0 placeholder-slate-600"
          id="input-terminal-cmd"
          autoComplete="off"
        />
        <button
          type="submit"
          className="px-2.5 py-1 bg-indigo-600 hover:bg-indigo-700 text-white rounded text-[10px] font-bold font-mono transition-colors"
          id="btn-submit-terminal-cmd"
        >
          Execute
        </button>
      </form>
    </div>
  );
};
