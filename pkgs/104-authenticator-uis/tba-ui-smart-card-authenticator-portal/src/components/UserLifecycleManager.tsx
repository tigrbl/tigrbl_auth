import React, { useState } from 'react';
import { SmartCard, AuditLog } from '../types';
import { 
  Plus, Trash2, Calendar, AlertTriangle, Fingerprint, RefreshCcw, 
  ChevronRight, Clock, ShieldCheck, Settings, Check, ArrowRight, ShieldAlert
} from 'lucide-react';

interface UserLifecycleManagerProps {
  cards: SmartCard[];
  onAddCard: (card: SmartCard) => void;
  onRemoveCard: (id: string) => void;
  onUpdateCardStatus: (id: string, status: SmartCard['status']) => void;
  onLogIncident: (log: Omit<AuditLog, 'id' | 'timestamp'>) => void;
  readerConnected: boolean;
  cardInserted: boolean;
}

export const UserLifecycleManager: React.FC<UserLifecycleManagerProps> = ({
  cards,
  onAddCard,
  onRemoveCard,
  onUpdateCardStatus,
  onLogIncident,
  readerConnected,
  cardInserted,
}) => {
  const [activeTab, setActiveTab] = useState<'list' | 'register' | 'detail' | 'renew'>('list');
  const [selectedCard, setSelectedCard] = useState<SmartCard | null>(cards[0] || null);
  
  // Registration States
  const [regStep, setRegStep] = useState<1 | 2 | 3>(1);
  const [regLabel, setRegLabel] = useState('');
  const [regType, setRegType] = useState<'PIV' | 'CAC'>('CAC');
  const [regPin, setRegPin] = useState('');
  const [simulatedCert, setSimulatedCert] = useState<SmartCard | null>(null);

  // Overlap renewal state
  const [renewalTargetId, setRenewalTargetId] = useState<string | null>(null);

  // Simulated raw certificates available in the middleware for registration
  const unmappedCerts: Omit<SmartCard, 'id' | 'lastUsed' | 'status'>[] = [
    {
      label: 'PIV Identity Certificate',
      subject: 'CN=CONNOR.SARAH.ANN.8820394851,OU=HHS,O=U.S. Government,C=US',
      issuer: 'CN=HHS PIV SUBCA G3,OU=PKI,O=U.S. Government,C=US',
      serialNumber: '5E:11:92:AA:7B:44:03:DD',
      fingerprint: 'SHA-256: 8D:C2:5F:77:88:99:AA:BB:CC:DD:EE:FF:11:22:33:44:55:66:77:88:99:00:11:22:33:44:55:66:77:88:AA:BC',
      notBefore: '2026-07-20T00:00:00Z',
      notAfter: '2029-07-20T00:00:00Z',
      eku: ['Client Authentication (1.3.6.1.5.5.7.3.2)'],
      san: 'PrincipalName: sarah.connor@hhs.gov',
      hardware: {
        reader: 'SCR-3310 Contactless Smart Card Reader',
        cardType: 'PIV',
        pinAttemptsRemaining: 3,
        pinLocked: false,
        touchRequired: false,
      }
    },
    {
      label: 'DoD Email Signature Certificate',
      subject: 'CN=CONNOR.SARAH.ANN.8820394851,OU=USA,O=U.S. Government,C=US',
      issuer: 'CN=DOD SUBCA CA-62,OU=PKI,O=U.S. Government,C=US',
      serialNumber: '4C:99:EE:22:8A:2F:E9:9C',
      fingerprint: 'SHA-256: E3:A1:4C:E9:99:FF:01:23:45:67:89:AB:CD:EF:01:23:45:67:89:AB:CD:EF:01:23:45:67:89:AB:CE:BB:11:99',
      notBefore: '2026-07-15T00:00:00Z',
      notAfter: '2029-07-15T00:00:00Z',
      eku: ['Secure Email (1.3.6.1.5.5.7.3.4)'],
      san: 'RFC822Name: sarah.connor@mail.mil',
      hardware: {
        reader: 'SCR-3310 Contactless Smart Card Reader',
        cardType: 'CAC',
        pinAttemptsRemaining: 3,
        pinLocked: false,
        touchRequired: false,
      }
    }
  ];

  const handleSelectRegCert = (certIdx: number) => {
    const cert = unmappedCerts[certIdx];
    setSimulatedCert({
      ...cert,
      id: `sc-reg-${Date.now()}`,
      status: 'active',
      lastUsed: 'Never used',
    });
    setRegStep(2);
  };

  const handleCompleteRegistration = (e: React.FormEvent) => {
    e.preventDefault();
    if (!simulatedCert) return;

    const finalCard: SmartCard = {
      ...simulatedCert,
      label: regLabel || simulatedCert.label,
      hardware: {
        ...simulatedCert.hardware,
        cardType: regType,
      }
    };

    onAddCard(finalCard);
    setSelectedCard(finalCard);
    onLogIncident({
      event: 'sc.enrollment.success',
      actor: finalCard.subject.split(',')[0],
      status: 'success',
      cardFingerprint: finalCard.fingerprint.slice(0, 16) + '...',
      details: `Enrolled new ${regType} card successfully. Validated issuer chain, EKU, and cryptographic possession.`,
      ipAddress: '10.142.0.4'
    });

    // Reset and go to detail
    setRegLabel('');
    setRegPin('');
    setSimulatedCert(null);
    setRegStep(1);
    setActiveTab('list');
  };

  const handleRevokeCard = (card: SmartCard) => {
    const isLastCard = cards.length === 1;
    let message = `Are you absolutely sure you want to immediately revoke and remove "${card.label}"?\n\nThis will immediately:\n- Disconnect 2 associated developer mTLS service bindings\n- Terminate all active sessions utilizing this smart-card credential\n- Blacklist this certificate serial on local OCSP/CRL responder simulators.`;
    
    if (isLastCard) {
      message += `\n\n⚠️ WARNING: This is your final enrolled smart card. Removing this factor will force your account into supervised identity recovery.`;
    }

    if (confirm(message)) {
      onRemoveCard(card.id);
      onLogIncident({
        event: 'sc.auth.revocation',
        actor: card.subject.split(',')[0],
        status: 'failure',
        cardFingerprint: card.fingerprint.slice(0, 16) + '...',
        details: `Immediate card deletion and CRL revocation triggered by user. Associated mTLS profile tokens blacklisted.`,
        ipAddress: '10.142.0.4'
      });
      setSelectedCard(cards.find(c => c.id !== card.id) || null);
    }
  };

  const handleInitiateRenewal = (card: SmartCard) => {
    setRenewalTargetId(card.id);
    setSimulatedCert({
      ...unmappedCerts[0],
      id: `sc-renew-${Date.now()}`,
      label: `Replacement CAC (Renewal Overlap)`,
      status: 'active',
      lastUsed: 'Never used',
    });
    setRegLabel(`Replacement CAC (Renewal Overlap)`);
    setRegStep(2);
    setActiveTab('register');
  };

  return (
    <div className="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm flex flex-col h-full" id="lifecycle-panel">
      {/* Tab bar */}
      <div className="bg-slate-50 border-b border-slate-200 px-5 py-3.5 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Settings className="w-4.5 h-4.5 text-indigo-600" />
          <h3 className="font-semibold text-slate-800 text-sm">Enrollment & User Lifecycle</h3>
        </div>
        <div className="flex gap-1.5">
          <button
            onClick={() => setActiveTab('list')}
            className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-colors ${
              activeTab === 'list' ? 'bg-indigo-600 text-white shadow-xs' : 'text-slate-600 hover:bg-slate-100 hover:text-slate-800'
            }`}
            id="tab-view-cards"
          >
            My Cards ({cards.length})
          </button>
          <button
            onClick={() => {
              setRegStep(1);
              setSimulatedCert(null);
              setActiveTab('register');
            }}
            className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-colors flex items-center gap-1 ${
              activeTab === 'register' ? 'bg-indigo-600 text-white shadow-xs' : 'text-slate-600 hover:bg-slate-100 hover:text-slate-800'
            }`}
            id="tab-enroll-card"
          >
            <Plus className="w-3.5 h-3.5" />
            Enroll Token
          </button>
        </div>
      </div>

      {/* Main Panel Content */}
      <div className="p-5 flex-1 flex flex-col min-h-[420px]">
        {activeTab === 'list' && (
          <div className="grid grid-cols-1 md:grid-cols-12 gap-5 flex-1">
            {/* Sidebar List */}
            <div className="md:col-span-5 border-r border-slate-100 pr-1 space-y-2">
              <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">Registered Keys</span>
              
              {cards.length === 0 ? (
                <div className="text-center py-10 bg-slate-50 rounded-lg border border-dashed border-slate-200 p-4">
                  <ShieldAlert className="w-8 h-8 text-slate-400 mx-auto mb-2" />
                  <p className="text-xs font-semibold text-slate-600">No registered smart cards found</p>
                  <p className="text-[10px] text-slate-400 mt-1">Register a PIV or CAC to configure possession factor authentication.</p>
                </div>
              ) : (
                <div className="space-y-2 max-h-[350px] overflow-y-auto pr-1">
                  {cards.map((card) => {
                    const isSelected = selectedCard?.id === card.id;
                    return (
                      <button
                        key={card.id}
                        onClick={() => setSelectedCard(card)}
                        className={`w-full text-left p-3 rounded-lg border transition-all flex items-start gap-2.5 ${
                          isSelected 
                            ? 'bg-indigo-50/70 border-indigo-200 ring-1 ring-indigo-50' 
                            : 'bg-white hover:bg-slate-50 border-slate-200'
                        }`}
                        id={`enrolled-card-item-${card.id}`}
                      >
                        <div className={`p-1.5 rounded-md ${isSelected ? 'bg-indigo-600 text-white' : 'bg-slate-100 text-slate-600'} shrink-0 mt-0.5`}>
                          <Clock className="w-4 h-4" />
                        </div>
                        <div className="min-w-0 flex-1">
                          <div className="flex items-center justify-between gap-1.5">
                            <span className="text-xs font-bold text-slate-700 truncate block">{card.label}</span>
                            <span className={`text-[8.5px] font-bold px-1 py-0.2 rounded font-mono ${
                              card.status === 'active' ? 'bg-emerald-100 text-emerald-800' :
                              card.status === 'expiring' ? 'bg-amber-100 text-amber-800' :
                              card.status === 'expired' ? 'bg-rose-100 text-rose-800' :
                              'bg-slate-200 text-slate-800'
                            }`}>
                              {card.status}
                            </span>
                          </div>
                          <p className="text-[10px] text-slate-400 font-mono truncate mt-0.5">Subject: {card.subject.split(',')[0].replace('CN=', '')}</p>
                        </div>
                      </button>
                    );
                  })}
                </div>
              )}
            </div>

            {/* Selected Card Details */}
            <div className="md:col-span-7 flex flex-col justify-between">
              {selectedCard ? (
                <div className="space-y-4">
                  <div className="flex items-start justify-between">
                    <div>
                      <h4 className="text-sm font-bold text-slate-800">{selectedCard.label}</h4>
                      <p className="text-[10px] font-mono text-slate-500 mt-0.5">ID: {selectedCard.id} • Type: {selectedCard.hardware.cardType}</p>
                    </div>
                    <button
                      onClick={() => handleRevokeCard(selectedCard)}
                      className="px-2.5 py-1 text-[10.5px] font-semibold text-rose-600 hover:text-white hover:bg-rose-600 border border-rose-200 rounded-lg transition-colors flex items-center gap-1 bg-rose-50"
                      id={`btn-revoke-card-${selectedCard.id}`}
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                      Revoke Card
                    </button>
                  </div>

                  {/* Validity stats bar */}
                  <div className="bg-slate-50 p-3 rounded-lg border border-slate-200/80 space-y-1.5 text-xs">
                    <div className="flex justify-between text-[11px] text-slate-600 font-medium">
                      <span>Card Expiration Timeline</span>
                      <span className="font-mono text-slate-700">Expires {new Date(selectedCard.notAfter).toLocaleDateString()}</span>
                    </div>
                    <div className="w-full bg-slate-200 rounded-full h-2 overflow-hidden">
                      <div 
                        className={`h-full rounded-full ${
                          selectedCard.status === 'active' ? 'bg-indigo-600' :
                          selectedCard.status === 'expiring' ? 'bg-amber-500 animate-pulse' :
                          'bg-rose-500'
                        }`} 
                        style={{ 
                          width: selectedCard.status === 'expired' ? '0%' : 
                                 selectedCard.status === 'expiring' ? '15%' : '78%' 
                        }}
                      ></div>
                    </div>
                    <div className="flex justify-between text-[10px] text-slate-400">
                      <span>Registered: {new Date(selectedCard.notBefore).toLocaleDateString()}</span>
                      {selectedCard.status === 'expiring' && (
                        <span className="text-amber-700 font-bold flex items-center gap-1">
                          <AlertTriangle className="w-3 h-3" />
                          Expiring within grace period. Action recommended.
                        </span>
                      )}
                    </div>
                  </div>

                  {/* Cryptographic properties */}
                  <div className="space-y-2">
                    <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Cryptographic Specifications</span>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-[10.5px]">
                      <div className="bg-slate-50 p-2.5 rounded border border-slate-200/50">
                        <span className="text-slate-500 block">Subject Identifier</span>
                        <span className="text-slate-700 font-mono truncate block mt-0.5" title={selectedCard.subject}>{selectedCard.subject}</span>
                      </div>
                      <div className="bg-slate-50 p-2.5 rounded border border-slate-200/50">
                        <span className="text-slate-500 block">Signing Authority (Issuer)</span>
                        <span className="text-slate-700 font-mono truncate block mt-0.5" title={selectedCard.issuer}>{selectedCard.issuer}</span>
                      </div>
                      <div className="bg-slate-50 p-2.5 rounded border border-slate-200/50">
                        <span className="text-slate-500 block">Certificate Serial</span>
                        <span className="text-slate-700 font-mono block mt-0.5">{selectedCard.serialNumber}</span>
                      </div>
                      <div className="bg-slate-50 p-2.5 rounded border border-slate-200/50">
                        <span className="text-slate-500 block">Extended Key Usage (EKU)</span>
                        <span className="text-slate-700 font-mono truncate block mt-0.5">{selectedCard.eku.join(', ')}</span>
                      </div>
                    </div>

                    <div className="bg-slate-50 p-2.5 rounded border border-slate-200/50 text-[10.5px]">
                      <span className="text-slate-500 flex items-center gap-1">
                        <Fingerprint className="w-3.5 h-3.5 text-slate-400" />
                        Certificate SHA-256 Fingerprint
                      </span>
                      <span className="text-slate-700 font-mono block break-all text-[9.5px] mt-1 p-1 bg-white border border-slate-150 rounded">{selectedCard.fingerprint}</span>
                    </div>
                  </div>

                  {/* Overlap renewal button if expiring */}
                  {selectedCard.status === 'expiring' && (
                    <div className="p-3 bg-amber-50 border border-amber-100 rounded-lg flex items-center justify-between">
                      <div className="flex gap-2">
                        <Clock className="w-4 h-4 text-amber-700 mt-0.5 shrink-0" />
                        <div className="text-[10px] text-slate-600">
                          <span className="font-semibold text-amber-900 block">Overlap Renewal Eligible</span>
                          Bind your replacement certificate now before retiring this card to prevent administrative lockout.
                        </div>
                      </div>
                      <button
                        onClick={() => handleInitiateRenewal(selectedCard)}
                        className="px-3 py-1.5 bg-amber-600 hover:bg-amber-700 text-white text-[10.5px] font-bold rounded-lg transition-colors whitespace-nowrap"
                        id="btn-renew-overlap"
                      >
                        Renew with Overlap
                      </button>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center py-20 text-slate-400 text-xs">
                  Select a card on the left to inspect its parameters and lifecycle.
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'register' && (
          <div className="max-w-xl mx-auto w-full py-2">
            {regStep === 1 && (
              <div className="space-y-4">
                <div className="text-center">
                  <h4 className="text-xs font-bold text-slate-800 uppercase tracking-tight">Initiate New Smart Card Registration</h4>
                  <p className="text-xs text-slate-500 mt-1 leading-relaxed">
                    Insert your physical smart card. The card middleware will project the public certificate details.
                  </p>
                </div>

                {/* Preflight detection inline */}
                <div className="p-3.5 bg-slate-50 border border-slate-200 rounded-lg space-y-2 text-xs">
                  <span className="text-[10px] font-bold text-slate-500 uppercase">Hardware Check</span>
                  <div className="flex justify-between">
                    <span className="text-slate-600">CCID USB Reader connected:</span>
                    <span className={`font-mono font-bold ${readerConnected ? 'text-emerald-600' : 'text-amber-600'}`}>
                      {readerConnected ? 'DETECTED' : 'NOT DETECTED'}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-600">Smart Card inserted:</span>
                    <span className={`font-mono font-bold ${cardInserted ? 'text-emerald-600' : 'text-amber-600'}`}>
                      {cardInserted ? 'DETECTED (Active Contacts)' : 'EMPTY SLOT'}
                    </span>
                  </div>
                </div>

                {!cardInserted ? (
                  <div className="p-4 bg-amber-50 border border-amber-100 rounded-lg text-xs text-amber-800 flex gap-2">
                    <AlertTriangle className="w-4.5 h-4.5 text-amber-600 shrink-0 mt-0.5" />
                    <div>
                      <span className="font-semibold block">Hardware Absent</span>
                      Insert a physical smart card into your local reader to invoke the certificate selection projection.
                    </div>
                  </div>
                ) : (
                  <div className="space-y-2">
                    <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Eligible Certificates Unmapped in Middleware</span>
                    {unmappedCerts.map((cert, idx) => (
                      <button
                        key={idx}
                        onClick={() => handleSelectRegCert(idx)}
                        className="w-full text-left p-3 border border-slate-200 rounded-lg hover:border-indigo-500 hover:bg-indigo-50/20 transition-all flex justify-between items-center group"
                        id={`reg-cert-choice-${idx}`}
                      >
                        <div>
                          <span className="text-xs font-bold text-slate-700 block group-hover:text-indigo-950">
                            {cert.subject.split(',')[0].replace('CN=', '')}
                          </span>
                          <span className="text-[10px] text-slate-400 font-mono">{cert.issuer.split(',')[0]}</span>
                        </div>
                        <div className="flex items-center gap-2 text-xs font-semibold text-indigo-600">
                          Map Public Cert
                          <ChevronRight className="w-4 h-4" />
                        </div>
                      </button>
                    ))}
                  </div>
                )}
              </div>
            )}

            {regStep === 2 && simulatedCert && (
              <form onSubmit={handleCompleteRegistration} className="space-y-4">
                <div className="text-center pb-2 border-b border-slate-100">
                  <h4 className="text-xs font-bold text-slate-800 uppercase tracking-tight">Configure Enrolled Certificate</h4>
                  <p className="text-xs text-slate-500 mt-1">Bind this identity to your secure account</p>
                </div>

                {/* Scoped fields */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
                  <div className="space-y-1.5">
                    <label className="text-[10.5px] font-semibold text-slate-600 uppercase block">Custom Card Label</label>
                    <input
                      type="text"
                      value={regLabel}
                      onChange={(e) => setRegLabel(e.target.value)}
                      placeholder="e.g. My Primary Agency CAC"
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 text-xs bg-white text-slate-800"
                      maxLength={32}
                      id="reg-input-label"
                      required
                    />
                  </div>
                  <div className="space-y-1.5">
                    <label className="text-[10.5px] font-semibold text-slate-600 uppercase block">Smart Card Profile Type</label>
                    <select
                      value={regType}
                      onChange={(e) => setRegType(e.target.value as any)}
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 text-xs bg-white text-slate-800"
                      id="reg-select-type"
                    >
                      <option value="CAC">CAC (DoD Common Access Card)</option>
                      <option value="PIV">PIV (Federal Personal Identity Verification)</option>
                    </select>
                  </div>
                </div>

                <div className="bg-slate-50 p-4 rounded-lg border border-slate-200 text-xs space-y-2">
                  <span className="text-[10px] font-bold text-slate-500 uppercase block">Certificate Projection Metadata</span>
                  <div className="grid grid-cols-2 gap-x-4 gap-y-1 font-mono text-[10px] text-slate-600">
                    <div>Subject: <span className="text-slate-800 break-all">{simulatedCert.subject.split(',')[0]}</span></div>
                    <div>Issuer: <span className="text-slate-800 break-all">{simulatedCert.issuer.split(',')[0]}</span></div>
                    <div>Serial: <span className="text-slate-800">{simulatedCert.serialNumber}</span></div>
                    <div>Validity: <span className="text-slate-800">Until {new Date(simulatedCert.notAfter).toLocaleDateString()}</span></div>
                  </div>
                </div>

                {/* Safe PIN proof simulated entry */}
                <div className="space-y-1.5 max-w-xs mx-auto">
                  <label className="text-[10.5px] font-semibold text-slate-600 uppercase block text-center">Confirm Card PIN for Registration Proof</label>
                  <input
                    type="password"
                    value={regPin}
                    onChange={(e) => setRegPin(e.target.value)}
                    placeholder="Enter Card PIN (try 1234)"
                    className="w-full px-3 py-2 text-center border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 tracking-widest font-mono text-xs bg-white"
                    id="reg-input-pin"
                    required
                  />
                  <p className="text-center text-[9px] text-slate-400">The PIN is validated locally by the token chip; private key remains secure on hardware.</p>
                </div>

                <div className="flex gap-2 pt-2">
                  <button
                    type="button"
                    onClick={() => setRegStep(1)}
                    className="flex-1 py-2 bg-slate-100 hover:bg-slate-200 text-slate-600 text-xs font-semibold rounded-lg transition-colors border border-slate-200"
                    id="reg-btn-back"
                  >
                    Back
                  </button>
                  <button
                    type="submit"
                    disabled={!regPin}
                    className="flex-1 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold rounded-lg transition-colors shadow-sm flex items-center justify-center gap-1.5"
                    id="reg-btn-complete"
                  >
                    <ShieldCheck className="w-3.5 h-3.5" />
                    Complete Enrollment
                  </button>
                </div>
              </form>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
