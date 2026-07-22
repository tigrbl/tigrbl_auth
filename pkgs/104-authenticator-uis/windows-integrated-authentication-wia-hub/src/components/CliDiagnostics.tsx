/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useRef, useEffect } from 'react';
import { Terminal, Shield, Play, HelpCircle, FileCode } from 'lucide-react';

interface CliDiagnosticsProps {
  currentSpn: string;
  currentDomain: string;
}

interface CommandLine {
  text: string;
  type: 'input' | 'output' | 'error' | 'success';
}

export default function CliDiagnostics({ currentSpn, currentDomain }: CliDiagnosticsProps) {
  const [command, setCommand] = useState('');
  const [history, setHistory] = useState<CommandLine[]>([
    { text: 'WIA Kerberos Diagnostic Terminal (Redacted Security Context)', type: 'output' },
    { text: 'Type "help" to list available enterprise diagnostic utilities.', type: 'output' },
    { text: 'Current Active Domain Context: ' + currentDomain, type: 'output' },
    { text: '', type: 'output' },
  ]);

  const terminalEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    terminalEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [history]);

  const handleCommandSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!command.trim()) return;

    const trimmedCmd = command.trim();
    const newHistory = [...history, { text: `C:\\Users\\Administrator> ${trimmedCmd}`, type: 'input' as const }];

    const args = trimmedCmd.split(' ');
    const baseCmd = args[0].toLowerCase();

    let reply: CommandLine[] = [];

    switch (baseCmd) {
      case 'help':
        reply = [
          { text: 'Available diagnostic commands:', type: 'output' },
          { text: '  nslookup -query=srv _kerberos._tcp   Resolve DNS service mapping records', type: 'output' },
          { text: '  kinit <principal_upn>                Request Initial Ticket Granting Ticket (TGT)', type: 'output' },
          { text: '  klist                                Inspect cached tickets, service accounts, and encryption suites', type: 'output' },
          { text: '  wia-diag --test-spn <spn_value>      Structured security conformance test of target SPN', type: 'output' },
          { text: '  clear                                Clear the terminal diagnostic screen', type: 'output' },
        ];
        break;

      case 'clear':
        setHistory([]);
        setCommand('');
        return;

      case 'nslookup':
        if (trimmedCmd.includes('_kerberos._tcp')) {
          reply = [
            { text: 'Server:  UnicastDNS.corp.internal', type: 'output' },
            { text: 'Address:  10.240.0.1', type: 'output' },
            { text: '', type: 'output' },
            { text: '_kerberos._tcp.' + currentDomain.toLowerCase() + '  SRV service location:', type: 'output' },
            { text: '          priority       = 0', type: 'output' },
            { text: '          weight         = 100', type: 'output' },
            { text: '          port           = 88', type: 'output' },
            { text: '          svr hostname   = dc-01.' + currentDomain.toLowerCase(), type: 'output' },
            { text: 'dc-01.' + currentDomain.toLowerCase() + '     internet address = 10.240.10.15', type: 'output' },
            { text: 'DNS SRV records resolved successfully. KDC routing is correct.', type: 'success' },
          ];
        } else {
          reply = [
            { text: 'DNS query syntax: nslookup -query=srv _kerberos._tcp', type: 'error' },
          ];
        }
        break;

      case 'kinit':
        const upn = args[1] || 'user@' + currentDomain;
        reply = [
          { text: 'Contacting Key Distribution Center (KDC) for realm: ' + currentDomain.toUpperCase() + '...', type: 'output' },
          { text: 'Identity verified. Retrieving TGT ticket mapping...', type: 'output' },
          { text: 'Ticket retrieved successfully. Cached in system token-store.', type: 'success' },
          { text: '[REDACTED] Session Key payload (AES256-CTS-HMAC-SHA1-96)', type: 'output' },
        ];
        break;

      case 'klist':
        reply = [
          { text: 'Credentials cache: System Kerberos Credential Manager API', type: 'output' },
          { text: 'Principal: Administrator@' + currentDomain.toUpperCase(), type: 'output' },
          { text: '', type: 'output' },
          { text: '  #1>  Client: Administrator@' + currentDomain.toUpperCase(), type: 'output' },
          { text: '       Server: krbtgt/' + currentDomain.toUpperCase() + '@' + currentDomain.toUpperCase(), type: 'output' },
          { text: '       KerbTicket Encryption: AES-256-CTS-HMAC-SHA1-96', type: 'output' },
          { text: '       Ticket Flags: 0x40a10000 -> FORWARDABLE, RENEWABLE, INITIAL, PRE-AUTHENT', type: 'output' },
          { text: '       Start Time: ' + new Date().toLocaleString(), type: 'output' },
          { text: '       End Time:   ' + new Date(Date.now() + 36000 * 1000).toLocaleString(), type: 'output' },
          { text: '', type: 'output' },
          { text: '  #2>  Client: Administrator@' + currentDomain.toUpperCase(), type: 'output' },
          { text: '       Server: ' + currentSpn, type: 'output' },
          { text: '       KerbTicket Encryption: AES-256-CTS-HMAC-SHA1-96', type: 'output' },
          { text: '       Ticket Flags: 0x40e10000 -> FORWARDABLE, RENEWABLE, AP-REQ-OK', type: 'output' },
          { text: '       Start Time: ' + new Date().toLocaleString(), type: 'output' },
          { text: '       End Time:   ' + new Date(Date.now() + 36000 * 1000).toLocaleString(), type: 'output' },
          { text: '       [REDACTED] Ciphertext: <VECTORS HIDDEN FOR USER DATA PRIVACY>', type: 'success' },
        ];
        break;

      case 'wia-diag':
        const targetSpn = args[2] || currentSpn;
        reply = [
          { text: '==================================================', type: 'output' },
          { text: '  WINDOWS INTEGRATED AUTH CONFORMANCE REPORT', type: 'output' },
          { text: '==================================================', type: 'output' },
          { text: 'Evaluating Domain Name Context: ' + currentDomain, type: 'output' },
          { text: 'Testing Service Principal Name: ' + targetSpn, type: 'output' },
          { text: 'Client OS Context: Windows 11 Enterprise (Ver 22H2)', type: 'output' },
          { text: '', type: 'output' },
          { text: '  [✓] DNS SRV Record Resolution           : OK', type: 'success' },
          { text: '  [✓] KDC Site-Local Connection (Port 88)  : OK', type: 'success' },
          { text: '  [✓] Cryptographic Forest Trust Mappings : OK', type: 'success' },
          { text: '  [✓] Extended EPA Channel Bindings Checked: OK', type: 'success' },
          { text: '  [✓] Token Replay Counter Check          : OK', type: 'success' },
          { text: '', type: 'success' },
          { text: 'CONFORMANCE VERDICT: PASS (Direct automatic credential mapping fully valid)', type: 'success' },
          { text: '==================================================', type: 'output' },
        ];
        break;

      default:
        reply = [
          { text: `Unknown command "${baseCmd}". Type "help" to see valid commands.`, type: 'error' },
        ];
    }

    setHistory([...newHistory, ...reply]);
    setCommand('');
  };

  return (
    <div id="cli-diagnostics" className="bg-slate-950 rounded-2xl border border-slate-800 shadow-2xl overflow-hidden font-mono text-xs text-emerald-400">
      {/* CLI Header bar */}
      <div className="bg-slate-900 border-b border-slate-800 px-4 py-2.5 flex items-center justify-between text-slate-400">
        <div className="flex items-center gap-2">
          <Terminal className="w-4 h-4 text-emerald-500" />
          <span className="font-semibold text-xs tracking-wider uppercase text-slate-300">WIA Enterprise Command Terminal</span>
        </div>
        <div className="flex items-center gap-1">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
          <span className="text-[10px] text-emerald-500 font-bold uppercase tracking-widest">KDC LINKED</span>
        </div>
      </div>

      {/* Console output area */}
      <div className="p-4 h-72 overflow-y-auto scrollbar-thin select-text space-y-1 bg-slate-950">
        {history.map((line, idx) => (
          <div
            key={idx}
            className={`leading-relaxed break-all ${
              line.type === 'input' ? 'text-white font-semibold' :
              line.type === 'error' ? 'text-rose-400' :
              line.type === 'success' ? 'text-emerald-400 font-semibold' :
              'text-slate-300'
            }`}
          >
            {line.text}
          </div>
        ))}
        <div ref={terminalEndRef} />
      </div>

      {/* CommandLine Entry Input */}
      <form onSubmit={handleCommandSubmit} className="bg-slate-900/40 border-t border-slate-800 p-2 flex items-center gap-2">
        <span className="text-white pl-2">C:\&gt;</span>
        <input
          type="text"
          value={command}
          onChange={(e) => setCommand(e.target.value)}
          placeholder="Type command here (e.g. klist, help)..."
          className="flex-1 bg-transparent border-none text-white outline-none focus:ring-0 placeholder-slate-600 text-xs py-1"
          autoComplete="off"
          autoCorrect="off"
          autoCapitalize="off"
          spellCheck="false"
        />
        <button
          type="submit"
          className="p-1.5 bg-emerald-950/45 text-emerald-400 hover:bg-emerald-900/60 rounded border border-emerald-800 cursor-pointer"
        >
          <Play className="w-3.5 h-3.5" />
        </button>
      </form>
    </div>
  );
}
