import React from 'react';
import { RefreshCw, CheckCircle, ArrowRight, CornerDownRight } from 'lucide-react';

interface KeyRotationTimelineProps {
  currentStage: number; // 0 to 4
  onAdvance: () => void;
  onReset: () => void;
  replacingKeyName: string;
  originalKeyName: string;
}

export default function KeyRotationTimeline({
  currentStage,
  onAdvance,
  onReset,
  replacingKeyName,
  originalKeyName
}: KeyRotationTimelineProps) {
  const stages = [
    { label: 'Unrotated', desc: 'Single active production key.' },
    { label: 'Generated Overlap', desc: 'Co-exist replacement key created.' },
    { label: 'Attestation Verified', desc: 'Ownership proof validated by server.' },
    { label: 'Telemetry Verification', desc: 'Overlapping 10% traffic test active.' },
    { label: 'Retired Active v2', desc: 'Original key revoked, v2 fully active.' }
  ];

  return (
    <div id="key-rotation-timeline" className="bg-slate-900/60 border border-slate-800 rounded-xl p-4 space-y-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-2">
        <div className="flex items-center gap-1.5 font-bold text-slate-100 text-xs uppercase tracking-wide">
          <RefreshCw className="w-3.5 h-3.5 text-indigo-400" />
          <span>Overlapping Rotation Lifecycle</span>
        </div>
        <span className="text-[10px] font-mono font-bold bg-indigo-950/60 text-indigo-400 border border-indigo-900/40 px-1.5 py-0.5 rounded">
          Stage {currentStage}/4
        </span>
      </div>

      <div className="space-y-3">
        <div className="flex flex-col gap-2.5">
          {stages.map((stg, index) => {
            const isCompleted = index < currentStage;
            const isCurrent = index === currentStage;

            return (
              <div key={stg.label} className="flex gap-2.5 items-start text-xs relative">
                {index < stages.length - 1 && (
                  <div className={`absolute left-2.5 top-6 w-0.5 h-6 ${isCompleted ? 'bg-indigo-500' : 'bg-slate-800'}`} />
                )}
                <div className={`w-5 h-5 rounded-full flex items-center justify-center shrink-0 border text-[10px] font-bold ${
                  isCompleted
                    ? 'bg-indigo-600/25 border-indigo-500 text-indigo-400'
                    : isCurrent
                    ? 'bg-indigo-600 text-white border-indigo-500 ring-4 ring-indigo-500/15'
                    : 'bg-slate-950 border-slate-800 text-slate-500'
                }`}>
                  {isCompleted ? '✓' : index}
                </div>
                <div className="space-y-0.5 pt-0.5">
                  <span className={`font-semibold block ${isCurrent ? 'text-slate-100 font-bold' : isCompleted ? 'text-slate-300' : 'text-slate-500'}`}>
                    {stg.label}
                  </span>
                  <p className="text-[10.5px] text-slate-400 leading-normal">{stg.desc}</p>
                </div>
              </div>
            );
          })}
        </div>

        <div className="bg-slate-950/40 border border-slate-850 p-2.5 rounded-lg space-y-1.5 text-[11px] text-slate-300">
          <div className="flex items-center gap-1 font-semibold text-slate-400">
            <CornerDownRight className="w-3.5 h-3.5 shrink-0" />
            <span>Active State Details:</span>
          </div>
          {currentStage === 0 && (
            <p>Ready to trigger dual-lifetime key overlap for <span className="text-indigo-400 font-mono">{originalKeyName}</span>.</p>
          )}
          {currentStage > 0 && currentStage < 4 && (
            <p>Dual active overlap: Both <span className="text-amber-400 font-mono">{originalKeyName}</span> and <span className="text-indigo-400 font-mono">{replacingKeyName}</span> sign requests.</p>
          )}
          {currentStage === 4 && (
            <p>Rotation finalized. Only <span className="text-emerald-400 font-mono">{replacingKeyName}</span> is accepted. Retired keys are logged.</p>
          )}
        </div>

        <div className="flex gap-2 justify-end pt-1">
          {currentStage > 0 && (
            <button
              onClick={onReset}
              className="text-[11px] bg-slate-800 hover:bg-slate-750 text-slate-300 font-bold py-1.5 px-3 rounded-lg transition-colors cursor-pointer"
            >
              Reset Lifecycle
            </button>
          )}
          {currentStage < 4 && (
            <button
              onClick={onAdvance}
              className="text-[11px] bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-1.5 px-3 rounded-lg transition-colors flex items-center gap-1 cursor-pointer"
            >
              Advance Stage <ArrowRight className="w-3 h-3" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
