/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { 
  Plus, 
  Trash2, 
  ShieldAlert, 
  Fingerprint, 
  Key, 
  Smartphone, 
  Mail, 
  AlertCircle,
  QrCode,
  Check,
  RotateCcw,
  ShieldCheck,
  HelpCircle,
  Search,
  MoreVertical,
  Activity,
  UserCheck,
  Shield,
  Loader2,
  ChevronRight
} from 'lucide-react';
import { MfaFactor, FactorType, FactorClass, AuditEvent } from '../types';

interface MyAuthenticatorsProps {
  factors: MfaFactor[];
  onAddFactor: (factor: Omit<MfaFactor, 'id' | 'enrolledAt'>) => void;
  onRemoveFactor: (id: string) => void;
  onUpdateFactor: (id: string, updates: Partial<MfaFactor>) => void;
  addAuditEvent: (event: Omit<AuditEvent, 'id' | 'timestamp'>) => void;
}

export default function MyAuthenticators({
  factors,
  onAddFactor,
  onRemoveFactor,
  onUpdateFactor,
  addAuditEvent,
}: MyAuthenticatorsProps) {
  const [showEnrollModal, setShowEnrollModal] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  
  // Enrollment Wizard States
  const [enrollStep, setEnrollStep] = useState<'type' | 'verify' | 'complete'>('type');
  const [newFactorType, setNewFactorType] = useState<FactorType>('passkey');
  const [newFactorName, setNewFactorName] = useState('');
  const [totpSecret, setTotpSecret] = useState('');
  const [verificationCode, setVerificationCode] = useState('');
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);

  // Filter factors based on search
  const filteredFactors = factors.filter(f => 
    f.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    f.type.toLowerCase().includes(searchQuery.toLowerCase()) ||
    (f.deviceName && f.deviceName.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  const getFactorIcon = (type: FactorType) => {
    switch (type) {
      case 'passkey': return <Fingerprint className="w-5 h-5" />;
      case 'security_key': return <Key className="w-5 h-5" />;
      case 'totp': return <QrCode className="w-5 h-5" />;
      case 'push': return <Smartphone className="w-5 h-5" />;
      case 'email_otp': return <Mail className="w-5 h-5" />;
      default: return <Shield className="w-5 h-5" />;
    }
  };

  const startEnrollment = () => {
    setEnrollStep('type');
    setNewFactorName('');
    setErrorMsg(null);
    setNewFactorType('passkey');
    setShowEnrollModal(true);
  };

  const handleSelectType = (type: FactorType) => {
    setNewFactorType(type);
    
    // Auto-suggest default name
    const count = factors.filter(f => f.type === type).length + 1;
    let name = '';
    switch (type) {
      case 'passkey': name = `My Biometric Passkey ${count}`; break;
      case 'security_key': name = `YubiKey Token ${count}`; break;
      case 'totp': name = `Authenticator app ${count}`; break;
      case 'push': name = `Acme Push App ${count}`; break;
      case 'email_otp': name = `Backup Email ${count}`; break;
    }
    setNewFactorName(name);

    if (type === 'totp') {
      // Simulate random TOTP secret key
      const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567';
      let secret = '';
      for (let i = 0; i < 16; i++) {
        secret += chars.charAt(Math.floor(Math.random() * chars.length));
      }
      setTotpSecret(secret);
    }
    setEnrollStep('verify');
  };

  const handleVerifyEnrollment = () => {
    if (!newFactorName.trim()) {
      setErrorMsg('Please enter a descriptive name for this authenticator.');
      return;
    }

    if (newFactorType === 'totp' && verificationCode.length !== 6) {
      setErrorMsg('Please enter the 6-digit confirmation code from your authenticator app.');
      return;
    }

    setIsProcessing(true);
    setErrorMsg(null);

    // Simulate WebAuthn and network latency
    setTimeout(() => {
      setIsProcessing(false);

      // Create factor model
      let factorClass: FactorClass = 'Possession';
      let phishingResistant = false;
      let deviceName = 'Generic Web Client';

      if (newFactorType === 'passkey') {
        factorClass = 'Inherence';
        phishingResistant = true;
        deviceName = 'Apple TouchID / Windows Hello';
      } else if (newFactorType === 'security_key') {
        factorClass = 'Possession';
        phishingResistant = true;
        deviceName = 'YubiKey 5 NFC';
      } else if (newFactorType === 'push') {
        factorClass = 'Possession';
        phishingResistant = false;
        deviceName = 'iPhone 15 Pro';
      } else if (newFactorType === 'totp') {
        factorClass = 'Possession';
        phishingResistant = false;
        deviceName = 'Google Authenticator';
      } else if (newFactorType === 'email_otp') {
        factorClass = 'Possession';
        phishingResistant = false;
        deviceName = 'Email Address';
      }

      onAddFactor({
        type: newFactorType,
        name: newFactorName,
        factorClass,
        status: 'active',
        phishingResistant,
        deviceName,
        lastUsedAt: undefined,
      });

      addAuditEvent({
        eventType: 'FACTOR_ENROLLED',
        subject: 'jane.doe@acme.com',
        status: 'success',
        factorType: newFactorType,
        factorClass,
        detail: `Enrolled new authentication factor: ${newFactorName} (${factorClass})`,
        ipAddress: '192.168.1.45',
        userAgent: navigator.userAgent,
      });

      setEnrollStep('complete');
    }, 1200);
  };

  const handleRemoveFactor = (id: string, factor: MfaFactor) => {
    // Safety check: Cannot remove last remaining active factor if total factors <= 2 (including recovery)
    const activeMfaFactors = factors.filter(f => f.status === 'active' && f.type !== 'recovery');
    
    if (activeMfaFactors.length <= 1 && factor.type !== 'recovery') {
      alert('Security Enforcement Gate: You cannot delete your last enrolled MFA factor. Acme policies require at least one active MFA possession/inherence factor to prevent total account lockout.');
      
      addAuditEvent({
        eventType: 'FACTOR_DELETION_BLOCKED',
        subject: 'jane.doe@acme.com',
        status: 'warning',
        factorType: factor.type,
        detail: `Blocked attempt to delete the last active MFA factor: ${factor.name}`,
        ipAddress: '192.168.1.45',
        userAgent: navigator.userAgent,
      });
      return;
    }

    if (confirm(`Are you sure you want to remove "${factor.name}"? This action cannot be undone and will revoke its cryptographic binding.`)) {
      onRemoveFactor(id);
      addAuditEvent({
        eventType: 'FACTOR_REVOKED',
        subject: 'jane.doe@acme.com',
        status: 'warning',
        factorType: factor.type,
        detail: `Revoked and deleted authentication factor: ${factor.name}`,
        ipAddress: '192.168.1.45',
        userAgent: navigator.userAgent,
      });
    }
  };

  const toggleFactorStatus = (id: string, factor: MfaFactor) => {
    const nextStatus = factor.status === 'active' ? 'suspended' : 'active';
    
    // Safety check for suspension too
    if (nextStatus === 'suspended') {
      const activeFactorsCount = factors.filter(f => f.status === 'active' && f.type !== 'recovery').length;
      if (activeFactorsCount <= 1 && factor.type !== 'recovery') {
        alert('Security Enforcement Gate: You cannot suspend your only active MFA factor.');
        return;
      }
    }

    onUpdateFactor(id, { status: nextStatus });
    
    addAuditEvent({
      eventType: nextStatus === 'suspended' ? 'FACTOR_SUSPENDED' : 'FACTOR_UNSUSPENDED',
      subject: 'jane.doe@acme.com',
      status: nextStatus === 'suspended' ? 'warning' : 'success',
      factorType: factor.type,
      detail: `${nextStatus === 'suspended' ? 'Suspended' : 'Activated'} authentication factor: ${factor.name}`,
      ipAddress: '192.168.1.45',
      userAgent: navigator.userAgent,
    });
  };

  return (
    <div className="flex-1 p-6 overflow-y-auto animate-fade-in" id="factors-admin">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
        <div>
          <h1 className="text-xl font-bold text-slate-900 tracking-tight">Authenticator Inventory</h1>
          <p className="text-xs text-slate-500">Enrolled multi-factor assurances linked to your corporate profile.</p>
        </div>
        <button
          onClick={startEnrollment}
          className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-lg text-xs shadow-md shadow-indigo-100 flex items-center gap-1.5 transition-all self-start"
        >
          <Plus className="w-4 h-4" /> Enroll New Authenticator
        </button>
      </div>

      {/* Safety Compliance Metric Banner */}
      <div className="bg-emerald-50 border border-emerald-200/60 rounded-xl p-4 mb-6 flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-2xs">
        <div className="flex items-start gap-3">
          <div className="w-9 h-9 rounded-lg bg-emerald-100 text-emerald-700 flex items-center justify-center shrink-0">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <div>
            <h4 className="text-xs font-bold text-slate-800">Account Safety Evaluation: Healthy Assurance</h4>
            <p className="text-[11px] text-slate-500 max-w-xl mt-0.5">
              You have {factors.filter(f => f.status === 'active' && f.type !== 'recovery').length} active second-factor class(es) registered. If any hardware device is lost, you are configured with emergency offline master recovery codes.
            </p>
          </div>
        </div>
        <div className="flex gap-2">
          <span className="px-2.5 py-1 bg-white text-emerald-800 text-[10px] font-bold rounded-lg border border-emerald-200/50 flex items-center gap-1">
            <UserCheck className="w-3.5 h-3.5 text-emerald-500" /> Compliant
          </span>
        </div>
      </div>

      {/* Search Input */}
      <div className="mb-5 relative max-w-md">
        <Search className="w-4 h-4 absolute left-3 top-2.5 text-slate-400" />
        <input
          type="text"
          placeholder="Filter devices, tokens, or classes..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full bg-white border border-slate-200 rounded-lg pl-9 pr-4 py-1.5 text-xs text-slate-700 focus:outline-hidden focus:ring-2 focus:ring-indigo-500"
        />
      </div>

      {/* Factors Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" id="factors-grid">
        {filteredFactors.map((factor) => {
          const isActive = factor.status === 'active';
          const isRecovery = factor.type === 'recovery';

          return (
            <div 
              key={factor.id} 
              className={`bg-white border rounded-xl p-4 shadow-3xs flex flex-col justify-between transition-all relative ${
                isActive ? 'border-slate-200' : 'border-rose-100 bg-rose-50/20 opacity-75'
              }`}
            >
              {/* Factor Header */}
              <div className="flex items-start justify-between mb-3">
                <div className="flex gap-3">
                  <div className={`w-9 h-9 rounded-lg flex items-center justify-center ${
                    isActive 
                      ? 'bg-slate-100 text-slate-700' 
                      : 'bg-rose-100 text-rose-600'
                  }`}>
                    {getFactorIcon(factor.type)}
                  </div>
                  <div>
                    <h3 className="text-xs font-bold text-slate-800 flex items-center gap-1.5">
                      {factor.name}
                      {isRecovery && (
                        <span className="px-1.5 py-0.2 bg-amber-100 text-amber-800 text-[8px] font-bold rounded uppercase">
                          Recovery
                        </span>
                      )}
                    </h3>
                    <span className="text-[10px] text-slate-400 font-medium">
                      Class: {factor.factorClass}
                    </span>
                  </div>
                </div>

                <div className="flex items-center gap-1">
                  {factor.phishingResistant && (
                    <span className="px-1.5 py-0.5 bg-emerald-50 text-emerald-700 text-[8px] font-bold rounded border border-emerald-100">
                      Phishing Res.
                    </span>
                  )}
                </div>
              </div>

              {/* Factor Details */}
              <div className="bg-slate-50 rounded-lg p-2.5 space-y-1.5 text-[10px] text-slate-500 mb-4 font-mono">
                <div className="flex justify-between">
                  <span>Hardware Device:</span>
                  <span className="text-slate-700 truncate max-w-[120px]">{factor.deviceName || 'N/A'}</span>
                </div>
                <div className="flex justify-between">
                  <span>Cryptographic Mode:</span>
                  <span className="text-slate-700">{factor.phishingResistant ? 'Asymmetric WebAuthn' : 'HMAC-SHA1'}</span>
                </div>
                <div className="flex justify-between">
                  <span>Enrolled:</span>
                  <span className="text-slate-700">10 months ago</span>
                </div>
                <div className="flex justify-between">
                  <span>Status:</span>
                  <span className={`font-bold ${isActive ? 'text-emerald-600' : 'text-rose-600'}`}>
                    {factor.status.toUpperCase()}
                  </span>
                </div>
              </div>

              {/* Factor Actions */}
              <div className="flex gap-2 pt-2 border-t border-slate-100 mt-auto justify-end">
                <button
                  onClick={() => toggleFactorStatus(factor.id, factor)}
                  className={`px-2.5 py-1 text-[10px] font-bold rounded-md border transition-colors ${
                    isActive
                      ? 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50'
                      : 'bg-indigo-50 border-indigo-200 text-indigo-700 hover:bg-indigo-100'
                  }`}
                >
                  {isActive ? 'Suspend' : 'Activate'}
                </button>
                <button
                  onClick={() => handleRemoveFactor(factor.id, factor)}
                  disabled={isRecovery}
                  className={`p-1.5 rounded-md border text-slate-400 hover:text-rose-600 hover:bg-rose-50 border-slate-200 hover:border-rose-200 transition-colors ${isRecovery ? 'opacity-30 cursor-not-allowed' : ''}`}
                  title={isRecovery ? "Recovery codes cannot be deleted" : "Delete factor"}
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {/* Enrollment Wizard Modal */}
      {showEnrollModal && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center z-50 p-4" id="enrollment-modal">
          <div className="bg-white rounded-2xl w-full max-w-md border border-slate-200 shadow-xl overflow-hidden animate-fade-in flex flex-col max-h-[90vh]">
            {/* Modal Header */}
            <div className="p-4 bg-slate-50 border-b border-slate-100 flex justify-between items-center">
              <h2 className="text-sm font-bold text-slate-800 flex items-center gap-1.5">
                <Plus className="w-4 h-4 text-indigo-600" /> Authenticator Registration Flow
              </h2>
              <button 
                onClick={() => setShowEnrollModal(false)}
                className="text-slate-400 hover:text-slate-600 font-bold text-sm"
              >
                ✕
              </button>
            </div>

            {/* Modal Body */}
            <div className="p-5 flex-1 overflow-y-auto">
              {errorMsg && (
                <div className="bg-rose-50 border border-rose-200 text-rose-800 text-xs p-2.5 rounded-lg mb-4 flex items-start gap-2">
                  <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
                  <span>{errorMsg}</span>
                </div>
              )}

              {enrollStep === 'type' && (
                <div>
                  <h3 className="text-xs font-bold text-slate-700 mb-3">1. Select Factor Class & Authenticator Interface</h3>
                  <div className="space-y-2.5">
                    {/* Passkey Option */}
                    <div 
                      onClick={() => handleSelectType('passkey')}
                      className="p-3 border border-slate-200 rounded-xl hover:border-indigo-500 hover:bg-indigo-50/20 cursor-pointer transition-all flex items-center justify-between group"
                    >
                      <div className="flex gap-3">
                        <div className="w-8 h-8 rounded-full bg-indigo-50 text-indigo-600 flex items-center justify-center group-hover:bg-indigo-100 shrink-0">
                          <Fingerprint className="w-4 h-4" />
                        </div>
                        <div className="text-left">
                          <div className="text-xs font-bold text-slate-800 flex items-center gap-1.5">
                            Platform Biometric Passkey
                            <span className="px-1.5 py-0.2 bg-emerald-100 text-emerald-800 text-[8px] font-bold rounded uppercase">Phishing Res.</span>
                          </div>
                          <div className="text-[10px] text-slate-400 mt-0.5">Asymmetric local WebAuthn (TouchID, FaceID, Windows Hello)</div>
                        </div>
                      </div>
                      <ChevronRight className="w-4 h-4 text-slate-400" />
                    </div>

                    {/* Security Key Option */}
                    <div 
                      onClick={() => handleSelectType('security_key')}
                      className="p-3 border border-slate-200 rounded-xl hover:border-indigo-500 hover:bg-indigo-50/20 cursor-pointer transition-all flex items-center justify-between group"
                    >
                      <div className="flex gap-3">
                        <div className="w-8 h-8 rounded-full bg-indigo-50 text-indigo-600 flex items-center justify-center group-hover:bg-indigo-100 shrink-0">
                          <Key className="w-4 h-4" />
                        </div>
                        <div className="text-left">
                          <div className="text-xs font-bold text-slate-800 flex items-center gap-1.5">
                            FIDO2 Physical Security Key
                            <span className="px-1.5 py-0.2 bg-emerald-100 text-emerald-800 text-[8px] font-bold rounded uppercase">Phishing Res.</span>
                          </div>
                          <div className="text-[10px] text-slate-400 mt-0.5">Hardware USB / NFC tokens (YubiKey, Feitian, SoloKeys)</div>
                        </div>
                      </div>
                      <ChevronRight className="w-4 h-4 text-slate-400" />
                    </div>

                    {/* TOTP Option */}
                    <div 
                      onClick={() => handleSelectType('totp')}
                      className="p-3 border border-slate-200 rounded-xl hover:border-indigo-500 hover:bg-indigo-50/20 cursor-pointer transition-all flex items-center justify-between group"
                    >
                      <div className="flex gap-3">
                        <div className="w-8 h-8 rounded-full bg-indigo-50 text-indigo-600 flex items-center justify-center group-hover:bg-indigo-100 shrink-0">
                          <QrCode className="w-4 h-4" />
                        </div>
                        <div className="text-left">
                          <div className="text-xs font-bold text-slate-800">Time-based One Time Password (TOTP)</div>
                          <div className="text-[10px] text-slate-400 mt-0.5">Authenticator app code rotation (Google Auth, Duo, Authy)</div>
                        </div>
                      </div>
                      <ChevronRight className="w-4 h-4 text-slate-400" />
                    </div>

                    {/* Push Option */}
                    <div 
                      onClick={() => handleSelectType('push')}
                      className="p-3 border border-slate-200 rounded-xl hover:border-indigo-500 hover:bg-indigo-50/20 cursor-pointer transition-all flex items-center justify-between group"
                    >
                      <div className="flex gap-3">
                        <div className="w-8 h-8 rounded-full bg-indigo-50 text-indigo-600 flex items-center justify-center group-hover:bg-indigo-100 shrink-0">
                          <Smartphone className="w-4 h-4" />
                        </div>
                        <div className="text-left">
                          <div className="text-xs font-bold text-slate-800">Mobile Push Authenticator</div>
                          <div className="text-[10px] text-slate-400 mt-0.5">Interactive mobile push challenge dialogs</div>
                        </div>
                      </div>
                      <ChevronRight className="w-4 h-4 text-slate-400" />
                    </div>
                  </div>
                </div>
              )}

              {enrollStep === 'verify' && (
                <div className="space-y-4">
                  <h3 className="text-xs font-bold text-slate-700">2. Authenticate & Setup Cryptographic Binding</h3>
                  
                  <div>
                    <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">Descriptive Token Name</label>
                    <input
                      type="text"
                      value={newFactorName}
                      onChange={(e) => setNewFactorName(e.target.value)}
                      className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2 text-xs text-slate-700 focus:outline-hidden focus:ring-2 focus:ring-indigo-500 focus:bg-white font-medium"
                    />
                  </div>

                  {newFactorType === 'totp' && (
                    <div className="bg-slate-50 border border-slate-200 rounded-xl p-3 text-center">
                      <div className="text-[10px] text-slate-500 mb-2">Scan the QR code or manually enter the secret in your authenticator app.</div>
                      
                      {/* Fake QR code generation */}
                      <div className="w-24 h-24 bg-white border border-slate-200 mx-auto flex items-center justify-center rounded-lg shadow-2xs mb-2">
                        <QrCode className="w-20 h-20 text-slate-800" />
                      </div>

                      <div className="text-[9px] font-mono text-slate-400 mb-4 select-all">
                        Key: <span className="font-bold text-indigo-600">{totpSecret}</span>
                      </div>

                      <div>
                        <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1 text-left">Confirm 6-Digit Pin</label>
                        <input
                          type="text"
                          maxLength={6}
                          placeholder="000000"
                          value={verificationCode}
                          onChange={(e) => setVerificationCode(e.target.value.replace(/\D/g, ''))}
                          className="w-full bg-white border border-slate-300 rounded-lg p-2 text-center text-sm font-mono font-bold tracking-widest text-indigo-600 focus:outline-hidden focus:ring-2 focus:ring-indigo-500"
                        />
                      </div>
                    </div>
                  )}

                  {(newFactorType === 'passkey' || newFactorType === 'security_key') && (
                    <div className="bg-indigo-50 border border-indigo-100 rounded-xl p-4 text-center">
                      <Fingerprint className="w-12 h-12 text-indigo-600 mx-auto mb-2 animate-pulse" />
                      <div className="text-xs font-semibold text-indigo-800 mb-1">Hardware Handshake Required</div>
                      <div className="text-[10px] text-indigo-600/80">Press the Register button below. Your browser will prompt you to save a public-key credential on this device.</div>
                    </div>
                  )}

                  {newFactorType === 'push' && (
                    <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 text-center">
                      <Smartphone className="w-10 h-10 text-slate-400 mx-auto mb-2" />
                      <div className="text-[10px] text-slate-500">We will register your mobile device to receive cryptographically signed Push approval tokens.</div>
                    </div>
                  )}

                  <div className="flex gap-2 pt-2 border-t border-slate-100">
                    <button
                      onClick={() => setEnrollStep('type')}
                      className="flex-1 py-2 border border-slate-200 rounded-lg text-xs font-bold text-slate-600 hover:bg-slate-50"
                    >
                      Back
                    </button>
                    <button
                      onClick={handleVerifyEnrollment}
                      disabled={isProcessing}
                      className="flex-1 py-2 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white rounded-lg text-xs font-bold shadow-xs flex items-center justify-center gap-1.5"
                    >
                      {isProcessing && <Loader2 className="w-3.5 h-3.5 animate-spin" />}
                      Register Credential
                    </button>
                  </div>
                </div>
              )}

              {enrollStep === 'complete' && (
                <div className="text-center py-4 space-y-4">
                  <div className="w-12 h-12 bg-emerald-50 rounded-full flex items-center justify-center text-emerald-600 mx-auto border border-emerald-100">
                    <Check className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-slate-800">Authenticator Registered Successfully</h3>
                    <p className="text-[11px] text-slate-500 mt-1">Cryptographic key material safely generated, bound, and activated on your account profile.</p>
                  </div>
                  <button
                    onClick={() => {
                      setShowEnrollModal(false);
                      setEnrollStep('type');
                    }}
                    className="w-full py-2 bg-slate-900 hover:bg-slate-800 text-white font-bold rounded-lg text-xs shadow-xs"
                  >
                    Return to Inventory
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
