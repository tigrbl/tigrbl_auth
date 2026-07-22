import React, { useState } from 'react';
import { Terminal, Copy, Check, Code, Play, RefreshCw, Cpu } from 'lucide-react';

export default function CliTooling() {
  const [activeTab, setActiveTab] = useState<'cli' | 'nodejs' | 'python'>('cli');
  const [selectedCommand, setSelectedCommand] = useState<'gen' | 'sign' | 'rotate' | 'status'>('gen');
  const [terminalOutput, setTerminalOutput] = useState<string>('Run a command to see output...');
  const [running, setRunning] = useState(false);
  const [copiedCode, setCopiedCode] = useState(false);

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedCode(true);
    setTimeout(() => setCopiedCode(false), 2000);
  };

  const executeCliCommand = () => {
    setRunning(true);
    setTerminalOutput('Executing cryptographic command...');

    setTimeout(() => {
      setRunning(false);
      const now = new Date().toISOString();
      const kid = `swk-${Math.floor(Math.random() * 900000 + 100000)}`;

      switch (selectedCommand) {
        case 'gen':
          setTerminalOutput(
`$ swk gen --profile dpop --store macos_keychain --name user_session_key
[info] Initializing CryptoKit software-secured keypair creation...
[info] Keystore context: Apple Keystore Services
[info] Generating prime numbers... bound validation complete.
[info] Export blocked: true
[info] Public JWK registered with Server: OK
[info] Requesting server possession proof challenge...
[info] Possession challenge received: nonce-789456
[info] Signed proof assertion with local key.
[info] Server attestation verify: OK (classification: software_secured)
[info] Credential fully activated.
----------------------------------------------------------------------
Key ID (kid) : ${kid}
Fingerprint  : SHA256:7uGvK9x...[${Math.random().toString(36).substring(4, 10)}]
Storage Class: software_secured (Verified AMR: swk)
Timestamp    : ${now}
Status       : active`
          );
          break;

        case 'sign':
          setTerminalOutput(
`$ swk sign --key ${kid} --nonce challenge-9922 --audience https://api.internal/
[info] Reading local key descriptor for ${kid}
[info] Querying macOS Keystore context...
[info] Prompting native system user authorization...
[info] Keystore authorization: SUCCESS (Authorized OK)
[info] Signing SHA256 hash bound to audience and nonce...
[info] Created proof assertion block.
----------------------------------------------------------------------
{
  "alg": "ES256",
  "kid": "${kid}",
  "typ": "dpop+jwt"
}
.
{
  "jti": "jti-random-9912234",
  "htm": "POST",
  "htu": "https://api.internal/",
  "iat": 1784112345,
  "nonce": "challenge-9922"
}
.
[signature: 64_bytes_crypto_material_redacted]
----------------------------------------------------------------------
Proof Assertion generated successfully.`
          );
          break;

        case 'rotate':
          setTerminalOutput(
`$ swk rotate --key ${kid} --new-name user_session_key_v2
[info] Initializing overlapping key rotation...
[info] Step 1: Created overlap key ${kid}-v2 in Approved OS Keystore.
[info] Step 2: Registered public JWK set on server.
[info] Step 3: Server issued challenge-response possession proof.
[info] Step 4: Proved possession of new private key: verified OK.
[info] Step 5: Commencing traffic verification... verified 100% traffic.
[info] Step 6: Deprecated and explicitly retired original key ${kid}.
----------------------------------------------------------------------
Rotation Complete. Original key ${kid} is now REVOKED.
Replacement key ${kid}-v2 is now ACTIVE.`
          );
          break;

        case 'status':
          setTerminalOutput(
`$ swk status --key ${kid}
----------------------------------------------------------------------
KEY DETAIL REPORT:
----------------------------------------------------------------------
Key ID        : ${kid}
Alias         : user_session_key
Algorithm     : ES256
Storage Class : software_secured
Verified Evid : YES (swk AMR certified)
Provider      : macOS Keychain (CryptoKit)
Backup Policy : blocked
Export Policy : blocked
Last Used     : ${now}
Hash Audit    : cb7b3e89a59c362b5d43818e...`
          );
          break;
      }
    }, 600);
  };

  const nodeJsCode = `import { GoogleGenAI } from "@google/genai";
import { SwkClient } from "@swk-secure/sdk-node";

// 1. Initialize the Software-Secured Key Adapter
const swk = new SwkClient({
  keystore: "macos_keychain", // bound to native OS security
  profile: "dpop"
});

// 2. Generate a software-secured key
const key = await swk.generateKey({
  name: "billing_access_token",
  algorithms: ["ES256"]
});

// 3. Generate bound cryptographic signature proofs on-demand
const proof = await swk.signAssertion({
  keyId: key.id,
  challenge: "nonce-992233",
  audience: "https://api.gateway.internal"
});

console.log("Verified AMR Token:", proof.evidenceToken);`;

  const pythonCode = `from swk_secure_sdk import SwkClient, KeyProfile

# 1. Initialize connection to Windows CNG or macOS Keychain
client = SwkClient(
    keystore="native_default",
    profile=KeyProfile.DPOP
)

# 2. Register local software key safely
key = client.generate_key(
    name="payment_signing_key", 
    algorithm="ES256"
)

# 3. Create challenge-response signature assertion
assertion = client.sign_assertion(
    key_id=key.id,
    nonce="server-challenge-xyz",
    audience="https://api.internal"
)

print(f"Generated swk signature: {assertion.signature}")`;

  return (
    <div id="cli-sdk-tooling" className="bg-white border border-slate-200 rounded-xl p-5 space-y-5 shadow-sm">
      <div className="flex items-center justify-between border-b border-slate-100 pb-3">
        <div className="flex items-center gap-2">
          <Terminal className="w-5 h-5 text-slate-700" />
          <h4 className="font-semibold text-slate-800 text-sm">CLI & SDK Developer Tooling</h4>
        </div>
        <div className="flex bg-slate-100 p-0.5 rounded-lg text-xs font-semibold">
          <button
            onClick={() => setActiveTab('cli')}
            id="tab-cli"
            className={`px-3 py-1 rounded-md transition-colors cursor-pointer ${
              activeTab === 'cli' ? 'bg-white shadow text-indigo-700' : 'text-slate-500 hover:text-slate-800'
            }`}
          >
            CLI Emulator
          </button>
          <button
            onClick={() => setActiveTab('nodejs')}
            id="tab-nodejs"
            className={`px-3 py-1 rounded-md transition-colors cursor-pointer ${
              activeTab === 'nodejs' ? 'bg-white shadow text-indigo-700' : 'text-slate-500 hover:text-slate-800'
            }`}
          >
            NodeJS SDK
          </button>
          <button
            onClick={() => setActiveTab('python')}
            id="tab-python"
            className={`px-3 py-1 rounded-md transition-colors cursor-pointer ${
              activeTab === 'python' ? 'bg-white shadow text-indigo-700' : 'text-slate-500 hover:text-slate-800'
            }`}
          >
            Python SDK
          </button>
        </div>
      </div>

      {activeTab === 'cli' && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* CLI Selector Controls */}
          <div className="md:col-span-1 space-y-2 border-r border-slate-100 pr-2">
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wide block mb-1">Select CLI command</span>
            {[
              { id: 'gen', cmd: 'swk gen', desc: 'Create, prove & activate key' },
              { id: 'sign', cmd: 'swk sign', desc: 'Generate bound signature' },
              { id: 'rotate', cmd: 'swk rotate', desc: 'Overlap key replacement' },
              { id: 'status', cmd: 'swk status', desc: 'Inspect key classification' },
            ].map((cmd) => (
              <button
                key={cmd.id}
                id={`btn-cli-${cmd.id}`}
                onClick={() => setSelectedCommand(cmd.id as any)}
                className={`w-full text-left p-2.5 rounded-lg border text-xs transition-all cursor-pointer ${
                  selectedCommand === cmd.id
                    ? 'bg-indigo-50 border-indigo-400 text-indigo-800 shadow-sm'
                    : 'bg-white border-slate-200 hover:bg-slate-50 text-slate-600'
                }`}
              >
                <div className="font-mono font-semibold">{cmd.cmd}</div>
                <div className="text-[10px] text-slate-400 mt-0.5">{cmd.desc}</div>
              </button>
            ))}

            <button
              onClick={executeCliCommand}
              id="btn-run-cli"
              disabled={running}
              className="w-full mt-3 bg-slate-900 hover:bg-slate-800 text-white font-semibold py-2 rounded-lg text-xs flex items-center justify-center gap-1.5 transition-colors cursor-pointer shadow disabled:opacity-50"
            >
              {running ? (
                <>
                  <RefreshCw className="w-3.5 h-3.5 animate-spin" /> Running...
                </>
              ) : (
                <>
                  <Play className="w-3.5 h-3.5 text-indigo-400" /> Run Command
                </>
              )}
            </button>
          </div>

          {/* Terminal Box */}
          <div className="md:col-span-2 flex flex-col bg-slate-950 text-slate-300 font-mono text-[11px] rounded-xl border border-slate-900 overflow-hidden shadow-inner h-[250px]">
            <div className="bg-slate-900/80 px-3 py-1.5 border-b border-slate-950 flex items-center justify-between shrink-0">
              <div className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-rose-500" />
                <span className="w-2.5 h-2.5 rounded-full bg-amber-500" />
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
                <span className="text-[10px] text-slate-400 font-bold ml-1.5">CLI Terminal Emulator</span>
              </div>
              <button
                onClick={() => copyToClipboard(terminalOutput)}
                className="text-slate-400 hover:text-slate-200 transition-colors"
                title="Copy Terminal Output"
              >
                <Copy className="w-3.5 h-3.5" />
              </button>
            </div>
            <pre className="p-3 overflow-y-auto flex-1 leading-relaxed whitespace-pre-wrap select-all selection:bg-indigo-600">
              {terminalOutput}
            </pre>
          </div>
        </div>
      )}

      {activeTab === 'nodejs' && (
        <div className="space-y-3">
          <div className="flex items-center justify-between text-xs text-slate-500">
            <span>First-party Node SDK Integration example</span>
            <button
              onClick={() => copyToClipboard(nodeJsCode)}
              id="btn-copy-nodejs"
              className="text-indigo-600 hover:text-indigo-800 flex items-center gap-1 font-semibold p-1"
            >
              {copiedCode ? (
                <>
                  <Check className="w-3.5 h-3.5 text-emerald-600" /> Copied!
                </>
              ) : (
                <>
                  <Copy className="w-3.5 h-3.5" /> Copy Code
                </>
              )}
            </button>
          </div>
          <div className="relative">
            <pre className="p-4 bg-slate-900 text-slate-200 rounded-xl font-mono text-xs leading-relaxed overflow-x-auto border border-slate-800 max-h-[220px] overflow-y-auto">
              {nodeJsCode}
            </pre>
          </div>
        </div>
      )}

      {activeTab === 'python' && (
        <div className="space-y-3">
          <div className="flex items-center justify-between text-xs text-slate-500">
            <span>First-party Python SDK Wrapper example</span>
            <button
              onClick={() => copyToClipboard(pythonCode)}
              id="btn-copy-python"
              className="text-indigo-600 hover:text-indigo-800 flex items-center gap-1 font-semibold p-1"
            >
              {copiedCode ? (
                <>
                  <Check className="w-3.5 h-3.5 text-emerald-600" /> Copied!
                </>
              ) : (
                <>
                  <Copy className="w-3.5 h-3.5" /> Copy Code
                </>
              )}
            </button>
          </div>
          <div className="relative">
            <pre className="p-4 bg-slate-900 text-slate-200 rounded-xl font-mono text-xs leading-relaxed overflow-x-auto border border-slate-800 max-h-[220px] overflow-y-auto">
              {pythonCode}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}
