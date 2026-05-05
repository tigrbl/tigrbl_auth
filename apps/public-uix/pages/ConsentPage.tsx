import React from "react";
import { Card } from "../components/UI";

interface ConsentPageProps {
  approveTarget: string;
  cancelTarget: string;
  clientName: string;
  scopes: string[];
}

export const ConsentPage: React.FC<ConsentPageProps> = ({
  approveTarget,
  cancelTarget,
  clientName,
  scopes,
}) => {
  const requestedScopes = scopes.length > 0 ? scopes : ["openid"];

  return (
    <div className="flex-grow flex items-center justify-center p-6 bg-slate-50">
      <div className="w-full max-w-2xl space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
        <div className="text-center space-y-2">
          <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Review consent</h1>
          <p className="text-slate-500">
            Confirm the information {clientName} may access through the governed tigrbl_auth public UIX.
          </p>
        </div>

        <Card className="p-8 space-y-6">
          <div className="space-y-2">
            <p className="text-xs font-bold uppercase tracking-[0.2em] text-slate-400">Client application</p>
            <p className="text-xl font-semibold text-slate-900">{clientName}</p>
          </div>

          <div className="space-y-3">
            <p className="text-xs font-bold uppercase tracking-[0.2em] text-slate-400">Requested scopes</p>
            <div className="flex flex-wrap gap-2">
              {requestedScopes.map((scope) => (
                <span
                  key={scope}
                  className="rounded-full bg-slate-100 px-3 py-1 text-sm font-semibold text-slate-700"
                >
                  {scope}
                </span>
              ))}
            </div>
          </div>

          <p className="text-sm leading-6 text-slate-600">
            Approval returns you only to governed public UIX routes. Administrative and control-plane surfaces
            remain excluded from this browser-facing flow.
          </p>

          <div className="flex flex-col gap-3 pt-2 sm:flex-row">
            <button
              type="button"
              onClick={() => {
                window.location.hash = approveTarget;
              }}
              className="flex-1 rounded-brand bg-brand px-5 py-3 font-semibold text-white shadow-lg shadow-brand/20 transition-all hover:opacity-90"
            >
              Approve access
            </button>
            <button
              type="button"
              onClick={() => {
                window.location.hash = cancelTarget;
              }}
              className="flex-1 rounded-brand border border-slate-200 px-5 py-3 font-semibold text-slate-600 transition-colors hover:border-slate-300 hover:text-slate-900"
            >
              Cancel
            </button>
          </div>
        </Card>
      </div>
    </div>
  );
};

