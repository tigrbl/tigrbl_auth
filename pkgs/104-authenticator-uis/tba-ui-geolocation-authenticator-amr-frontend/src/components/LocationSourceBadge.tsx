import React from 'react';
import { EvidenceSourceState, LocationSource } from '../types';
import { ShieldCheck, ShieldAlert, Ban, Clock, EyeOff, Radio, Laptop, Network, MapPin, Milestone } from 'lucide-react';

interface LocationSourceBadgeProps {
  sourceType: LocationSource['type'] | string;
  state?: EvidenceSourceState;
  showIcon?: boolean;
}

export const LocationSourceBadge: React.FC<LocationSourceBadgeProps> = ({
  sourceType,
  state,
  showIcon = true
}) => {
  const getSourceConfig = (type: string) => {
    switch (type) {
      case 'device':
        return {
          label: 'Device GPS',
          icon: MapPin,
          bg: 'bg-indigo-50 border-indigo-200 text-indigo-700 dark:bg-indigo-950/30 dark:border-indigo-800 dark:text-indigo-300',
          desc: 'High-accuracy on-device satellite coordinates'
        };
      case 'enterprise_zone':
        return {
          label: 'Corporate Zone',
          icon: Milestone,
          bg: 'bg-emerald-50 border-emerald-200 text-emerald-700 dark:bg-emerald-950/30 dark:border-emerald-800 dark:text-emerald-300',
          desc: 'Secured enterprise networking perimeter'
        };
      case 'managed_posture':
        return {
          label: 'Managed Posture',
          icon: Laptop,
          bg: 'bg-blue-50 border-blue-200 text-blue-700 dark:bg-blue-950/30 dark:border-blue-800 dark:text-blue-300',
          desc: 'MDM validated corporate device signal'
        };
      case 'network':
        return {
          label: 'Carrier Network',
          icon: Network,
          bg: 'bg-amber-50 border-amber-200 text-amber-700 dark:bg-amber-950/30 dark:border-amber-800 dark:text-amber-300',
          desc: 'Coarse regional ISP-derived location'
        };
      case 'trusted_upstream':
        return {
          label: 'Trusted Upstream',
          icon: Radio,
          bg: 'bg-purple-50 border-purple-200 text-purple-700 dark:bg-purple-950/30 dark:border-purple-800 dark:text-purple-300',
          desc: 'Upstream IDP signed location claims'
        };
      default:
        return {
          label: sourceType || 'Unknown Source',
          icon: ShieldAlert,
          bg: 'bg-gray-50 border-gray-200 text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-300',
          desc: 'Unregistered evidence class'
        };
    }
  };

  const getStateConfig = (s: EvidenceSourceState) => {
    switch (s) {
      case 'active':
        return {
          label: 'Active',
          bg: 'bg-emerald-100 text-emerald-800 border-emerald-300 dark:bg-emerald-950/40 dark:text-emerald-300 dark:border-emerald-800',
          icon: ShieldCheck
        };
      case 'draft':
        return {
          label: 'Draft',
          bg: 'bg-sky-100 text-sky-800 border-sky-300 dark:bg-sky-950/40 dark:text-sky-300 dark:border-sky-800',
          icon: ShieldAlert
        };
      case 'degraded':
        return {
          label: 'Degraded',
          bg: 'bg-amber-100 text-amber-800 border-amber-300 dark:bg-amber-950/40 dark:text-amber-300 dark:border-amber-800',
          icon: ShieldAlert
        };
      case 'suspended':
        return {
          label: 'Suspended',
          bg: 'bg-orange-100 text-orange-800 border-orange-300 dark:bg-orange-950/40 dark:text-orange-300 dark:border-orange-800',
          icon: Ban
        };
      case 'revoked':
        return {
          label: 'Revoked',
          bg: 'bg-rose-100 text-rose-800 border-rose-300 dark:bg-rose-950/40 dark:text-rose-300 dark:border-rose-800',
          icon: EyeOff
        };
      case 'expired':
        return {
          label: 'Expired',
          bg: 'bg-gray-100 text-gray-800 border-gray-300 dark:bg-gray-800 dark:text-gray-300 dark:border-gray-700',
          icon: Clock
        };
      case 'deleted':
        return {
          label: 'Deleted',
          bg: 'bg-red-100 text-red-800 border-red-300 dark:bg-red-950/40 dark:text-red-300 dark:border-red-800',
          icon: Ban
        };
      default:
        return {
          label: s,
          bg: 'bg-gray-100 text-gray-800 border-gray-300 dark:bg-gray-800 dark:text-gray-300 dark:border-gray-700',
          icon: ShieldAlert
        };
    }
  };

  const sourceConfig = getSourceConfig(sourceType);
  const SourceIcon = sourceConfig.icon;

  return (
    <div className="inline-flex flex-wrap items-center gap-1.5" role="group" aria-label={`Location source: ${sourceConfig.label}`}>
      <span
        title={sourceConfig.desc}
        className={`inline-flex items-center gap-1 px-2.5 py-1 text-xs font-medium rounded-md border ${sourceConfig.bg}`}
      >
        {showIcon && <SourceIcon className="w-3.5 h-3.5" aria-hidden="true" />}
        <span>{sourceConfig.label}</span>
      </span>

      {state && (() => {
        const stateConfig = getStateConfig(state);
        const StateIcon = stateConfig.icon;
        return (
          <span
            title={`State is ${stateConfig.label}`}
            className={`inline-flex items-center gap-1 px-2 py-0.5 text-[10px] tracking-wide uppercase font-semibold rounded-full border ${stateConfig.bg}`}
          >
            {showIcon && <StateIcon className="w-2.5 h-2.5" aria-hidden="true" />}
            <span>{stateConfig.label}</span>
          </span>
        );
      })()}
    </div>
  );
};
