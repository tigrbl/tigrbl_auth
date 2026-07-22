/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { AlertCircle, HelpCircle, ShieldAlert, Monitor, ArrowRight, RefreshCw, HelpCircle as HelpIcon } from 'lucide-react';
import { SimMode } from '../types';

interface ManagedEnvironmentNoticeProps {
  errorCode: SimMode;
  errorMessage: string;
  onRetry: () => void;
  onFallbackLocal: () => void;
  onFallbackFederation: () => void;
}

export default function ManagedEnvironmentNotice({
  errorCode,
  errorMessage,
  onRetry,
  onFallbackLocal,
  onFallbackFederation,
}: ManagedEnvironmentNoticeProps) {

  const getErrorDetail = () => {
    switch (errorCode) {
      case 'unsupported_browser':
        return {
          title: 'Unsupported or Unconfigured Browser',
          icon: <Monitor className="w-6 h-6 text-rose-600" />,
          desc: 'Your browser is not configured to send your Windows Kerberos credentials to this application zone. Group Policy or local trust settings are missing.',
          recommend: 'Please use a managed corporate browser (such as Microsoft Edge or Google Chrome with Integrated Authentication policy enabled).',
          code: 'ERR_WIA_BROWSER_POLICY_RESTRICTED',
        };
      case 'unmanaged_device':
        return {
          title: 'Unmanaged Device Network Location',
          icon: <ShieldAlert className="w-6 h-6 text-rose-600" />,
          desc: 'Windows Integrated Authentication requires a direct, secure connection to the local Active Directory Domain Controller / Key Distribution Center (KDC).',
          recommend: 'Please verify that your enterprise VPN is connected or that you are signed in on a managed corporate network.',
          code: 'ERR_WIA_KDC_UNREACHABLE_ON_EXT_NET',
        };
      case 'private_mode':
        return {
          title: 'Private Browsing Restrictions',
          icon: <ShieldAlert className="w-6 h-6 text-rose-600" />,
          desc: 'Your web browser is currently in Private, Incognito, or Ephemeral mode. Device-linked identity handshakes are disabled to protect your anonymity.',
          recommend: 'Please reopen this enterprise portal in a normal browser tab to sign in automatically.',
          code: 'ERR_WIA_EPHEMERAL_WINDOW_RESTRICTION',
        };
      case 'clock_skew':
        return {
          title: 'Workstation System Clock Skew',
          icon: <AlertCircle className="w-6 h-6 text-rose-600" />,
          desc: 'Kerberos authentication relies on strict synchronization of time. The clock skew between your system and the Domain Controller exceeds the allowed limit (5 minutes).',
          recommend: 'Please synchronize your computer clock with the domain time server (w32time) and reload.',
          code: 'KRB_AP_ERR_SKEW_EXCEEDED (0x25)',
        };
      case 'domain_mismatch':
        return {
          title: 'Enterprise Realm / Domain Mismatch',
          icon: <ShieldAlert className="w-6 h-6 text-rose-600" />,
          desc: 'The Active Directory realm presented by your workstation is not configured or verified for this enterprise tenant.',
          recommend: 'Ensure you are logging into the correct tenant gateway or contact your global tenant administrator to register the domain.',
          code: 'ERR_WIA_REALM_TENANT_NOT_VERIFIED',
        };
      case 'ambiguous_mapping':
        return {
          title: 'Ambiguous Account Identifier Mapping',
          icon: <HelpCircle className="w-6 h-6 text-rose-600" />,
          desc: 'The Kerberos ticket claims mapped to multiple local account identifiers. Auto-linking is prohibited to prevent account takeover.',
          recommend: 'Please sign in with a different factor or request a manual administrative verification.',
          code: 'ERR_WIA_AMBIGUOUS_SUBJECT_MAPPING',
        };
      case 'account_denied':
        return {
          title: 'Enterprise Account Restricted',
          icon: <ShieldAlert className="w-6 h-6 text-rose-600" />,
          desc: 'Your active workstation session was verified, but your enterprise directory account is currently locked, expired, or suspended.',
          recommend: 'Contact your corporate IT helpdesk to resolve account lockouts or expired passwords.',
          code: 'ERR_WIA_AD_ACCOUNT_SUSPENDED',
        };
      case 'spn_failure':
        return {
          title: 'Service Principal Name (SPN) Error',
          icon: <AlertCircle className="w-6 h-6 text-rose-600" />,
          desc: 'The target SPN representing this web portal does not exist, is mapped to multiple accounts, or lacks correct Service Account registration in AD.',
          recommend: 'This is an administrative directory error. Operator attention is required to register correct SPN attributes.',
          code: 'KRB_ERR_S_PRINCIPAL_UNKNOWN (0x7)',
        };
      case 'trust_failure':
        return {
          title: 'Active Directory Trust Path Expired',
          icon: <ShieldAlert className="w-6 h-6 text-rose-600" />,
          desc: 'The cryptographic trust connection between this cloud tenant and your local Windows Active Directory forest has failed verification.',
          recommend: 'Please contact platform operations to refresh the cross-realm federation trust.',
          code: 'ERR_WIA_REALM_TRUST_FAILURE',
        };
      case 'provider_timeout':
        return {
          title: 'Active Directory Connection Timeout',
          icon: <AlertCircle className="w-6 h-6 text-rose-600" />,
          desc: 'The identity provider failed to verify your workstation ticket because the corporate Domain Controller / LDAP service timed out.',
          recommend: 'Please try again in a few moments, or check corporate network status boards.',
          code: 'ERR_WIA_PROVIDER_BACKEND_TIMEOUT',
        };
      case 'credential_replay':
        return {
          title: 'Kerberos Token Replay Detected',
          icon: <ShieldAlert className="w-6 h-6 text-rose-600" />,
          desc: 'A duplicate, stale, or replayed Kerberos authenticator token was received by the security validation engine.',
          recommend: 'Please refresh the page to obtain a fresh ticket from your workstation ticket cache.',
          code: 'KRB_AP_ERR_REPEAT_REPLAY (0x22)',
        };
      case 'proxy_stripped':
        return {
          title: 'HTTP Proxy Negotiation Header Stripping',
          icon: <ShieldAlert className="w-6 h-6 text-rose-600" />,
          desc: 'The WWW-Authenticate/Authorization Negotiate header handshake was blocked, stripped, or altered by an intermediary network proxy or secure gateway.',
          recommend: 'Configure your network proxy to allow Negotiate/Ntlm header forwarding, or use an external login backup method.',
          code: 'ERR_WIA_HTTP_PROXY_STRIPPED_HEADERS',
        };
      default:
        return {
          title: 'Windows Integrated Sign-In Unavailable',
          icon: <AlertCircle className="w-6 h-6 text-rose-600" />,
          desc: 'Your workstation could not be automatically authenticated using local Windows credentials.',
          recommend: 'You can attempt to retry the handshake or select another approved company login factor.',
          code: 'ERR_WIA_GENERIC_NEGOTIATION_FAILED',
        };
    }
  };

  const detail = getErrorDetail();

  return (
    <div id="managed-env-notice" className="w-full max-w-md bg-white rounded-2xl border border-rose-100 shadow-xl overflow-hidden animate-fadeIn">
      {/* Banner / Error Header */}
      <div className="p-6 pb-4 bg-gradient-to-br from-rose-50 to-rose-100/40 border-b border-rose-100 flex gap-4">
        <div className="w-12 h-12 rounded-xl bg-rose-50 border border-rose-200 flex items-center justify-center shrink-0 shadow-xs">
          {detail.icon}
        </div>
        <div>
          <span className="text-[10px] font-mono font-semibold text-rose-600 tracking-wider uppercase bg-rose-50 border border-rose-200 px-1.5 py-0.5 rounded">
            {detail.code}
          </span>
          <h2 className="font-display text-lg font-bold text-rose-950 mt-1.5">
            {detail.title}
          </h2>
        </div>
      </div>

      {/* Detail Body */}
      <div className="p-6 space-y-5">
        <p className="text-sm text-slate-600 leading-relaxed">
          {detail.desc}
        </p>

        <div className="p-3 bg-slate-50 border border-slate-100 rounded-lg text-xs text-slate-600 leading-relaxed flex gap-2">
          <HelpIcon className="w-4 h-4 text-slate-400 shrink-0 mt-0.5" />
          <span>
            <strong>Resolution Guidance:</strong> {detail.recommend}
          </span>
        </div>

        {/* Fallbacks */}
        <div className="space-y-3 pt-2">
          <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-500">
            Approved Enterprise Fallbacks
          </h3>

          <div className="space-y-2">
            {/* OIDC/SAML IdP */}
            <button
              onClick={onFallbackFederation}
              id="btn-fallback-fed"
              className="w-full py-3 px-4 bg-slate-900 hover:bg-slate-800 text-white rounded-lg text-xs font-semibold transition-all flex items-center justify-between cursor-pointer"
            >
              <span>Federated Portal Sign-In (Microsoft Entra / Okta)</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>

            {/* Standard Credential Backup */}
            <button
              onClick={onFallbackLocal}
              id="btn-fallback-local"
              className="w-full py-2.5 px-4 bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 rounded-lg text-xs font-medium transition-all flex items-center justify-between cursor-pointer"
            >
              <span>Standard Workplace Password & OTP Factor</span>
              <ArrowRight className="w-3.5 h-3.5 text-slate-400" />
            </button>
          </div>
        </div>
      </div>

      {/* Actions Footer */}
      <div className="px-6 py-4 bg-slate-50 border-t border-slate-100 flex items-center justify-between">
        <button
          onClick={onRetry}
          id="btn-retry-wia"
          className="text-xs font-semibold text-blue-600 hover:text-blue-700 flex items-center gap-1 cursor-pointer"
        >
          <RefreshCw className="w-3 h-3" /> Re-attempt Windows Authentication
        </button>
        <span className="text-[10px] text-slate-400 font-mono">Secured Auth Payload</span>
      </div>
    </div>
  );
}
