import React from 'react';
import { Cpu, ShieldCheck, HelpCircle, HardDrive, AlertCircle, RefreshCw, Layers } from 'lucide-react';

interface PreflightProps {
  browserCompatible: boolean;
  middlewareRunning: boolean;
  readerConnected: boolean;
  cardInserted: boolean;
  selectedReaderName: string;
  onRefresh: () => void;
}

export const SmartCardPreflight: React.FC<PreflightProps> = ({
  browserCompatible,
  middlewareRunning,
  readerConnected,
  cardInserted,
  selectedReaderName,
  onRefresh,
}) => {
  const checkList = [
    {
      id: 'browser',
      name: 'Browser Certificate Selector Extension / API',
      description: 'WebCrypto mTLS & native OS certificate routing compatibility',
      status: browserCompatible ? 'pass' : 'fail',
      errorMsg: 'Your current browser is missing secure WebCrypto mTLS bindings. Use Chrome, Edge, or Firefox.',
    },
    {
      id: 'middleware',
      name: 'Smart Card Middleware (ActivClient / OpenSC / Charismathics)',
      description: 'Cryptographic API (PKCS#11 / CNG / CryptoAPI) communication bridge',
      status: browserCompatible ? (middlewareRunning ? 'pass' : 'warning') : 'fail',
      errorMsg: 'Middleware service not responding. Ensure ActivClient, OpenSC, or your organizational PKCS#11 driver is running.',
    },
    {
      id: 'reader',
      name: 'Smart Card USB / Contactless Reader',
      description: 'CCID compliant hardware reader connection status',
      status: browserCompatible && middlewareRunning ? (readerConnected ? 'pass' : 'fail') : 'pending',
      errorMsg: 'No USB CCID smart card reader detected. Plug in your external reader (SCR-3310, Omnikey, etc.).',
    },
    {
      id: 'card',
      name: 'Physical Token Insertion (PIV / CAC)',
      description: 'Presence of valid cryptographic microchip on reader contact',
      status: browserCompatible && middlewareRunning && readerConnected ? (cardInserted ? 'pass' : 'fail') : 'pending',
      errorMsg: 'Card slot is empty. Insert your PIV/CAC card firmly into the reader contact point.',
    },
  ];

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm" id="preflight-card">
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-100">
        <div className="flex items-center gap-2">
          <ShieldCheck className="w-5 h-5 text-indigo-600" />
          <h3 className="font-semibold text-slate-800 text-base">Compatibility & Middleware Preflight</h3>
        </div>
        <button
          onClick={onRefresh}
          className="flex items-center gap-1.5 px-3 py-1 text-xs font-medium text-slate-600 hover:text-indigo-600 border border-slate-200 rounded-lg bg-slate-50 hover:bg-indigo-50 transition-colors"
          id="btn-preflight-refresh"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          Re-scan Hardware
        </button>
      </div>

      <p className="text-xs text-slate-500 mb-4 leading-relaxed">
        Before smart card authentication can occur, your local web-browser, operating system certificate store, cryptoprovider, reader, and CAC/PIV physical device must be verified.
      </p>

      {/* Reader status bar */}
      <div className="bg-slate-50 rounded-lg p-3 mb-5 border border-slate-200/60 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <HardDrive className={`w-5 h-5 ${readerConnected ? 'text-indigo-600' : 'text-slate-400'}`} />
          <div>
            <div className="text-xs font-semibold text-slate-700">USB Reader Interface</div>
            <div className="text-[10.5px] text-slate-500 font-mono">
              {readerConnected ? selectedReaderName : 'No reader detected (polling CCID...)'}
            </div>
          </div>
        </div>
        <span
          className={`text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full ${
            readerConnected
              ? 'bg-emerald-100 text-emerald-800 border border-emerald-200'
              : 'bg-amber-100 text-amber-800 border border-amber-200'
          }`}
        >
          {readerConnected ? 'CONNECTED' : 'DISCONNECTED'}
        </span>
      </div>

      {/* Grid of steps */}
      <div className="space-y-3.5">
        {checkList.map((step) => (
          <div
            key={step.id}
            className={`p-3.5 rounded-lg border transition-all ${
              step.status === 'pass'
                ? 'bg-emerald-50/40 border-emerald-100'
                : step.status === 'fail'
                ? 'bg-rose-50/40 border-rose-100'
                : step.status === 'warning'
                ? 'bg-amber-50/40 border-amber-100'
                : 'bg-slate-50/50 border-slate-100 opacity-65'
            }`}
          >
            <div className="flex items-start justify-between gap-3">
              <div className="flex gap-2.5">
                <div className="mt-0.5">
                  {step.status === 'pass' && (
                    <span className="flex h-4 w-4 items-center justify-center rounded-full bg-emerald-500 text-white text-[10px] font-bold">✓</span>
                  )}
                  {step.status === 'fail' && (
                    <span className="flex h-4 w-4 items-center justify-center rounded-full bg-rose-500 text-white text-[10px] font-bold">✕</span>
                  )}
                  {step.status === 'warning' && (
                    <span className="flex h-4 w-4 items-center justify-center rounded-full bg-amber-500 text-white text-[10px] font-bold">!</span>
                  )}
                  {step.status === 'pending' && (
                    <span className="flex h-4 w-4 items-center justify-center rounded-full bg-slate-300 text-slate-600 text-[9px] font-bold">○</span>
                  )}
                </div>
                <div>
                  <h4 className="text-xs font-semibold text-slate-800">{step.name}</h4>
                  <p className="text-[10px] text-slate-500 mt-0.5 leading-relaxed">{step.description}</p>
                </div>
              </div>
              <span className="text-[9.5px] font-mono uppercase tracking-wider font-semibold">
                {step.status === 'pass' && <span className="text-emerald-700">Pass</span>}
                {step.status === 'fail' && <span className="text-rose-700">Fail</span>}
                {step.status === 'warning' && <span className="text-amber-700">Warning</span>}
                {step.status === 'pending' && <span className="text-slate-400">Blocked</span>}
              </span>
            </div>

            {/* Error Message if failed / warned */}
            {(step.status === 'fail' || step.status === 'warning') && (
              <div className="mt-2.5 pt-2 border-t border-dashed border-slate-200/60 flex items-start gap-1.5">
                <AlertCircle className="w-3.5 h-3.5 text-rose-500 shrink-0 mt-0.5" />
                <p className="text-[10px] text-slate-600 font-medium leading-relaxed">{step.errorMsg}</p>
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="mt-4 p-3 bg-indigo-50/50 border border-indigo-100 rounded-lg flex items-start gap-2">
        <Layers className="w-4 h-4 text-indigo-600 mt-0.5 shrink-0" />
        <div className="text-[10px] text-indigo-900 leading-relaxed">
          <span className="font-semibold">Security Note:</span> CAC and PIV smart cards use on-chip cryptographic modules (FIPS 140-2 Level 3) where the private signing keys never leave the hardware boundary. PIN authentication is managed safely within the card microchip.
        </div>
      </div>
    </div>
  );
};
