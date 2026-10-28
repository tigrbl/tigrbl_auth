import React, { useState, useEffect } from 'react';
import { SmartCard } from '../types';
import { KeyRound, ShieldAlert, Cpu, Fingerprint, Eye, EyeOff, Lock, Unlock, CheckCircle } from 'lucide-react';

interface CertificateSelectorHandoffProps {
  cards: SmartCard[];
  isOpen: boolean;
  onSelect: (card: SmartCard, pin: string) => void;
  onCancel: () => void;
}

export const CertificateSelectorHandoff: React.FC<CertificateSelectorHandoffProps> = ({
  cards,
  isOpen,
  onSelect,
  onCancel,
}) => {
  const [selectedCard, setSelectedCard] = useState<SmartCard | null>(null);
  const [step, setStep] = useState<'select' | 'pin' | 'touch' | 'verifying'>('select');
  const [pin, setPin] = useState('');
  const [showPin, setShowPin] = useState(false);
  const [attempts, setAttempts] = useState(3);
  const [pinError, setPinError] = useState('');
  const [shake, setShake] = useState(false);
  const [touchActive, setTouchActive] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setSelectedCard(null);
      setStep('select');
      setPin('');
      setPinError('');
      setAttempts(3);
      setTouchActive(false);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleSelectCard = (card: SmartCard) => {
    setSelectedCard(card);
    setAttempts(card.hardware.pinAttemptsRemaining);
    if (card.hardware.pinLocked || card.hardware.pinAttemptsRemaining === 0) {
      setPinError('This card PIN is blocked. PUK (PIN Unblock Key) or administrative reset is required.');
      setStep('pin');
    } else {
      setPinError('');
      setStep('pin');
    }
  };

  const handlePinSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedCard) return;

    if (selectedCard.hardware.pinLocked || attempts === 0) {
      setPinError('Card PIN is blocked. Security module locked.');
      return;
    }

    // Default correct PIN is "1234" for all active cards in simulator
    if (pin === '1234') {
      setPinError('');
      if (selectedCard.hardware.touchRequired) {
        setStep('touch');
        setTouchActive(true);
      } else {
        triggerVerification('');
      }
    } else {
      const nextAttempts = attempts - 1;
      setAttempts(nextAttempts);
      setShake(true);
      setTimeout(() => setShake(false), 500);

      if (nextAttempts <= 0) {
        setPinError('PIN BLOCKED. You have exceeded maximum PIN validation attempts. The smart-card cryptographic coprocessor is locked.');
        selectedCard.hardware.pinLocked = true;
        selectedCard.hardware.pinAttemptsRemaining = 0;
      } else {
        setPinError(`Incorrect Smart Card PIN. ${nextAttempts} attempt${nextAttempts > 1 ? 's' : ''} remaining before hardware block.`);
      }
    }
  };

  const triggerVerification = (mockPin: string) => {
    setStep('verifying');
    setTimeout(() => {
      if (selectedCard) {
        onSelect(selectedCard, pin);
      }
    }, 1500);
  };

  const handleTouchSimulate = () => {
    setTouchActive(false);
    triggerVerification('');
  };

  return (
    <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center z-50 p-4" id="virtual-os-prompt">
      <div className="bg-slate-100 rounded-xl shadow-2xl border border-slate-300 w-full max-w-lg overflow-hidden flex flex-col">
        {/* Mock OS Header */}
        <div className="bg-slate-800 text-slate-200 px-4 py-3 flex items-center justify-between border-b border-slate-700 select-none">
          <div className="flex items-center gap-2">
            <Cpu className="w-4.5 h-4.5 text-indigo-400" />
            <span className="text-xs font-bold font-mono tracking-wider text-slate-300">OS SYSTEM SECURITY PROMPT</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded-full bg-rose-500/80"></span>
            <span className="w-3 h-3 rounded-full bg-amber-500/80"></span>
            <span className="w-3 h-3 rounded-full bg-emerald-500/80"></span>
          </div>
        </div>

        {/* Content Area */}
        <div className="p-6 flex-1 flex flex-col justify-center min-h-[300px]">
          {step === 'select' && (
            <div className="space-y-4">
              <div className="text-center pb-2">
                <h3 className="text-sm font-bold text-slate-800 uppercase tracking-tight">Select Certificate</h3>
                <p className="text-xs text-slate-500 mt-1">
                  The client application is requesting smart card mTLS authentication. Select a certificate projection:
                </p>
              </div>

              <div className="space-y-2.5 max-h-[220px] overflow-y-auto pr-1">
                {cards.map((card) => {
                  const isWrongProfile = card.eku.length === 1 && card.eku[0].includes('Secure Email');
                  return (
                    <button
                      key={card.id}
                      onClick={() => handleSelectCard(card)}
                      className="w-full text-left p-3 rounded-lg border bg-white hover:border-indigo-500 hover:bg-slate-50/50 hover:shadow-xs transition-all flex items-start gap-3 group"
                      id={`os-cert-item-${card.id}`}
                    >
                      <div className="p-2 bg-slate-100 rounded-md group-hover:bg-indigo-50 shrink-0">
                        <KeyRound className="w-4.5 h-4.5 text-slate-600 group-hover:text-indigo-600" />
                      </div>
                      <div className="min-w-0 flex-1">
                        <div className="flex items-center justify-between gap-2">
                          <span className="text-xs font-bold text-slate-700 truncate block group-hover:text-indigo-950">
                            {card.subject.split(',')[0].replace('CN=', '')}
                          </span>
                          <span className={`text-[9px] px-1.5 py-0.5 rounded-full font-bold font-mono uppercase shrink-0 ${
                            card.status === 'active' ? 'bg-emerald-50 text-emerald-700 border border-emerald-100' :
                            card.status === 'expiring' ? 'bg-amber-50 text-amber-700 border border-amber-100' :
                            card.status === 'expired' ? 'bg-rose-50 text-rose-700 border border-rose-100' :
                            'bg-slate-200 text-slate-700'
                          }`}>
                            {card.hardware.cardType}
                          </span>
                        </div>
                        <div className="text-[10px] text-slate-500 font-mono truncate mt-0.5">
                          Issuer: {card.issuer.split(',')[0].replace('CN=', '')}
                        </div>
                        <div className="text-[9.5px] text-slate-400 mt-0.5">
                          Serial: {card.serialNumber} • Valid till: {new Date(card.notAfter).toLocaleDateString()}
                        </div>
                        {isWrongProfile && (
                          <div className="mt-1.5 text-[9px] font-bold text-amber-700 bg-amber-50 rounded px-1.5 py-0.5 w-fit border border-amber-100">
                            Warning: Missing ClientAuth EKU
                          </div>
                        )}
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {step === 'pin' && selectedCard && (
            <div className={`space-y-4 ${shake ? 'animate-bounce' : ''}`}>
              <div className="text-center">
                <div className="inline-flex p-3 bg-indigo-50 border border-indigo-100 rounded-full mb-3 text-indigo-600">
                  <Lock className="w-5 h-5" />
                </div>
                <h3 className="text-sm font-bold text-slate-800">Smart Card PIN Prompt</h3>
                <p className="text-xs text-slate-500 mt-1">
                  Provide PIN to unlock the private cryptographic key on <span className="font-semibold text-slate-700">{selectedCard.label}</span>.
                </p>
              </div>

              <form onSubmit={handlePinSubmit} className="space-y-4 max-w-xs mx-auto">
                <div className="relative">
                  <input
                    type={showPin ? 'text' : 'password'}
                    value={pin}
                    onChange={(e) => setPin(e.target.value)}
                    disabled={selectedCard.hardware.pinLocked || attempts === 0}
                    placeholder="Enter Card PIN (try 1234)"
                    className="w-full pl-3 pr-10 py-2.5 text-center font-mono text-sm tracking-widest bg-white border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 disabled:bg-slate-100 disabled:text-slate-400"
                    maxLength={12}
                    id="input-card-pin"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPin(!showPin)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
                    id="btn-toggle-pin-visibility"
                  >
                    {showPin ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>

                {pinError ? (
                  <div className="p-3 bg-rose-50 border border-rose-100 rounded-lg text-left flex gap-2">
                    <ShieldAlert className="w-4 h-4 text-rose-600 mt-0.5 shrink-0" />
                    <div className="text-[10px] text-rose-700 font-medium leading-relaxed">{pinError}</div>
                  </div>
                ) : (
                  <div className="text-center text-[10px] text-slate-500 font-semibold">
                    {attempts} validation attempt{attempts > 1 ? 's' : ''} remaining before hardware lock-out
                  </div>
                )}

                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => setStep('select')}
                    className="flex-1 py-2 text-xs font-semibold text-slate-600 hover:text-slate-800 bg-slate-200/80 rounded-lg hover:bg-slate-200 transition-colors"
                    id="btn-back-to-certs"
                  >
                    Back
                  </button>
                  <button
                    type="submit"
                    disabled={!pin || selectedCard.hardware.pinLocked || attempts === 0}
                    className="flex-1 py-2 text-xs font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors disabled:bg-slate-300 disabled:cursor-not-allowed flex items-center justify-center gap-1.5 shadow-sm"
                    id="btn-submit-pin"
                  >
                    <Unlock className="w-3.5 h-3.5" />
                    Verify PIN
                  </button>
                </div>
              </form>
            </div>
          )}

          {step === 'touch' && selectedCard && (
            <div className="space-y-4 text-center">
              <div className="inline-flex p-4 bg-indigo-50 text-indigo-600 rounded-full animate-pulse border border-indigo-100">
                <Fingerprint className="w-8 h-8" />
              </div>
              <h3 className="text-sm font-bold text-slate-800">Card Presence Touch Challenge</h3>
              <p className="text-xs text-slate-500 leading-relaxed max-w-sm mx-auto">
                Your organizational security profile requires a physical presence verification. Please tap or touch the gold contact sensor on your <span className="font-semibold text-slate-700">{selectedCard.hardware.reader.split(' ')[0]}</span> reader or key now.
              </p>

              <div className="pt-3 max-w-xs mx-auto">
                <button
                  type="button"
                  onClick={handleTouchSimulate}
                  className="w-full py-2.5 text-xs font-bold text-indigo-700 bg-indigo-50 hover:bg-indigo-100 border border-indigo-200 rounded-lg flex items-center justify-center gap-2 transition-all active:scale-98 shadow-xs"
                  id="btn-simulate-touch"
                >
                  <Fingerprint className="w-4 h-4 animate-ping" />
                  Simulate Reader/Key Touch
                </button>
              </div>
            </div>
          )}

          {step === 'verifying' && selectedCard && (
            <div className="space-y-4 text-center">
              <div className="flex justify-center">
                <div className="relative flex items-center justify-center">
                  <div className="w-12 h-12 border-4 border-slate-300 border-t-indigo-600 rounded-full animate-spin"></div>
                  <Cpu className="w-5 h-5 text-indigo-600 absolute" />
                </div>
              </div>
              <h3 className="text-xs font-bold text-slate-800 tracking-wider uppercase">Completing mTLS Verification...</h3>
              <p className="text-xs text-slate-500">
                Verifying PKCS#11 cryptographic proof and checking OCSP/CRL trust lists...
              </p>
              <div className="font-mono text-[9px] text-slate-400 bg-slate-50 p-2.5 rounded border border-slate-200/60 max-w-xs mx-auto text-left truncate">
                SIG: {selectedCard.fingerprint.slice(0, 48)}...
              </div>
            </div>
          )}
        </div>

        {/* Modal Footer */}
        <div className="bg-slate-200/80 px-6 py-3.5 flex justify-between items-center border-t border-slate-300 select-none">
          <span className="text-[10px] text-slate-500 font-medium">PKCS#11 CSP v2.4.0 Bridge</span>
          <button
            type="button"
            onClick={onCancel}
            className="px-3.5 py-1.5 text-xs font-semibold text-slate-600 bg-white border border-slate-300 hover:bg-slate-50 rounded-lg transition-colors"
            id="btn-cancel-os-prompt"
          >
            Cancel Handoff
          </button>
        </div>
      </div>
    </div>
  );
};
