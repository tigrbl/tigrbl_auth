import React, { useState } from 'react';
import { ZonePolicy, PolicyAction } from '../types';
import { Plus, Edit2, Trash2, Check, X, ShieldAlert, Wifi, Globe, MapPin, RefreshCw } from 'lucide-react';

interface ZonePolicyEditorProps {
  policies: ZonePolicy[];
  onSavePolicy: (policy: ZonePolicy) => void;
  onDeletePolicy: (id: string) => void;
}

export const ZonePolicyEditor: React.FC<ZonePolicyEditorProps> = ({
  policies,
  onSavePolicy,
  onDeletePolicy
}) => {
  const [editingId, setEditingId] = useState<string | null>(null);
  const [isAdding, setIsAdding] = useState(false);

  // Form states
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [action, setAction] = useState<PolicyAction>('Allow');
  const [freshnessLimit, setFreshnessLimit] = useState(15);
  const [accuracyRequired, setAccuracyRequired] = useState(50);
  const [allowedCIDRs, setAllowedCIDRs] = useState('');
  const [lat, setLat] = useState(30.2672);
  const [lng, setLng] = useState(-97.7431);
  const [radius, setRadius] = useState(100);

  const startEdit = (policy: ZonePolicy) => {
    setEditingId(policy.id);
    setName(policy.name);
    setDescription(policy.description);
    setAction(policy.action);
    setFreshnessLimit(policy.freshnessLimit);
    setAccuracyRequired(policy.accuracyRequired);
    setAllowedCIDRs(policy.allowedCIDRs.join(', '));
    if (policy.bounds) {
      setLat(policy.bounds.lat);
      setLng(policy.bounds.lng);
      setRadius(policy.bounds.radius);
    } else {
      setLat(30.2672);
      setLng(-97.7431);
      setRadius(100);
    }
  };

  const startAdd = () => {
    setIsAdding(true);
    setEditingId(null);
    setName('');
    setDescription('');
    setAction('Allow');
    setFreshnessLimit(15);
    setAccuracyRequired(50);
    setAllowedCIDRs('192.168.1.0/24');
    setLat(30.2672);
    setLng(-97.7431);
    setRadius(150);
  };

  const handleCancel = () => {
    setEditingId(null);
    setIsAdding(false);
  };

  const handleSave = (id?: string) => {
    if (!name.trim()) return;

    const cidrArray = allowedCIDRs
      .split(',')
      .map((c) => c.trim())
      .filter((c) => c.length > 0);

    const savedPolicy: ZonePolicy = {
      id: id || `pol-${Date.now()}`,
      name,
      description,
      action,
      freshnessLimit: Number(freshnessLimit),
      accuracyRequired: Number(accuracyRequired),
      allowedCIDRs: cidrArray,
      isActive: true,
      bounds: {
        lat: Number(lat),
        lng: Number(lng),
        radius: Number(radius)
      }
    };

    onSavePolicy(savedPolicy);
    setEditingId(null);
    setIsAdding(false);
  };

  return (
    <div className="space-y-4" role="region" aria-label="Zone and Risk Policy Configurator">
      <div className="flex items-center justify-between">
        <div>
          <h4 className="text-sm font-semibold text-slate-900 font-display">
            Authentication Geofence & Risk Policy Ruleset
          </h4>
          <p className="text-xs text-slate-500">
            Define authorized corporate ranges, telemetry accuracy boundaries, and fallback triggers
          </p>
        </div>
        {!isAdding && !editingId && (
          <button
            onClick={startAdd}
            className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs px-3 py-1.5 rounded-lg transition-all flex items-center gap-1 shadow-sm"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>Add Zone Policy</span>
          </button>
        )}
      </div>

      {/* Editor/Add Form (Inline Modal overlay style) */}
      {(isAdding || editingId) && (
        <div className="bg-slate-50 border-2 border-indigo-200 rounded-xl p-5 space-y-4 shadow-sm animate-fade-in">
          <div className="flex items-center justify-between border-b border-slate-200 pb-2">
            <h5 className="text-xs font-bold text-slate-800 uppercase tracking-wider font-mono">
              {isAdding ? 'Create New Geofence Zone' : 'Modify Geofence Ruleset'}
            </h5>
            <button
              onClick={handleCancel}
              className="p-1 hover:bg-slate-200 rounded text-slate-400 hover:text-slate-600"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Left Col */}
            <div className="space-y-3">
              <div>
                <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
                  Zone/Policy Identifier Name
                </label>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="e.g. Austin R&D HQ"
                  className="w-full bg-white border border-slate-200 rounded-lg px-3 py-1.5 text-xs focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
                  Scope/Description
                </label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Policy enforcement details..."
                  rows={2}
                  className="w-full bg-white border border-slate-200 rounded-lg px-3 py-1.5 text-xs focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
                    Enforcement Action
                  </label>
                  <select
                    value={action}
                    onChange={(e) => setAction(e.target.value as PolicyAction)}
                    className="w-full bg-white border border-slate-200 rounded-lg px-2.5 py-1.5 text-xs focus:outline-none focus:border-indigo-500 font-semibold"
                  >
                    <option value="Allow">Allow access</option>
                    <option value="Step-Up">Force Step-Up Authentication</option>
                    <option value="Deny">Hard Block / Deny</option>
                  </select>
                </div>

                <div>
                  <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
                    Freshness Limit (Minutes)
                  </label>
                  <input
                    type="number"
                    value={freshnessLimit}
                    onChange={(e) => setFreshnessLimit(Number(e.target.value))}
                    className="w-full bg-white border border-slate-200 rounded-lg px-3 py-1.5 text-xs focus:outline-none focus:border-indigo-500"
                  />
                </div>
              </div>
            </div>

            {/* Right Col */}
            <div className="space-y-3">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
                    Center Latitude
                  </label>
                  <input
                    type="number"
                    step="0.0001"
                    value={lat}
                    onChange={(e) => setLat(Number(e.target.value))}
                    className="w-full bg-white border border-slate-200 rounded-lg px-3 py-1.5 text-xs font-mono focus:outline-none focus:border-indigo-500"
                  />
                </div>

                <div>
                  <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
                    Center Longitude
                  </label>
                  <input
                    type="number"
                    step="0.0001"
                    value={lng}
                    onChange={(e) => setLng(Number(e.target.value))}
                    className="w-full bg-white border border-slate-200 rounded-lg px-3 py-1.5 text-xs font-mono focus:outline-none focus:border-indigo-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
                    Geofence Radius (Meters)
                  </label>
                  <input
                    type="number"
                    value={radius}
                    onChange={(e) => setRadius(Number(e.target.value))}
                    className="w-full bg-white border border-slate-200 rounded-lg px-3 py-1.5 text-xs focus:outline-none focus:border-indigo-500"
                  />
                </div>

                <div>
                  <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
                    Min Accuracy Required (M)
                  </label>
                  <input
                    type="number"
                    value={accuracyRequired}
                    onChange={(e) => setAccuracyRequired(Number(e.target.value))}
                    className="w-full bg-white border border-slate-200 rounded-lg px-3 py-1.5 text-xs focus:outline-none focus:border-indigo-500"
                  />
                </div>
              </div>

              <div>
                <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
                  Allowed Network CIDR Blocks (Comma Separated)
                </label>
                <input
                  type="text"
                  value={allowedCIDRs}
                  onChange={(e) => setAllowedCIDRs(e.target.value)}
                  placeholder="e.g. 192.168.10.0/24, 10.10.0.0/16"
                  className="w-full bg-white border border-slate-200 rounded-lg px-3 py-1.5 text-xs font-mono focus:outline-none focus:border-indigo-500"
                />
              </div>
            </div>
          </div>

          <div className="flex justify-end gap-2 border-t border-slate-200 pt-3">
            <button
              onClick={handleCancel}
              className="bg-white border border-slate-200 hover:bg-slate-100 text-slate-700 font-semibold text-xs px-3 py-1.5 rounded-lg transition-all"
            >
              Cancel
            </button>
            <button
              onClick={() => handleSave(editingId || undefined)}
              className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs px-4 py-1.5 rounded-lg transition-all flex items-center gap-1 shadow-sm"
            >
              <Check className="w-3.5 h-3.5" />
              <span>Save Ruleset</span>
            </button>
          </div>
        </div>
      )}

      {/* Policies List Table */}
      <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse" role="table">
            <thead>
              <tr className="bg-slate-50 border-b border-slate-100 text-[10px] font-bold uppercase text-slate-400 tracking-wider">
                <th className="py-3.5 px-4">Policy/Geofence</th>
                <th className="py-3.5 px-4">Enforcement Action</th>
                <th className="py-3.5 px-4">Precision Requirement</th>
                <th className="py-3.5 px-4">Allowed Subnets</th>
                <th className="py-3.5 px-4 text-right">Operations</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-xs">
              {policies.map((p) => (
                <tr key={p.id} className="hover:bg-slate-50/50 transition-colors">
                  <td className="py-3.5 px-4">
                    <div className="font-semibold text-slate-800">{p.name}</div>
                    <div className="text-[11px] text-slate-400 line-clamp-1 mt-0.5">{p.description}</div>
                    {p.bounds && (
                      <div className="flex items-center gap-1.5 text-[10px] text-indigo-600 font-mono mt-1">
                        <MapPin className="w-3 h-3 text-indigo-400 shrink-0" />
                        <span>Radius: {p.bounds.radius}m | Lat: {p.bounds.lat}, Lng: {p.bounds.lng}</span>
                      </div>
                    )}
                  </td>
                  <td className="py-3.5 px-4">
                    <span className={`inline-flex px-2 py-0.5 rounded-full text-[10px] font-semibold ${
                      p.action === 'Allow' ? 'bg-emerald-100 text-emerald-800' :
                      p.action === 'Step-Up' ? 'bg-amber-100 text-amber-800' : 'bg-rose-100 text-rose-800'
                    }`}>
                      {p.action}
                    </span>
                  </td>
                  <td className="py-3.5 px-4">
                    <div className="text-slate-600">Freshness &lt; <strong className="font-semibold font-mono">{p.freshnessLimit} min</strong></div>
                    <div className="text-[10px] text-slate-400 mt-0.5">Required Accuracy &lt; <strong className="font-mono">{p.accuracyRequired}m</strong></div>
                  </td>
                  <td className="py-3.5 px-4">
                    <div className="flex flex-wrap gap-1 max-w-[200px]">
                      {p.allowedCIDRs.map((cidr, index) => (
                        <span key={index} className="font-mono bg-slate-100 text-slate-600 text-[10px] px-1.5 py-0.5 rounded border border-slate-150">
                          {cidr === '*' ? 'ANY IP' : cidr}
                        </span>
                      ))}
                    </div>
                  </td>
                  <td className="py-3.5 px-4 text-right">
                    <div className="flex items-center justify-end gap-1.5">
                      <button
                        title="Edit policy"
                        onClick={() => startEdit(p)}
                        className="p-1 hover:bg-slate-100 rounded text-slate-500 hover:text-slate-700 transition-colors"
                      >
                        <Edit2 className="w-3.5 h-3.5" />
                      </button>
                      <button
                        title="Delete policy"
                        onClick={() => onDeletePolicy(p.id)}
                        className="p-1 hover:bg-rose-50 rounded text-rose-400 hover:text-rose-600 transition-colors"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
