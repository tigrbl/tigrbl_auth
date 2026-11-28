import React from 'react';
import { DecisionRecord } from '../types';
import { ShieldCheck, ShieldAlert, FileText, Database, Server, CheckCircle2, GitCommit } from 'lucide-react';

export default function LineageGraph({ decision }: { decision: DecisionRecord }) {
  const isPermit = decision.effect === 'permit';

  return (
    <div className="flex flex-col items-center justify-center py-12 px-4 min-w-max">
      
      {/* Level 1: Inputs (Facts & Request) */}
      <div className="flex space-x-12 relative z-10">
        <GraphNode 
          title="Normalized Request" 
          subtitle={`${decision.subject.name} -> ${decision.action} -> ${decision.resource.name}`} 
          icon={FileText} 
          type="input" 
        />
        <div className="flex flex-col gap-4">
          {decision.facts.map((f, i) => (
             <GraphNode 
               key={f.id} 
               title="Verified Fact" 
               subtitle={`${f.type} (${f.source})`} 
               icon={Database} 
               type="fact" 
               warning={f.freshness !== 'fresh'}
             />
          ))}
        </div>
      </div>

      <Edge />

      {/* Level 2: Policy Engine */}
      <div className="relative z-10">
        <GraphNode 
          title="Policy Decision Point" 
          subtitle={`Engine: ${decision.engineVersion} | Policy: ${decision.policyVersion}`} 
          icon={Server} 
          type="pdp" 
        />
      </div>

      <Edge />

      {/* Level 3: Decision */}
      <div className="relative z-10">
        <GraphNode 
          title={`Decision: ${decision.effect.toUpperCase()}`} 
          subtitle={`Key: ${decision.decisionKey.substring(0, 16)}...`} 
          icon={isPermit ? ShieldCheck : ShieldAlert} 
          type={isPermit ? 'permit' : 'deny'} 
        />
      </div>

      <Edge />

      {/* Level 4: Outcomes */}
      <div className="flex space-x-12 relative z-10">
        {decision.obligations.length > 0 && (
          <div className="flex flex-col gap-4">
             {decision.obligations.map(o => (
               <GraphNode 
                 key={o.id} 
                 title="Obligation" 
                 subtitle={o.type} 
                 icon={FileText} 
                 type="obligation" 
               />
             ))}
          </div>
        )}
        <GraphNode 
          title="Enforcement (PEP)" 
          subtitle={decision.enforcement ? decision.enforcement.pepId : 'Missing Receipt'} 
          icon={decision.enforcement?.status === 'enforced' ? CheckCircle2 : ShieldAlert} 
          type={!decision.enforcement ? 'warning' : decision.enforcement.status === 'enforced' ? 'enforced' : 'warning'} 
        />
      </div>
      
    </div>
  );
}

function Edge() {
  return (
    <div className="h-12 w-0.5 bg-slate-300 relative -my-1 z-0">
      <div className="absolute -bottom-1 left-1/2 -translate-x-1/2 text-slate-300">
        <GitCommit className="w-4 h-4" />
      </div>
    </div>
  );
}

function GraphNode({ title, subtitle, icon: Icon, type, warning }: any) {
  const getColors = () => {
    if (warning) return "bg-amber-50 border-amber-300 text-amber-900";
    switch (type) {
      case 'input': return "bg-blue-50 border-blue-200 text-blue-900";
      case 'fact': return "bg-indigo-50 border-indigo-200 text-indigo-900";
      case 'pdp': return "bg-slate-800 border-slate-700 text-white";
      case 'permit': return "bg-emerald-100 border-emerald-300 text-emerald-900 shadow-emerald-200";
      case 'deny': return "bg-rose-100 border-rose-300 text-rose-900 shadow-rose-200";
      case 'obligation': return "bg-purple-50 border-purple-200 text-purple-900";
      case 'enforced': return "bg-teal-50 border-teal-200 text-teal-900";
      case 'warning': return "bg-amber-50 border-amber-300 text-amber-900";
      default: return "bg-white border-slate-200 text-slate-800";
    }
  };

  const getIconColor = () => {
    if (warning) return "text-amber-500";
    if (type === 'pdp') return "text-slate-300";
    if (type === 'permit') return "text-emerald-600";
    if (type === 'deny') return "text-rose-600";
    return "text-indigo-500";
  }

  return (
    <div className={`w-64 p-4 rounded-xl border-2 shadow-sm flex items-start ${getColors()}`}>
      <Icon className={`w-6 h-6 mr-3 shrink-0 ${getIconColor()}`} />
      <div>
        <h4 className="text-sm font-bold">{title}</h4>
        <p className={`text-xs mt-1 ${type === 'pdp' ? 'text-slate-400' : 'opacity-80'}`}>{subtitle}</p>
      </div>
    </div>
  );
}
