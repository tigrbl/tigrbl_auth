import React from 'react';
import { SimulationProfile, ZonePolicy } from '../types';
import { MapPin, ShieldAlert, CheckCircle2, ShieldX, Compass, AlertTriangle, UserMinus } from 'lucide-react';

interface BoundarySimulatorProps {
  simulationProfiles: SimulationProfile[];
  activeProfile: SimulationProfile;
  policies: ZonePolicy[];
  onSelectProfile: (profile: SimulationProfile) => void;
  onChangeProfileValue: (key: keyof SimulationProfile, value: any) => void;
}

export const BoundarySimulator: React.FC<BoundarySimulatorProps> = ({
  simulationProfiles,
  activeProfile,
  policies,
  onSelectProfile,
  onChangeProfileValue
}) => {
  // Evaluates a simulation profile against all active policies
  const evaluatePolicyResult = (profile: SimulationProfile) => {
    // 1. Check for provider outage
    if (profile.providerStatus === 'offline') {
      return {
        action: 'Step-Up' as const,
        reason: 'Provider Outage Fallback',
        details: 'Failure state occurred; system fails-securely to OTP validation (silent fail-open is strictly prohibited).'
      };
    }

    // 2. Check for suspicious signals / VPN / Spoofing
    if (profile.vpnActive || profile.mockLocationActive) {
      const denyPolicies = policies.filter((p) => p.action === 'Deny' && p.isActive);
      if (denyPolicies.length > 0) {
        return {
          action: 'Deny' as const,
          reason: 'Embargoed/Suspicious Signals Policy Triggered',
          details: 'Telemetry indicates active proxy/VPN or mock location engine. High-risk signature blocked.'
        };
      }
      return {
        action: 'Step-Up' as const,
        reason: 'Suspicious Telemetry / VPN Active',
        details: 'Unverified signal origin. OTP or Passkey authentication required.'
      };
    }

    // 3. Check for lack of GPS permission
    if (!profile.permissionGranted) {
      return {
        action: 'Step-Up' as const,
        reason: 'GPS Permission Unavailable',
        details: 'Evaluating coarse network carrier IP instead. Forcing step-up ceremony.'
      };
    }

    // 4. Evaluate precise corporate geofences
    const hqPolicy = policies.find((p) => p.id === 'pol-corp-hq' && p.isActive);
    if (hqPolicy && hqPolicy.bounds) {
      const distance = calculateDistance(
        profile.lat,
        profile.lng,
        hqPolicy.bounds.lat,
        hqPolicy.bounds.lng
      );

      const inGeofence = distance <= hqPolicy.bounds.radius;
      const goodAccuracy = profile.accuracy <= hqPolicy.accuracyRequired;

      if (inGeofence && goodAccuracy) {
        // Also check CIDR matching (simulated)
        const isIpApproved = profile.ipAddress.startsWith('192.168.') || profile.ipAddress.startsWith('10.');
        if (isIpApproved) {
          return {
            action: hqPolicy.action,
            reason: 'Enterprise Headquarters Access Verified',
            details: `GPS within ${hqPolicy.bounds.radius}m fence (actual dist: ${distance.toFixed(1)}m) and IP is on trusted corporate corporate subnets.`
          };
        } else {
          return {
            action: 'Step-Up' as const,
            reason: 'Untrusted Network Origin',
            details: `GPS is inside the HQ perimeter but connection source IP (${profile.ipAddress}) is not on an enterprise wireless segment.`
          };
        }
      }
    }

    // 5. Evaluate broader regional bounds
    const regionPolicy = policies.find((p) => p.id === 'pol-low-risk-zone' && p.isActive);
    if (regionPolicy && regionPolicy.bounds) {
      const distance = calculateDistance(
        profile.lat,
        profile.lng,
        regionPolicy.bounds.lat,
        regionPolicy.bounds.lng
      );

      const inRegion = distance <= regionPolicy.bounds.radius;
      if (inRegion) {
        return {
          action: regionPolicy.action,
          reason: 'Domestic Regional Access Match',
          details: `User resides within Austin/Regional bounds (dist: ${(distance / 1000).toFixed(1)}km). Verified region matching.`
        };
      }
    }

    // 6. Default Deny / Strict Fallback
    return {
      action: 'Deny' as const,
      reason: 'No Matching Policy/Geofence Range',
      details: 'Coordinates and IP did not correlate to any approved workspace zones. Strict default-deny rule enforced.'
    };
  };

  // Haversine formula
  const calculateDistance = (lat1: number, lon1: number, lat2: number, lon2: number) => {
    const R = 6371000; // Radius of the earth in m
    const dLat = ((lat2 - lat1) * Math.PI) / 180;
    const dLon = ((lon2 - lon1) * Math.PI) / 180;
    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos((lat1 * Math.PI) / 180) *
        Math.cos((lat2 * Math.PI) / 180) *
        Math.sin(dLon / 2) *
        Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    const d = R * c; // Distance in m
    return d;
  };

  const currentResult = evaluatePolicyResult(activeProfile);

  // Lockout & Impact analysis
  const getImpactMetrics = () => {
    if (currentResult.action === 'Deny') {
      return {
        level: 'CRITICAL RISK' as const,
        bg: 'bg-rose-50 border-rose-200 text-rose-800 dark:bg-rose-950/20 dark:border-rose-900',
        alertIcon: ShieldX,
        lockoutRate: '95% of ordinary workforce',
        advice: 'Applying this configuration will hard block any remote connections from outside corporate geofences. Support center load will spikes.'
      };
    } else if (currentResult.action === 'Step-Up') {
      return {
        level: 'MODERATE RISK' as const,
        bg: 'bg-amber-50 border-amber-200 text-amber-800 dark:bg-amber-950/20 dark:border-amber-900',
        alertIcon: AlertTriangle,
        lockoutRate: '35% auth friction bump',
        advice: 'Users in this boundary will be forced to solve an SMS or Passkey challenge. Encourages security posture but adds transaction overhead.'
      };
    } else {
      return {
        level: 'LOW FRICTION' as const,
        bg: 'bg-emerald-50 border-emerald-200 text-emerald-800 dark:bg-emerald-950/10 dark:border-emerald-900',
        alertIcon: CheckCircle2,
        lockoutRate: '0% user friction',
        advice: 'Optimal login velocity. Access is silently allowed on verified high-accuracy GPS perimeters.'
      };
    }
  };

  const impact = getImpactMetrics();
  const ImpactIcon = impact.alertIcon;

  return (
    <div className="space-y-5" role="region" aria-label="Boundary Condition Simulator">
      <div>
        <h4 className="text-sm font-semibold text-slate-900 font-display">
          Geofence Boundary & Outage Simulator
        </h4>
        <p className="text-xs text-slate-500">
          Simulate extreme user locations, spoof detectors, device configurations, and provider offline states
        </p>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-5">
        {/* Simulator Profiles & Controls */}
        <div className="xl:col-span-2 bg-white border border-slate-200 rounded-xl p-5 shadow-sm space-y-4">
          <div>
            <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1.5">
              Select Preset Simulation Profile
            </label>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              {simulationProfiles.map((p) => {
                const isSelected = p.id === activeProfile.id;
                return (
                  <button
                    key={p.id}
                    onClick={() => onSelectProfile(p)}
                    className={`text-left p-3 rounded-lg border transition-all ${
                      isSelected
                        ? 'border-indigo-600 bg-indigo-50/50'
                        : 'border-slate-150 hover:border-slate-300 hover:bg-slate-50/50'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-slate-800 block truncate">{p.name}</span>
                      {isSelected && <CheckCircle2 className="w-3.5 h-3.5 text-indigo-600 shrink-0" />}
                    </div>
                    <span className="text-[10px] text-slate-500 line-clamp-1 block mt-0.5">{p.description}</span>
                  </button>
                );
              })}
            </div>
          </div>

          <hr className="border-slate-100" />

          {/* Interactive Parameters */}
          <div className="space-y-4">
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
              Customize Selected Boundary Parameters
            </span>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {/* Latitude / Longitude */}
              <div>
                <label className="text-xs font-semibold text-slate-700 block mb-1">GPS Coordinates</label>
                <div className="grid grid-cols-2 gap-2">
                  <input
                    type="number"
                    step="0.0001"
                    value={activeProfile.lat}
                    onChange={(e) => onChangeProfileValue('lat', Number(e.target.value))}
                    placeholder="Lat"
                    disabled={!activeProfile.permissionGranted}
                    className="w-full bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 text-xs font-mono disabled:opacity-50"
                  />
                  <input
                    type="number"
                    step="0.0001"
                    value={activeProfile.lng}
                    onChange={(e) => onChangeProfileValue('lng', Number(e.target.value))}
                    placeholder="Lng"
                    disabled={!activeProfile.permissionGranted}
                    className="w-full bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 text-xs font-mono disabled:opacity-50"
                  />
                </div>
              </div>

              {/* Accuracy / IP */}
              <div>
                <label className="text-xs font-semibold text-slate-700 block mb-1">Accuracy Radius & IP</label>
                <div className="grid grid-cols-2 gap-2">
                  <input
                    type="number"
                    value={activeProfile.accuracy}
                    onChange={(e) => onChangeProfileValue('accuracy', Number(e.target.value))}
                    placeholder="Meters"
                    disabled={!activeProfile.permissionGranted}
                    className="w-full bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 text-xs font-mono disabled:opacity-50"
                  />
                  <input
                    type="text"
                    value={activeProfile.ipAddress}
                    onChange={(e) => onChangeProfileValue('ipAddress', e.target.value)}
                    placeholder="IP Address"
                    className="w-full bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 text-xs font-mono"
                  />
                </div>
              </div>

              {/* Toggle checklist */}
              <div className="sm:col-span-2 grid grid-cols-2 sm:grid-cols-4 gap-2.5 pt-1.5">
                {/* Geolocation permission */}
                <label className="flex items-center gap-2 cursor-pointer bg-slate-50 border border-slate-200 rounded-lg p-2 hover:bg-slate-100 transition-all">
                  <input
                    type="checkbox"
                    checked={activeProfile.permissionGranted}
                    onChange={(e) => onChangeProfileValue('permissionGranted', e.target.checked)}
                    className="rounded border-slate-300 text-indigo-600 focus:ring-indigo-500"
                  />
                  <span className="text-[11px] font-medium text-slate-700 select-none">GPS Allowed</span>
                </label>

                {/* VPN state */}
                <label className="flex items-center gap-2 cursor-pointer bg-slate-50 border border-slate-200 rounded-lg p-2 hover:bg-slate-100 transition-all">
                  <input
                    type="checkbox"
                    checked={activeProfile.vpnActive}
                    onChange={(e) => onChangeProfileValue('vpnActive', e.target.checked)}
                    className="rounded border-slate-300 text-indigo-600 focus:ring-indigo-500"
                  />
                  <span className="text-[11px] font-medium text-slate-700 select-none">VPN Tunnel</span>
                </label>

                {/* Developer mock mock state */}
                <label className="flex items-center gap-2 cursor-pointer bg-slate-50 border border-slate-200 rounded-lg p-2 hover:bg-slate-100 transition-all">
                  <input
                    type="checkbox"
                    checked={activeProfile.mockLocationActive}
                    onChange={(e) => onChangeProfileValue('mockLocationActive', e.target.checked)}
                    className="rounded border-slate-300 text-indigo-600 focus:ring-indigo-500"
                  />
                  <span className="text-[11px] font-medium text-slate-700 select-none">Mock Location</span>
                </label>

                {/* Provider status dropdown */}
                <div className="flex flex-col">
                  <select
                    value={activeProfile.providerStatus}
                    onChange={(e) => onChangeProfileValue('providerStatus', e.target.value)}
                    className="bg-slate-50 border border-slate-200 rounded-lg p-2 text-[11px] font-semibold text-slate-700 focus:outline-none"
                  >
                    <option value="healthy">GPS Provider: OK</option>
                    <option value="degraded">GPS Provider: Degraded</option>
                    <option value="offline">GPS Provider: OFFLINE</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Live Evaluation Panel */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm text-slate-100 flex flex-col justify-between">
          <div className="space-y-4">
            <div className="flex items-center gap-1.5 font-mono text-[10px] text-slate-400">
              <Compass className="w-3.5 h-3.5 animate-pulse text-indigo-400" />
              <span>LIVE POLICY COMPASS ENGINE</span>
            </div>

            <div className="space-y-1.5">
              <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider block">
                Calculated Action
              </span>
              <div className="flex items-center gap-2">
                <span className={`text-xl font-bold font-display uppercase px-2.5 py-0.5 rounded ${
                  currentResult.action === 'Allow' ? 'bg-emerald-950 text-emerald-400 border border-emerald-900' :
                  currentResult.action === 'Step-Up' ? 'bg-amber-950 text-amber-400 border border-amber-900' :
                  'bg-rose-950 text-rose-400 border border-rose-900'
                }`}>
                  {currentResult.action}
                </span>
              </div>
            </div>

            <div className="space-y-1 bg-slate-950 border border-slate-800 rounded-lg p-3">
              <span className="text-[9px] font-bold text-slate-500 uppercase tracking-wider block font-mono">
                Matching Rule Explanation
              </span>
              <p className="text-xs text-indigo-300 font-semibold font-mono leading-relaxed">
                {currentResult.reason}
              </p>
              <p className="text-[11px] text-slate-400 leading-normal pt-1">
                {currentResult.details}
              </p>
            </div>
          </div>

          {/* Lockout and Risk analysis */}
          <div className={`mt-5 p-4 rounded-lg border ${impact.bg}`}>
            <div className="flex items-center gap-2 mb-1.5">
              <ImpactIcon className="w-4 h-4 shrink-0" />
              <span className="text-xs font-bold uppercase tracking-wider">
                {impact.level} ANALYTICS
              </span>
            </div>
            <div className="grid grid-cols-2 gap-3 text-xs mb-2">
              <div>
                <span className="opacity-60 block text-[10px]">AUTH FRICTION</span>
                <strong className="font-bold">{impact.lockoutRate}</strong>
              </div>
              <div>
                <span className="opacity-60 block text-[10px]">RULE VERDICT</span>
                <strong className="font-bold">{currentResult.action}</strong>
              </div>
            </div>
            <p className="text-[10px] opacity-80 leading-relaxed border-t border-current/15 pt-2">
              {impact.advice}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
