import React, { useState } from 'react';
import { ShieldCheck, ShieldAlert, AlertOctagon, Key, Trash2, Ban, Play, Activity } from 'lucide-react';
import { SimulatedServerState, AuditEvent } from '../types';

interface PinLifecyclePanelProps {
  serverState: SimulatedServerState;
  onAction: (action: string, payload?: any) => void;
  recentStrongAuth: boolean;
  onTriggerRecentStrongAuth: () => void;
}

export function PinLifecyclePanel({
  serverState,
  onAction,
  recentStrongAuth,
  onTriggerRecentStrongAuth,
}: PinLifecyclePanelProps) {
  const [showStatusConfirm, setShowStatusConfirm] = useState<'suspend' | 'compromise' | 'remove' | null>(null);

  const getStatusColor = () => {
    switch (serverState.status) {
      case 'active':
        return 'text-emerald-400 bg-emerald-950/30 border-emerald-900/50';
      case 'suspended':
        return 'text-amber-400 bg-amber-950/20 border-amber-900/40';
      case 'revoked':
        return 'text-slate-400 bg-slate-900/50 border-slate-800';
      case 'locked':
        return 'text-red-400 bg-red-950/30 border-red-900/50';
      case 'compromised':
        return 'text-rose-500 bg-rose-950/30 border-rose-900/50 font-bold';
      case 'forced-reset':
        return 'text-yellow-400 bg-yellow-950/30 border-yellow-900/50';
      default:
        return 'text-slate-400';
    }
  };

  const handleActionClick = (type: 'suspend' | 'compromise' | 'remove') => {
    if (!recentStrongAuth) {
      onTriggerRecentStrongAuth();
      return;
    }
    setShowStatusConfirm(type);
  };

  const confirmAction = () => {
    if (showStatusConfirm) {
      onAction(showStatusConfirm);
      setShowStatusConfirm(null);
    }
  };

  return (
    <div className="bg-slate-900/40 border border-slate-800 p-5 rounded-2xl text-left space-y-4">
      <div className="flex justify-between items-center border-b border-slate-800/80 pb-3">
        <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center gap-1.5">
          <Activity size={14} className="text-blue-400" />
          First-Party PIN Lifecycle Control
        </h3>
        {serverState.isFirstPartyEnrolled ? (
          <span className={`text-[10px] font-mono font-bold px-2.5 py-0.5 rounded border uppercase tracking-wider ${getStatusColor()}`}>
            {serverState.status}
          </span>
        ) : (
          <span className="text-[10px] font-mono text-slate-500 uppercase">Not Enrolled</span>
        )}
      </div>

      {!serverState.isFirstPartyEnrolled ? (
        <div className="text-center py-4 bg-slate-950/30 rounded-xl border border-dashed border-slate-800">
          <p className="text-xs text-slate-500 font-mono">No active account PIN found on simulated server.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {/* Security safeguard notice */}
          <div className="flex justify-between items-center bg-slate-950 p-3 rounded-xl border border-slate-850">
            <div className="space-y-0.5">
              <span className="text-[9px] font-mono text-slate-500 uppercase block">Safeguard Authorization</span>
              <span className={`text-xs font-semibold ${recentStrongAuth ? 'text-emerald-400' : 'text-amber-400'}`}>
                {recentStrongAuth ? '🛡️ Recent strong auth verified' : '⚠️ Strong auth required to edit'}
              </span>
            </div>
            {!recentStrongAuth && (
              <button
                type="button"
                onClick={onTriggerRecentStrongAuth}
                className="py-1 px-2.5 rounded bg-blue-950 border border-blue-900 hover:bg-blue-900 text-[10px] font-semibold text-blue-300 cursor-pointer transition-all"
              >
                Authenticate Now
              </button>
            )}
          </div>

          <div className="grid grid-cols-2 gap-2">
            {/* Suspend / Resume */}
            {serverState.status === 'suspended' ? (
              <button
                type="button"
                onClick={() => onAction('resume')}
                disabled={!recentStrongAuth}
                className="py-2 px-3 rounded-lg bg-emerald-950/40 border border-emerald-900 text-emerald-400 hover:bg-emerald-900/40 text-xs font-semibold flex items-center gap-1.5 transition-all cursor-pointer disabled:opacity-30 disabled:cursor-not-allowed"
              >
                <Play size={14} />
                Resume Use
              </button>
            ) : (
              <button
                type="button"
                disabled={!recentStrongAuth || serverState.status !== 'active'}
                onClick={() => handleActionClick('suspend')}
                className="py-2 px-3 rounded-lg bg-slate-950 border border-slate-800 text-amber-400 hover:bg-amber-950/10 text-xs font-semibold flex items-center gap-1.5 transition-all cursor-pointer disabled:opacity-30 disabled:cursor-not-allowed"
              >
                <Ban size={14} />
                Suspend PIN
              </button>
            )}

            {/* Compromise Indicator */}
            <button
              type="button"
              disabled={!recentStrongAuth || serverState.status === 'compromised'}
              onClick={() => handleActionClick('compromise')}
              className="py-2 px-3 rounded-lg bg-slate-950 border border-slate-800 text-rose-400 hover:bg-rose-950/10 text-xs font-semibold flex items-center gap-1.5 transition-all cursor-pointer disabled:opacity-30 disabled:cursor-not-allowed"
            >
              <AlertOctagon size={14} />
              Flag Compromise
            </button>

            {/* Forced Admin Reset */}
            <button
              type="button"
              disabled={serverState.status === 'forced-reset'}
              onClick={() => onAction('force-reset')}
              className="col-span-2 py-2 px-3 rounded-lg bg-yellow-950/20 border border-yellow-900/50 text-yellow-400 hover:bg-yellow-900/30 text-xs font-semibold flex items-center justify-center gap-1.5 transition-all cursor-pointer disabled:opacity-30"
            >
              <Key size={14} />
              Force Administrative Reset State
            </button>

            {/* Revoke / Remove safeguards */}
            <button
              type="button"
              disabled={!recentStrongAuth}
              onClick={() => handleActionClick('remove')}
              className="col-span-2 py-2.5 px-3 rounded-lg bg-red-950/10 border border-red-900/30 text-red-400 hover:bg-red-950/30 text-xs font-semibold flex items-center justify-center gap-1.5 transition-all cursor-pointer disabled:opacity-30 disabled:cursor-not-allowed"
            >
              <Trash2 size={14} />
              Remove PIN (Safeguards Enforced)
            </button>
          </div>

          {showStatusConfirm && (
            <div className="bg-slate-950 border border-slate-800 p-3 rounded-xl space-y-3 mt-2 animate-fadeIn">
              <p className="text-xs text-slate-300 font-sans">
                Are you absolutely sure you want to <span className="font-bold text-red-400 uppercase">{showStatusConfirm}</span> this first-party PIN?
              </p>
              <div className="flex gap-2">
                <button
                  type="button"
                  onClick={confirmAction}
                  className="flex-1 py-1 px-3 bg-red-600 text-white rounded text-xs font-semibold cursor-pointer hover:bg-red-500 transition-colors"
                >
                  Yes, Confirm
                </button>
                <button
                  type="button"
                  onClick={() => setShowStatusConfirm(null)}
                  className="flex-1 py-1 px-3 bg-slate-800 text-slate-300 rounded text-xs font-semibold cursor-pointer hover:bg-slate-700 transition-colors"
                >
                  Cancel
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
