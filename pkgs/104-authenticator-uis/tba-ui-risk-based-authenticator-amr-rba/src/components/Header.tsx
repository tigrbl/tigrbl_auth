import React, { useState, useEffect } from 'react';
import { Shield, Clock, HardDrive, RefreshCw } from 'lucide-react';

export default function Header() {
  const [time, setTime] = useState<string>('');

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setTime(now.toISOString().replace('T', ' ').substring(0, 19) + ' UTC');
    };
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header id="app-header" className="border-b border-slate-200 bg-white px-6 py-4 shadow-xs">
      <div className="mx-auto flex max-w-7xl flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        {/* Left Side: Brand & Icon */}
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-900 text-emerald-400">
            <Shield className="h-6 w-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="font-display text-xl font-bold tracking-tight text-slate-900">
                Risk-Based Authentication
              </h1>
              <span className="inline-flex items-center rounded-md bg-slate-100 px-1.5 py-0.5 text-xs font-mono font-medium text-slate-600 ring-1 ring-inset ring-slate-500/10">
                AMR: rba
              </span>
            </div>
            <p className="text-xs text-slate-500 font-sans">
              Adaptive Authentication Decision Engine &amp; Security Operations Center
            </p>
          </div>
        </div>

        {/* Right Side: Environment metadata & Real-time Clock */}
        <div className="flex flex-wrap items-center gap-4 text-xs font-mono">
          <div className="flex items-center gap-1.5 rounded-lg border border-slate-200 bg-slate-50 px-2.5 py-1.5 text-slate-600">
            <Clock className="h-3.5 w-3.5 text-slate-400" />
            <span>{time || 'Evaluating clock...'}</span>
          </div>

          <div className="flex items-center gap-1.5 rounded-lg border border-emerald-100 bg-emerald-50 px-2.5 py-1.5 text-emerald-700">
            <span className="relative flex h-2 w-2">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-500"></span>
            </span>
            <span>SYSTEM ENFORCED</span>
          </div>
        </div>
      </div>
    </header>
  );
}
