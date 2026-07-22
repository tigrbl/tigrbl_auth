/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useRef } from 'react';
import { 
  Phone, PhoneOff, Wifi, Battery, ShieldCheck, 
  Volume2, Play, AlertTriangle, ShieldAlert, Check, RefreshCw 
} from 'lucide-react';
import { CallContext } from '../types';

interface PhoneSimulatorProps {
  activeCall: CallContext | null;
  onAnswerCall: () => void;
  onDeclineCall: (reason: 'busy' | 'no_answer' | 'voicemail' | 'rejected' | 'failed') => void;
  onKeypadPress: (key: string) => void;
  onIvrSuccess: () => void;
  simulateStateOverride: 'none' | 'busy' | 'no_answer' | 'voicemail' | 'outage';
  setSimulateStateOverride: (val: 'none' | 'busy' | 'no_answer' | 'voicemail' | 'outage') => void;
}

export default function PhoneSimulator({
  activeCall,
  onAnswerCall,
  onDeclineCall,
  onKeypadPress,
  onIvrSuccess,
  simulateStateOverride,
  setSimulateStateOverride
}: PhoneSimulatorProps) {
  const [time, setTime] = useState('10:34 AM');
  const [keypadInput, setKeypadInput] = useState('');
  const [transcriptText, setTranscriptText] = useState('');
  const [isMuted, setIsMuted] = useState(false);
  const [isSpeaker, setIsSpeaker] = useState(true);
  const audioContextRef = useRef<AudioContext | null>(null);

  // Sync clock time
  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      let hours = now.getHours();
      const minutes = now.getMinutes().toString().padStart(2, '0');
      const ampm = hours >= 12 ? 'PM' : 'AM';
      hours = hours % 12 || 12;
      setTime(`${hours}:${minutes} ${ampm}`);
    };
    updateTime();
    const interval = setInterval(updateTime, 10000);
    return () => clearInterval(interval);
  }, []);

  // Play a soft DTMF key tone when keys are clicked
  const playDtmfTone = (key: string) => {
    try {
      if (!audioContextRef.current) {
        audioContextRef.current = new (window.AudioContext || (window as any).webkitAudioContext)();
      }
      const ctx = audioContextRef.current;
      if (ctx.state === 'suspended') {
        ctx.resume();
      }

      // Map phone keys to low/high DTMF frequencies
      const frequencies: { [key: string]: [number, number] } = {
        '1': [697, 1209], '2': [697, 1336], '3': [697, 1477],
        '4': [770, 1209], '5': [770, 1336], '6': [770, 1477],
        '7': [852, 1209], '8': [852, 1336], '9': [852, 1477],
        '*': [941, 1209], '0': [941, 1336], '#': [941, 1477]
      };

      if (!frequencies[key]) return;
      const [f1, f2] = frequencies[key];

      const osc1 = ctx.createOscillator();
      const osc2 = ctx.createOscillator();
      const gainNode = ctx.createGain();

      osc1.type = 'sine';
      osc1.frequency.value = f1;
      osc2.type = 'sine';
      osc2.frequency.value = f2;

      gainNode.gain.setValueAtTime(0, ctx.currentTime);
      gainNode.gain.linearRampToValueAtTime(0.08, ctx.currentTime + 0.05);
      gainNode.gain.setValueAtTime(0.08, ctx.currentTime + 0.15);
      gainNode.gain.linearRampToValueAtTime(0, ctx.currentTime + 0.2);

      osc1.connect(gainNode);
      osc2.connect(gainNode);
      gainNode.connect(ctx.destination);

      osc1.start();
      osc2.start();
      osc1.stop(ctx.currentTime + 0.25);
      osc2.stop(ctx.currentTime + 0.25);
    } catch (e) {
      // AudioContext blocked or unsupported
    }
  };

  // Generate real-time voice transcripts based on call context and status
  useEffect(() => {
    if (!activeCall) {
      setTranscriptText('');
      setKeypadInput('');
      return;
    }

    if (activeCall.status === 'ringing') {
      setTranscriptText('Incoming Secured Call...');
    } else if (activeCall.status === 'connected') {
      setTranscriptText('Connecting to secure gateway. Audio streaming initiated...');
    } else if (activeCall.status === 'ivr_active') {
      if (activeCall.ivrMode === 'code_read') {
        const codeDigits = activeCall.verificationCode.split('').join(', ');
        setTranscriptText(
          `"Welcome to Acme Telephony Verification. You are initiating a security ceremony. Your confirmation code is: ${codeDigits}. I repeat: ${codeDigits}. Please enter this on your web dashboard to proceed."`
        );
      } else {
        setTranscriptText(
          `"Hello! Acme Verification calling. You are performing a step-up confirmation for ${activeCall.transactionPurpose}. To APPROVE this transaction, please press [ 1 ]. To REJECT, please press [ 2 ]."`
        );
      }
    } else if (activeCall.status === 'awaiting_code') {
      setTranscriptText('"Awaiting keypad submission..."');
    } else if (activeCall.status === 'completed') {
      setTranscriptText('"Authentication verified successfully. Thank you, goodbye."');
    } else if (activeCall.status === 'rejected') {
      setTranscriptText('"Transaction rejected by user. Session terminated. Goodbye."');
    } else if (activeCall.status === 'voicemail') {
      setTranscriptText('"Voicemail greeting detected. Session terminated to avoid false-positives."');
    }
  }, [activeCall, activeCall?.status]);

  const handleDialKey = (key: string) => {
    playDtmfTone(key);
    onKeypadPress(key);
    setKeypadInput(prev => (prev + key).slice(-4));

    if (activeCall && activeCall.status === 'ivr_active' && activeCall.ivrMode === 'approval_press') {
      if (key === '1') {
        // Direct Keypad Approval!
        onIvrSuccess();
      } else if (key === '2') {
        onDeclineCall('rejected');
      }
    }
  };

  // Auto-respond for busy/voicemail/no_answer simulation overrides
  useEffect(() => {
    if (activeCall && activeCall.status === 'ringing') {
      if (simulateStateOverride === 'busy') {
        const timer = setTimeout(() => onDeclineCall('busy'), 1500);
        return () => clearTimeout(timer);
      } else if (simulateStateOverride === 'no_answer') {
        const timer = setTimeout(() => onDeclineCall('no_answer'), 4000);
        return () => clearTimeout(timer);
      } else if (simulateStateOverride === 'voicemail') {
        const timer = setTimeout(() => onDeclineCall('voicemail'), 2000);
        return () => clearTimeout(timer);
      } else if (simulateStateOverride === 'outage') {
        const timer = setTimeout(() => onDeclineCall('failed'), 1000);
        return () => clearTimeout(timer);
      }
    }
  }, [activeCall, activeCall?.status, simulateStateOverride]);

  return (
    <div id="phone-container" className="flex flex-col items-center">
      {/* Outer Phone Shell */}
      <div className="relative w-[340px] h-[670px] bg-zinc-900 rounded-[50px] p-3.5 shadow-2xl border-4 border-zinc-900/80 ring-1 ring-zinc-950/40">
        
        {/* Physical Camera Notch */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 h-6 w-36 bg-slate-900 rounded-b-2xl z-50 flex items-center justify-center">
          <div className="w-2.5 h-2.5 bg-zinc-850 rounded-full mr-2 border border-zinc-900"></div>
          <div className="w-12 h-1 bg-zinc-800 rounded-full"></div>
        </div>

        {/* Buttons (Decorative) */}
        <div className="absolute top-24 -left-1 w-[3px] h-12 bg-slate-700 rounded-r-lg"></div>
        <div className="absolute top-40 -left-1 w-[3px] h-16 bg-slate-700 rounded-r-lg"></div>
        <div className="absolute top-60 -left-1 w-[3px] h-16 bg-slate-700 rounded-r-lg"></div>
        <div className="absolute top-32 -right-1 w-[3px] h-20 bg-slate-700 rounded-l-lg"></div>

        {/* Interactive Screen Container */}
        <div className="w-full h-full bg-slate-950 rounded-[38px] overflow-hidden flex flex-col relative text-white font-sans select-none border border-zinc-900/50">
          
          {/* Status Bar */}
          <div className="h-10 px-6 pt-3 flex justify-between items-center text-xs text-zinc-300 font-medium z-40 bg-slate-950/20">
            <span>{time}</span>
            <div className="flex items-center space-x-1.5">
              <Wifi className="w-3.5 h-3.5" />
              <span className="text-[10px] tracking-widest font-bold">5G</span>
              <Battery className="w-4 h-4 text-emerald-500 fill-emerald-500" />
            </div>
          </div>

          {/* Active Call / Screen Display Router */}
          <div className="flex-1 flex flex-col px-4 pt-4 pb-6 overflow-hidden relative justify-between">
            
            {/* Screen State: Idle */}
            {!activeCall && (
              <div className="flex-1 flex flex-col justify-between items-center text-center py-6">
                <div className="pt-8">
                  <div className="w-14 h-14 bg-emerald-500/10 border border-emerald-500/20 rounded-2xl flex items-center justify-center mx-auto mb-3 animate-pulse">
                    <ShieldCheck className="w-7 h-7 text-emerald-400" />
                  </div>
                  <h3 className="text-sm font-semibold tracking-wide text-zinc-300">SECURE SHEILD TEL</h3>
                  <p className="text-[11px] text-zinc-500 font-mono mt-1">CONNECTED TO IDENTITY GATE</p>
                </div>

                <div className="w-full px-4 py-3 bg-zinc-900/60 border border-zinc-900/40 rounded-2xl">
                  <span className="text-[10px] text-zinc-400 font-medium block uppercase tracking-wider mb-1">Device Telephony Posture</span>
                  <div className="flex items-center justify-center space-x-1.5 text-emerald-400 text-xs font-mono font-semibold">
                    <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                    <span>STANDBY • READY FOR MFA</span>
                  </div>
                </div>

                <div className="text-[10px] text-zinc-500 leading-relaxed max-w-[200px]">
                  This simulator represents the out-of-band mobile device. Keep this visible to verify telephony handshakes.
                </div>
              </div>
            )}

            {/* Screen State: Incoming Ringing */}
            {activeCall && activeCall.status === 'ringing' && (
              <div className="flex-1 flex flex-col justify-between items-center text-center pt-8">
                <div>
                  <div className="w-16 h-16 bg-blue-500/10 border border-blue-500/20 rounded-full flex items-center justify-center mx-auto mb-4 animate-bounce">
                    <Phone className="w-8 h-8 text-blue-400 animate-pulse" />
                  </div>
                  <span className="text-[10px] font-semibold text-blue-400 tracking-widest uppercase block mb-1">Incoming Verification Call</span>
                  <h2 className="text-xl font-bold tracking-tight text-white mb-0.5">{activeCall.provider === 'custom_sip' ? 'Enterprise Voice PBX' : 'Acme Auth Gate'}</h2>
                  <p className="text-xs text-zinc-400 font-mono">{activeCall.destination}</p>
                </div>

                {/* Ringing Visualizer */}
                <div className="flex space-x-1.5 justify-center items-center h-10 w-full">
                  <span className="w-2.5 h-2.5 rounded-full bg-blue-500 animate-pulse"></span>
                  <span className="text-xs text-zinc-300 font-mono">Ringing...</span>
                </div>

                {/* Sliding Accept/Decline Actions */}
                <div className="w-full grid grid-cols-2 gap-4 px-2 pb-4">
                  <button 
                    onClick={() => onDeclineCall('rejected')}
                    className="flex flex-col items-center justify-center py-3 bg-red-500 hover:bg-red-600 rounded-2xl text-white transition-all cursor-pointer"
                  >
                    <PhoneOff className="w-5 h-5 mb-1" />
                    <span className="text-[11px] font-semibold">Decline</span>
                  </button>
                  <button 
                    onClick={onAnswerCall}
                    className="flex flex-col items-center justify-center py-3 bg-emerald-500 hover:bg-emerald-600 rounded-2xl text-white transition-all cursor-pointer shadow-lg shadow-emerald-500/20"
                  >
                    <Phone className="w-5 h-5 mb-1 animate-pulse" />
                    <span className="text-[11px] font-semibold">Answer</span>
                  </button>
                </div>
              </div>
            )}

            {/* Screen State: Connected & IVR Interactive */}
            {activeCall && activeCall.status !== 'ringing' && (
              <div className="flex-1 flex flex-col justify-between overflow-hidden">
                
                {/* Header Information */}
                <div className="text-center pt-4">
                  <div className="text-emerald-400 text-[10px] font-mono tracking-widest uppercase mb-0.5 flex items-center justify-center space-x-1">
                    <span className="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-ping"></span>
                    <span>Live Call Connection</span>
                  </div>
                  <h3 className="text-sm font-semibold text-white">{activeCall.provider === 'custom_sip' ? 'Enterprise Voice PBX' : 'Acme Auth Gate'}</h3>
                  <span className="text-[11px] text-zinc-400 font-mono block mt-0.5">Duration: {activeCall.maxTimer - activeCall.timer}s</span>
                </div>

                {/* Audio Waves Visualizer (Dynamic if connected/active) */}
                <div className="my-3 flex items-center justify-center h-12 space-x-1 bg-zinc-900/40 rounded-xl px-4 py-2 border border-zinc-900/20">
                  <Volume2 className="w-4 h-4 text-zinc-400 shrink-0 mr-1.5" />
                  {['ivr_active', 'connected'].includes(activeCall.status) ? (
                    <div className="flex items-center space-x-1 flex-1 justify-center h-full">
                      <span className="w-1 h-6 bg-emerald-500 rounded-full animate-[pulse-ring_1.2s_infinite]"></span>
                      <span className="w-1 h-8 bg-emerald-400 rounded-full animate-[pulse-ring_0.8s_infinite]"></span>
                      <span className="w-1 h-4 bg-emerald-500 rounded-full animate-[pulse-ring_1.5s_infinite]"></span>
                      <span className="w-1 h-9 bg-emerald-400 rounded-full animate-[pulse-ring_1s_infinite]"></span>
                      <span className="w-1 h-5 bg-emerald-500 rounded-full animate-[pulse-ring_0.7s_infinite]"></span>
                    </div>
                  ) : (
                    <div className="w-full text-center text-[11px] text-zinc-500 font-mono">Line Silent</div>
                  )}
                </div>

                {/* IVR Voice Playback Transcript (Crucial for accessibility and understanding) */}
                <div className="bg-zinc-900 border border-zinc-900/40 rounded-2xl p-3 min-h-[95px] flex flex-col justify-between max-h-[140px] overflow-y-auto mb-3">
                  <span className="text-[9px] text-emerald-400 font-mono uppercase tracking-widest block mb-1">IVR VOICE STREAM CAPTIONS:</span>
                  <p className="text-xs text-zinc-200 leading-relaxed italic font-medium">
                    {transcriptText || '"Connecting stream..."'}
                  </p>
                  {activeCall.status === 'ivr_active' && activeCall.ivrMode === 'approval_press' && (
                    <span className="text-[9px] text-amber-400 font-semibold uppercase mt-1 animate-pulse">Keypad Interaction Needed</span>
                  )}
                </div>

                {/* Physical Grid Keypad */}
                <div className="grid grid-cols-3 gap-x-3 gap-y-2 px-2 pb-2">
                  {['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#'].map(key => (
                    <button
                      key={key}
                      onClick={() => handleDialKey(key)}
                      disabled={['completed', 'rejected', 'voicemail'].includes(activeCall.status)}
                      className="h-10 rounded-full bg-zinc-800/95 hover:bg-zinc-750 active:bg-zinc-700 text-white font-semibold text-sm transition-all flex flex-col items-center justify-center cursor-pointer disabled:opacity-30 disabled:cursor-not-allowed border border-zinc-900/20 shadow-sm"
                    >
                      <span>{key}</span>
                      {key === '1' && activeCall.ivrMode === 'approval_press' && activeCall.status === 'ivr_active' && (
                        <span className="text-[7px] text-emerald-400 uppercase font-bold tracking-tighter">APPROVE</span>
                      )}
                      {key === '2' && activeCall.ivrMode === 'approval_press' && activeCall.status === 'ivr_active' && (
                        <span className="text-[7px] text-red-400 uppercase font-bold tracking-tighter">REJECT</span>
                      )}
                    </button>
                  ))}
                </div>

                {/* Hang up Button */}
                <div className="flex justify-center mt-2">
                  <button
                    onClick={() => onDeclineCall('rejected')}
                    className="w-12 h-12 bg-red-600 hover:bg-red-700 active:scale-95 text-white rounded-full flex items-center justify-center cursor-pointer shadow-lg shadow-red-600/20"
                  >
                    <PhoneOff className="w-5 h-5" />
                  </button>
                </div>

              </div>
            )}

          </div>

          {/* Swipe Indicator Home Bar */}
          <div className="h-4 pb-2 flex justify-center items-center">
            <div className="w-28 h-1 bg-zinc-800 rounded-full"></div>
          </div>

        </div>
      </div>

      {/* Simulator Control & Network Exception Console (Satisfies P2 & security tests) */}
      <div className="w-full mt-4 bg-zinc-900 border border-zinc-900 rounded-2xl p-4">
        <h4 className="text-xs font-semibold text-zinc-300 font-mono tracking-wider uppercase mb-3 flex items-center">
          <AlertTriangle className="w-3.5 h-3.5 text-amber-400 mr-1.5" />
          Carrier & Fraud Injection Console
        </h4>

        <div className="space-y-3">
          <div>
            <label className="text-[10px] text-zinc-500 font-mono uppercase block mb-1">Simulate Telephone Exceptions</label>
            <div className="grid grid-cols-2 gap-1.5">
              {[
                { key: 'none', label: 'Healthy Network' },
                { key: 'busy', label: 'Signal: Busy Line' },
                { key: 'no_answer', label: 'Signal: No Answer' },
                { key: 'voicemail', label: 'Signal: Voicemail' },
                { key: 'outage', label: 'Signal: Gateway Out' },
              ].map(opt => (
                <button
                  key={opt.key}
                  onClick={() => setSimulateStateOverride(opt.key as any)}
                  className={`text-[10px] font-mono py-1.5 px-2.5 rounded-lg border text-left transition-all cursor-pointer ${
                    simulateStateOverride === opt.key
                      ? 'bg-amber-500/10 border-amber-500/50 text-amber-300 font-bold'
                      : 'bg-zinc-950/40 border-zinc-900 text-zinc-400 hover:border-zinc-900 hover:text-zinc-300'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span>{opt.label}</span>
                    {simulateStateOverride === opt.key && <span className="w-1.5 h-1.5 bg-amber-400 rounded-full animate-ping"></span>}
                  </div>
                </button>
              ))}
            </div>
          </div>

          <div className="pt-2 border-t border-zinc-900/60 text-[10px] text-zinc-500 leading-normal flex items-start space-x-1.5">
            <ShieldAlert className="w-3.5 h-3.5 text-zinc-400 shrink-0 mt-0.5" />
            <span>
              If an exception is active, the simulator automatically responds with carrier signaling triggers during the ringing phase. Perfect for validating robust retry or fallback logic!
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
