import React, { useState } from 'react';
import { SmartCard, AuditLog } from '../types';
import { SmartCardPreflight } from './SmartCardPreflight';
import { CertificateSelectorHandoff } from './CertificateSelectorHandoff';
import { 
  Key, ShieldAlert, Cpu, CheckCircle, RefreshCw, AlertTriangle, 
  HelpCircle, ChevronRight, CornerDownRight, ArrowRight, ClipboardList, Info
} from 'lucide-react';

interface CeremonyShellProps {
  cards: SmartCard[];
  browserCompatible: boolean;
  middlewareRunning: boolean;
  readerConnected: boolean;
  cardInserted: boolean;
  selectedReaderName: string;
  onRefreshHardware: () => void;
  trustOutage: boolean; // simulated state
  onLogIncident: (log: Omit<AuditLog, 'id' | 'timestamp'>) => void;
  onAuthSuccess: (card: SmartCard) => void;
}

export const CeremonyShell: React.FC<CeremonyShellProps> = ({
  cards,
  browserCompatible,
  middlewareRunning,
  readerConnected,
  cardInserted,
  selectedReaderName,
  onRefreshHardware,
  trustOutage,
  onLogIncident,
  onAuthSuccess,
}) => {
  const [ceremonyStep, setCeremonyStep] = useState<'welcome' | 'confirm' | 'progress' | 'success' | 'failed'>('welcome');
  const [purpose, setPurpose] = useState<'login' | 'step-up'>('login');
  const [isOsPromptOpen, setIsOsPromptOpen] = useState(false);
  const [activeCard, setActiveCard] = useState<SmartCard | null>(null);
  
  // Ceremony Progress Checklist
  const [progress, setProgress] = useState<{ step: string; status: 'pending' | 'active' | 'pass' | 'fail' }[]>([
    { step: 'Local reader and middleware compatibility check', status: 'pending' },
    { step: 'OS certificate selection projection', status: 'pending' },
    { step: 'On-chip PIN authentication validation', status: 'pending' },
    { step: 'PKCS#11 RSA-2048 cryptographic signature proof', status: 'pending' },
    { step: 'Trust anchor certificate chain validation (PIV/CAC policy)', status: 'pending' },
    { step: 'Real-time revocation check (OCSP/CRL verify)', status: 'pending' },
  ]);

  const [failureReason, setFailureReason] = useState({ title: '', desc: '', action: '' });

  const handleStartCeremony = (type: 'login' | 'step-up') => {
    setPurpose(type);
    
    // Check preflight before proceeding
    if (!browserCompatible || !middlewareRunning || !readerConnected || !cardInserted) {
      setFailureReason({
        title: 'Hardware Preflight Block',
        desc: 'One or more local smart card components are missing. Check compatibility alerts.',
        action: 'Ensure your reader is connected, card is inserted, and middleware is running.'
      });
      setCeremonyStep('failed');
      onLogIncident({
        event: 'sc.auth.preflight.failed',
        actor: 'PRE-AUTHENTICATION',
        status: 'failure',
        details: 'Preflight checklist failed. Reader connected: ' + readerConnected + ', Card inserted: ' + cardInserted,
        ipAddress: '127.0.0.1'
      });
      return;
    }

    setCeremonyStep('confirm');
  };

  const handleLaunchCertSelection = () => {
    setIsOsPromptOpen(true);
  };

  const handleSelectCertificate = (selectedCard: SmartCard, pin: string) => {
    setIsOsPromptOpen(false);
    setActiveCard(selectedCard);
    setCeremonyStep('progress');

    // Reset progress steps
    const updatedProgress = progress.map((p, idx) => ({
      ...p,
      status: idx === 0 ? 'pass' as const : 'pending' as const
    }));
    setProgress(updatedProgress);

    // Run simulated steps with timeouts
    runSimulatedVerification(selectedCard, updatedProgress);
  };

  const runSimulatedVerification = (
    selectedCard: SmartCard, 
    initialProgress: typeof progress
  ) => {
    let currentIdx = 1;

    const interval = setInterval(() => {
      if (currentIdx >= initialProgress.length) {
        clearInterval(interval);
        
        // Final evaluation based on card status and simulated trust outage
        evaluateFinalStatus(selectedCard);
        return;
      }

      // If we are about to check trust anchor chain & revocation check, respect the simulated "trustOutage"
      if (currentIdx === 4 && trustOutage) {
        clearInterval(interval);
        setProgress(prev => prev.map((p, idx) => {
          if (idx === 4) return { ...p, status: 'fail' };
          if (idx > 4) return { ...p, status: 'pending' };
          return p;
        }));
        
        setFailureReason({
          title: 'Trust Service Connection Outage',
          desc: 'The cryptographic system was unable to contact the designated Root CA status or OCSP validation responder endpoint.',
          action: 'Contact organization trust desk or retry authentication when status service becomes operational.'
        });
        setCeremonyStep('failed');
        onLogIncident({
          event: 'sc.trust.outage.failure',
          actor: selectedCard.subject.split(',')[0],
          status: 'warning',
          cardFingerprint: selectedCard.fingerprint.slice(0, 16) + '...',
          details: 'Unable to query OCSP/CRL trust lists due to simulated network service outage.',
          ipAddress: '10.142.0.4'
        });
        return;
      }

      // Check for specific card flaws during progress
      if (currentIdx === 4 && selectedCard.status === 'expired') {
        clearInterval(interval);
        setProgress(prev => prev.map((p, idx) => {
          if (idx === 4) return { ...p, status: 'fail' };
          return p;
        }));
        setFailureReason({
          title: 'Certificate Chain Validation Failed: EXPIRED',
          desc: `The public certificate expired on ${new Date(selectedCard.notAfter).toLocaleDateString()}. The system prevents expired credentials from completing authorization.`,
          action: 'Your smart card is inactive. Please initiate card renewal or replacement.'
        });
        setCeremonyStep('failed');
        onLogIncident({
          event: 'sc.auth.expired',
          actor: selectedCard.subject.split(',')[0],
          status: 'failure',
          cardFingerprint: selectedCard.fingerprint.slice(0, 16) + '...',
          details: `Authentication blocked. Token expired on ${selectedCard.notAfter}`,
          ipAddress: '10.142.0.4'
        });
        return;
      }

      if (currentIdx === 4 && selectedCard.eku.length === 1 && selectedCard.eku[0].includes('Secure Email')) {
        // Wrong profile
        clearInterval(interval);
        setProgress(prev => prev.map((p, idx) => {
          if (idx === 4) return { ...p, status: 'fail' };
          return p;
        }));
        setFailureReason({
          title: 'Policy Enforcement Error: Invalid EKU Profile',
          desc: 'The selected certificate does not support the required Extended Key Usage (EKU) fields. Client Authentication (1.3.6.1.5.5.7.3.2) or Smartcard Logon (1.3.6.1.4.1.311.20.2.2) is missing.',
          action: 'Make sure you selected your cryptographic PIV/CAC certificate and not your personal S/MIME email signature.'
        });
        setCeremonyStep('failed');
        onLogIncident({
          event: 'sc.policy.eku.missing',
          actor: selectedCard.subject.split(',')[0],
          status: 'failure',
          cardFingerprint: selectedCard.fingerprint.slice(0, 16) + '...',
          details: 'EKU check failed. Certificate lacks 1.3.6.1.5.5.7.3.2 clientAuth signature.',
          ipAddress: '10.142.0.4'
        });
        return;
      }

      if (currentIdx === 5 && selectedCard.status === 'revoked') {
        clearInterval(interval);
        setProgress(prev => prev.map((p, idx) => {
          if (idx === 5) return { ...p, status: 'fail' };
          return p;
        }));
        setFailureReason({
          title: 'Certificate Revocation Check: CARD REVOKED',
          desc: 'The trust responder verified this certificate serial number has been blacklisted on the FPKI CRL. Reason: KeyCompromise / Terminated Access.',
          action: 'Access denied. The token has been decommissioned. Supervised credential recovery is required.'
        });
        setCeremonyStep('failed');
        onLogIncident({
          event: 'sc.auth.revoked',
          actor: selectedCard.subject.split(',')[0],
          status: 'failure',
          cardFingerprint: selectedCard.fingerprint.slice(0, 16) + '...',
          details: 'Revocation list lookup verified certificate revoked (CRL reason: KeyCompromise).',
          ipAddress: '10.142.0.4'
        });
        return;
      }

      // Mark current pass, make next active
      setProgress(prev => prev.map((p, idx) => {
        if (idx === currentIdx) return { ...p, status: 'pass' };
        if (idx === currentIdx + 1) return { ...p, status: 'active' };
        return p;
      }));

      currentIdx++;
    }, 700);
  };

  const evaluateFinalStatus = (card: SmartCard) => {
    // If we made it past all checks, evaluate status
    if (card.status === 'active' || card.status === 'expiring') {
      setCeremonyStep('success');
      onAuthSuccess(card);
      onLogIncident({
        event: purpose === 'login' ? 'sc.auth.success' : 'sc.stepup.success',
        actor: card.subject.split(',')[0],
        status: 'success',
        cardFingerprint: card.fingerprint.slice(0, 16) + '...',
        details: `Cryptographic proof complete (${purpose === 'login' ? 'primary auth' : 'action authorization'}). Status: ${card.status}.`,
        ipAddress: '10.142.0.4'
      });
    } else {
      // General fallbacks if any other state
      setFailureReason({
        title: 'Authentication Rejected',
        desc: `The smart card status is listed as '${card.status}'. Access policies forbid authentication with non-active hardware profiles.`,
        action: 'Insert an authorized active PIV/CAC token to proceed.'
      });
      setCeremonyStep('failed');
    }
  };

  const handleResetCeremony = () => {
    setActiveCard(null);
    setCeremonyStep('welcome');
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 text-slate-100 flex flex-col justify-between h-full shadow-md" id="ceremony-shell">
      {/* Top Header */}
      <div className="border-b border-slate-800 pb-4 mb-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Key className="w-5 h-5 text-indigo-400" />
            <h2 className="text-base font-bold tracking-tight text-white">Smart-Card Possession Ceremony</h2>
          </div>
          <span className="text-[10px] font-mono tracking-wider font-semibold px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-300 border border-indigo-500/20">
            AMR: sc
          </span>
        </div>
      </div>

      {/* Main step switcher */}
      <div className="flex-1 flex flex-col justify-center min-h-[340px]">
        {ceremonyStep === 'welcome' && (
          <div className="space-y-5 py-4">
            <div className="text-center">
              <div className="inline-flex p-4 bg-indigo-500/10 rounded-full border border-indigo-500/20 text-indigo-400 mb-3 animate-pulse">
                <Cpu className="w-8 h-8" />
              </div>
              <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider">PIV/CAC Identity Challenge</h3>
              <p className="text-xs text-slate-400 max-w-sm mx-auto mt-2 leading-relaxed">
                Provide secure possession proof via high-assurance hardware certificate token.
              </p>
            </div>

            {/* Quick preflight checklist preview */}
            <div className="bg-slate-950/50 p-4 rounded-lg border border-slate-800/80 max-w-md mx-auto space-y-2.5">
              <div className="text-[10px] uppercase font-bold tracking-wider text-slate-500 flex items-center gap-1">
                <ClipboardList className="w-3.5 h-3.5 text-indigo-400" />
                Reader Check
              </div>
              <div className="grid grid-cols-2 gap-2 text-xs">
                <div className="flex items-center gap-1.5 text-slate-300">
                  <span className={`h-1.5 w-1.5 rounded-full ${readerConnected ? 'bg-emerald-400' : 'bg-rose-400'}`}></span>
                  Reader: <span className="font-semibold text-slate-200">{readerConnected ? 'OK' : 'None'}</span>
                </div>
                <div className="flex items-center gap-1.5 text-slate-300">
                  <span className={`h-1.5 w-1.5 rounded-full ${cardInserted ? 'bg-emerald-400' : 'bg-rose-400'}`}></span>
                  Token Card: <span className="font-semibold text-slate-200">{cardInserted ? 'OK' : 'Absent'}</span>
                </div>
              </div>
            </div>

            <div className="flex flex-col sm:flex-row gap-3 max-w-md mx-auto pt-2">
              <button
                onClick={() => handleStartCeremony('login')}
                className="flex-1 py-3 px-4 rounded-lg text-xs font-bold bg-indigo-600 hover:bg-indigo-700 text-white shadow-sm flex items-center justify-center gap-2 hover:shadow-indigo-500/10 transition-all active:scale-98"
                id="btn-start-sc-login"
              >
                Sign In with Smart Card
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
              <button
                onClick={() => handleStartCeremony('step-up')}
                className="flex-1 py-3 px-4 rounded-lg text-xs font-bold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 flex items-center justify-center gap-2 transition-all active:scale-98"
                id="btn-start-sc-stepup"
              >
                Sensitive Action Step-Up
                <ShieldAlert className="w-3.5 h-3.5 text-amber-400" />
              </button>
            </div>
            
            <p className="text-center text-[10px] text-slate-500 leading-relaxed max-w-xs mx-auto">
              Compatible with DoD Common Access Cards, PIV agency credentials, and PKCS#11 hardware keys.
            </p>
          </div>
        )}

        {ceremonyStep === 'confirm' && (
          <div className="space-y-5 py-3">
            <div className="p-4 bg-amber-500/10 border border-amber-500/20 rounded-lg text-slate-300 text-xs">
              <div className="flex gap-2 items-start">
                <Info className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                <div className="space-y-1">
                  <span className="font-bold text-white uppercase tracking-wider text-[10px]">Transaction Intent Confirmation</span>
                  <p className="text-slate-300 leading-relaxed mt-0.5">
                    {purpose === 'login' ? (
                      <span>You are requesting a secure login session to <span className="font-semibold text-indigo-300">Production Console Ingress</span>. This will submit a cryptographic proof signed by your smart-card private key.</span>
                    ) : (
                      <span>You are performing high-privilege action <span className="font-semibold text-rose-300">"REVOKE_ALL_SESSION_ROOT"</span>. This requires immediate step-up cryptographic confirmation of your PIV/CAC possession factor.</span>
                    )}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-slate-950 p-4 rounded-lg border border-slate-800 space-y-2.5 max-w-md mx-auto">
              <div className="text-[10px] font-bold text-slate-500 uppercase">Interactive Steps Overview:</div>
              <div className="space-y-1.5 text-xs text-slate-400">
                <div className="flex items-center gap-1.5">
                  <span className="w-4 h-4 rounded-full bg-indigo-500/20 text-indigo-400 text-[10px] font-bold flex items-center justify-center shrink-0">1</span>
                  <span>Invoke browser mTLS OS keychain selector</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <span className="w-4 h-4 rounded-full bg-indigo-500/20 text-indigo-400 text-[10px] font-bold flex items-center justify-center shrink-0">2</span>
                  <span>Input 4-8 digit hardware PIN on device</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <span className="w-4 h-4 rounded-full bg-indigo-500/20 text-indigo-400 text-[10px] font-bold flex items-center justify-center shrink-0">3</span>
                  <span>Confirm touch capability (if token-backed)</span>
                </div>
              </div>
            </div>

            <div className="flex gap-2 max-w-xs mx-auto">
              <button
                onClick={handleResetCeremony}
                className="flex-1 py-2 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition-colors"
                id="btn-ceremony-cancel"
              >
                Cancel
              </button>
              <button
                onClick={handleLaunchCertSelection}
                className="flex-1 py-2 rounded-lg text-xs font-bold bg-indigo-600 hover:bg-indigo-700 text-white shadow-sm transition-colors"
                id="btn-ceremony-invoke"
              >
                Launch Selector
              </button>
            </div>
          </div>
        )}

        {ceremonyStep === 'progress' && (
          <div className="space-y-5 max-w-md mx-auto py-2">
            <div className="text-center">
              <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest animate-pulse">CRYPTOGRAPHIC CHALLENGE IN PROGRESS</h4>
              <p className="text-[10px] text-slate-500 font-mono mt-1">Challenge token: {activeCard ? activeCard.serialNumber : ''}</p>
            </div>

            <div className="space-y-2 bg-slate-950 p-4 rounded-lg border border-slate-800">
              {progress.map((step, idx) => (
                <div key={idx} className="flex items-start gap-2.5 text-[11px] leading-relaxed">
                  <div className="mt-1 shrink-0">
                    {step.status === 'pass' && <span className="h-2 w-2 rounded-full bg-emerald-400 block shadow-emerald-400/50 shadow-sm animate-pulse"></span>}
                    {step.status === 'active' && <span className="h-2 w-2 rounded-full bg-indigo-500 block animate-ping"></span>}
                    {step.status === 'pending' && <span className="h-2 w-2 rounded-full bg-slate-700 block"></span>}
                    {step.status === 'fail' && <span className="h-2 w-2 rounded-full bg-rose-500 block shadow-rose-500/50 shadow-sm"></span>}
                  </div>
                  <span className={`
                    ${step.status === 'pass' ? 'text-slate-300 line-through' : ''}
                    ${step.status === 'active' ? 'text-indigo-300 font-semibold' : ''}
                    ${step.status === 'pending' ? 'text-slate-600' : ''}
                    ${step.status === 'fail' ? 'text-rose-400 font-bold' : ''}
                  `}>
                    {step.step}
                  </span>
                </div>
              ))}
            </div>

            <div className="text-center text-[10px] text-slate-500">
              Cryptographic pipeline running over HTTPS client/server handshake...
            </div>
          </div>
        )}

        {ceremonyStep === 'success' && activeCard && (
          <div className="space-y-5 py-4 text-center">
            <div className="inline-flex p-3 bg-emerald-500/10 rounded-full border border-emerald-500/20 text-emerald-400">
              <CheckCircle className="w-8 h-8" />
            </div>
            
            <div className="space-y-1">
              <h3 className="text-sm font-bold text-white uppercase tracking-wider">Possession Verified Successfully</h3>
              <p className="text-xs text-slate-400 leading-relaxed max-w-sm mx-auto">
                {purpose === 'login' ? 'Authentication successful. Smart-card credentials validated against security policy.' : 'Step-up approved. Action execution scope authorized.'}
              </p>
            </div>

            {/* Authenticated token properties */}
            <div className="bg-slate-950 p-4 rounded-lg border border-slate-800 text-left space-y-2 text-xs max-w-sm mx-auto">
              <div className="flex justify-between pb-1.5 border-b border-slate-800">
                <span className="text-slate-500 font-medium">Verified Identity</span>
                <span className="text-slate-300 font-mono truncate max-w-[180px] font-bold">
                  {activeCard.subject.split(',')[0].replace('CN=', '')}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Authenticating Factor</span>
                <span className="text-slate-300 font-mono text-[10px]">sc (Smart Card Certificate)</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Token Type / CSP</span>
                <span className="text-slate-300">{activeCard.hardware.cardType} / PKCS#11</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Authority Issuer</span>
                <span className="text-slate-300 font-mono text-[10px] truncate max-w-[180px]">
                  {activeCard.issuer.split(',')[0].replace('CN=', '')}
                </span>
              </div>
            </div>

            <button
              onClick={handleResetCeremony}
              className="py-2.5 px-6 rounded-lg text-xs font-semibold bg-emerald-600 hover:bg-emerald-700 text-white shadow-sm transition-colors"
              id="btn-ceremony-done"
            >
              Close Ceremony Panel
            </button>
          </div>
        )}

        {ceremonyStep === 'failed' && (
          <div className="space-y-5 py-4">
            <div className="text-center">
              <div className="inline-flex p-3 bg-rose-500/10 rounded-full border border-rose-500/20 text-rose-400 mb-2">
                <ShieldAlert className="w-8 h-8" />
              </div>
              <h3 className="text-sm font-bold text-white uppercase tracking-wider">{failureReason.title}</h3>
              <p className="text-xs text-rose-300 max-w-md mx-auto mt-2 leading-relaxed">
                {failureReason.desc}
              </p>
            </div>

            <div className="p-3.5 bg-slate-950/60 rounded-lg border border-slate-800 flex gap-2.5 text-xs text-slate-400">
              <AlertTriangle className="w-4.5 h-4.5 text-amber-500 shrink-0 mt-0.5" />
              <div>
                <span className="font-semibold text-slate-300">Suggested Mitigation Action:</span>
                <p className="text-[11px] leading-relaxed mt-0.5 text-slate-400">{failureReason.action}</p>
              </div>
            </div>

            <div className="flex flex-col sm:flex-row gap-2 max-w-xs mx-auto">
              <button
                onClick={handleResetCeremony}
                className="flex-1 py-2 text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 rounded-lg transition-colors"
                id="btn-ceremony-retry"
              >
                Retry Selection
              </button>
              
              {/* Recovery trigger */}
              <button
                onClick={() => {
                  alert('Initiating identity-proofed recovery mechanism. In production, this redirects to a supervisor clearance portal, hardware bypass issuance, or physical enrollment office.');
                  onLogIncident({
                    event: 'sc.auth.recovery_flow.initiated',
                    actor: 'RECOVERY_ENGINE',
                    status: 'warning',
                    details: 'User initiated supervised recovery bypass flow. Action logged.',
                    ipAddress: '10.142.0.4'
                  });
                }}
                className="flex-1 py-2 text-xs font-semibold bg-indigo-950 hover:bg-indigo-900 border border-indigo-800 text-indigo-300 rounded-lg transition-colors"
                id="btn-ceremony-recovery"
              >
                Identity Recovery
              </button>
            </div>
          </div>
        )}
      </div>

      <CertificateSelectorHandoff
        cards={cards}
        isOpen={isOsPromptOpen}
        onSelect={handleSelectCertificate}
        onCancel={() => setIsOsPromptOpen(false)}
      />
    </div>
  );
};
