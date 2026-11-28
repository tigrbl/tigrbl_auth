/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useRef } from 'react';
import { Camera, ShieldAlert, Sparkles, RefreshCw, Volume2, HelpCircle, UserCheck, AlertOctagon } from 'lucide-react';
import { motion } from 'motion/react';

interface FaceCaptureShellProps {
  purpose: 'enrollment' | 'login' | 'step_up' | 'replacement';
  challenge: string;
  onSuccess: (evidenceData: any) => void;
  onFailure: (reason: string, isSpoof: boolean) => void;
  onCancel: () => void;
}

export const FaceCaptureShell: React.FC<FaceCaptureShellProps> = ({
  purpose,
  challenge,
  onSuccess,
  onFailure,
  onCancel
}) => {
  const [step, setStep] = useState<'align' | 'blink' | 'still' | 'processing'>('align');
  const [progress, setProgress] = useState(15);
  const [correctiveText, setCorrectiveText] = useState('Align face inside the bounding circle.');
  const [spokenEquiv, setSpokenEquiv] = useState('Please position your face in the center of the frame and remain still.');
  const [voiceSynthesized, setVoiceSynthesized] = useState(false);
  const [livenessResult, setLivenessResult] = useState<'none' | 'success' | 'spoof_detected' | 'insufficient_quality'>('none');
  const [frameNum, setFrameNum] = useState(0);

  // Simulation controls
  const [simulateOutcome, setSimulateOutcome] = useState<'success' | 'spoof' | 'quality'>('success');

  // Animation ticks for simulated video feed
  useEffect(() => {
    const timer = setInterval(() => {
      setFrameNum((prev) => prev + 1);
    }, 150);
    return () => clearInterval(timer);
  }, []);

  // Liveness wizard state machine
  useEffect(() => {
    let t1: any, t2: any, t3: any;

    if (step === 'align') {
      setProgress(25);
      setCorrectiveText('Position face inside the green circle. Ensure adequate lighting.');
      setSpokenEquiv('Position face inside the green circle. Ensure adequate lighting.');
      t1 = setTimeout(() => {
        setStep('blink');
      }, 2500);
    } else if (step === 'blink') {
      setProgress(55);
      setCorrectiveText('Liveness Challenge: Please BLINK slowly twice.');
      setSpokenEquiv('Challenge active. Please blink slowly twice now to verify liveness.');
      t2 = setTimeout(() => {
        setStep('still');
      }, 2800);
    } else if (step === 'still') {
      setProgress(85);
      setCorrectiveText('Liveness Challenge: Hold still for 3D depth alignment...');
      setSpokenEquiv('Liveness challenge: Please hold completely still for final 3D depth alignment.');
      t3 = setTimeout(() => {
        setStep('processing');
        setProgress(100);
        evaluateVerification();
      }, 3000);
    }

    return () => {
      clearTimeout(t1);
      clearTimeout(t2);
      clearTimeout(t3);
    };
  }, [step]);

  const evaluateVerification = () => {
    setCorrectiveText('Verifying signed cryptotoken in verifier boundary...');
    setSpokenEquiv('Processing securely on server. Please wait.');
    
    setTimeout(() => {
      if (simulateOutcome === 'success') {
        setLivenessResult('success');
        onSuccess({
          challenge,
          purpose,
          hardwareBacked: true,
          verificationTime: new Date().toISOString(),
          issuer: 'approved-native-enclave-v4',
          trustLevel: 'high_attested'
        });
      } else if (simulateOutcome === 'spoof') {
        setLivenessResult('spoof_detected');
        onFailure('Presentation Attack Detected: Simulated photograph or video replay suspected.', true);
      } else {
        setLivenessResult('insufficient_quality');
        onFailure('Biometric Capture Rejected: Excessive shadows or partial face occlusion detected.', false);
      }
    }, 2000);
  };

  const speakText = () => {
    // Standard web speech synthesis wrapper
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(spokenEquiv);
      utterance.rate = 1.0;
      window.speechSynthesis.speak(utterance);
      setVoiceSynthesized(true);
      setTimeout(() => setVoiceSynthesized(false), 2000);
    } else {
      alert('Speech synthesis is not supported in this browser environment.');
    }
  };

  return (
    <div id="face-capture-shell-card" className="bg-white border border-gray-200 rounded-2xl shadow-sm p-6 max-w-xl mx-auto text-center">
      {/* Transaction header */}
      <div className="flex items-center justify-between border-b border-gray-100 pb-3 mb-5">
        <div className="text-left">
          <span className="text-[10px] uppercase font-bold text-gray-400 tracking-wider">Secure Native Capture Boundary</span>
          <h4 className="text-sm font-semibold text-gray-900 capitalize flex items-center gap-1.5">
            <Sparkles className="w-4 h-4 text-indigo-500" /> 
            {purpose === 'enrollment' ? 'Enrollment Ceremony' : purpose === 'replacement' ? 'Template Retraining Ceremony' : 'First-Party Identity Verification'}
          </h4>
        </div>
        <div className="text-right">
          <span className="text-[10px] font-mono text-gray-500 bg-gray-50 px-2 py-0.5 rounded border border-gray-200">
            CHALLENGE: {challenge.substring(0, 10)}...
          </span>
        </div>
      </div>

      {/* Simulator configuration panel */}
      <div className="bg-indigo-50/50 border border-indigo-100 rounded-xl p-3 mb-5 text-left text-xs">
        <div className="flex items-center justify-between">
          <span className="font-semibold text-indigo-900 flex items-center gap-1">
            <HelpCircle className="w-4 h-4 text-indigo-600" /> Biometric Capture Sandbox Parameters
          </span>
          <span className="font-mono text-[9px] text-indigo-500 uppercase bg-indigo-100 px-1.5 py-0.5 rounded">Interactive Override</span>
        </div>
        <p className="text-gray-600 text-[11px] mt-1">
          Adjust the outcome parameter to test presentation attack detection (liveness failures), inadequate light flags, or successful completion.
        </p>
        <div className="flex gap-4 mt-3">
          <label className="flex items-center gap-1.5 cursor-pointer text-gray-700">
            <input
              type="radio"
              name="simulateOutcome"
              checked={simulateOutcome === 'success'}
              onChange={() => setSimulateOutcome('success')}
              className="text-indigo-600 focus:ring-indigo-500"
            />
            <span>Successful Verification</span>
          </label>
          <label className="flex items-center gap-1.5 cursor-pointer text-gray-700">
            <input
              type="radio"
              name="simulateOutcome"
              checked={simulateOutcome === 'spoof'}
              onChange={() => setSimulateOutcome('spoof')}
              className="text-red-600 focus:ring-red-500"
            />
            <span className="text-red-700 font-medium">Suspected Spoof (PAD)</span>
          </label>
          <label className="flex items-center gap-1.5 cursor-pointer text-gray-700">
            <input
              type="radio"
              name="simulateOutcome"
              checked={simulateOutcome === 'quality'}
              onChange={() => setSimulateOutcome('quality')}
              className="text-amber-600 focus:ring-amber-500"
            />
            <span className="text-amber-700">Occlusion/Low Quality</span>
          </label>
        </div>
      </div>

      {/* Camera Video Simulator Screen */}
      <div className="relative w-[320px] h-[320px] mx-auto bg-gray-950 rounded-full overflow-hidden border-4 border-gray-800 flex items-center justify-center mb-5 shadow-inner">
        {/* Animated grid overlay to indicate active camera scanner */}
        <div className="absolute inset-0 bg-[radial-gradient(#ffffff08_1px,transparent_1px)] [background-size:16px_16px] pointer-events-none" />

        {/* Outer glowing scan ring */}
        <div className={`absolute inset-4 rounded-full border-2 transition-all duration-700 pointer-events-none ${
          step === 'processing' 
            ? 'border-indigo-500 border-dashed animate-spin' 
            : step === 'still'
            ? 'border-green-500 scale-102 shadow-[0_0_15px_rgba(34,197,94,0.3)]'
            : 'border-indigo-400 animate-pulse'
        }`} />

        {/* Facial Landmark Guide Outline */}
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none opacity-85">
          <svg className="w-60 h-60 text-gray-600" viewBox="0 0 100 100" fill="none" stroke="currentColor" strokeWidth="1.2">
            {/* Outer Head Outline */}
            <path d="M50 15 C30 15, 20 30, 20 55 C20 75, 35 90, 50 90 C65 90, 80 75, 80 55 C80 30, 70 15, 50 15 Z" 
              stroke={step === 'still' ? '#22c55e' : step === 'blink' ? '#6366f1' : '#4b5563'} 
              strokeWidth={step === 'still' || step === 'blink' ? '2' : '1.2'}
              className="transition-colors duration-300"
            />
            {/* Eyes Guide */}
            {step === 'blink' && (frameNum % 4 === 0 || frameNum % 4 === 1) ? (
              <>
                {/* Closed eyes for blinking animation */}
                <line x1="32" y1="42" x2="42" y2="42" stroke="#6366f1" strokeWidth="2.5" />
                <line x1="58" y1="42" x2="68" y2="42" stroke="#6366f1" strokeWidth="2.5" />
              </>
            ) : (
              <>
                {/* Normal open eyes guide */}
                <circle cx="37" cy="42" r="3" fill="none" stroke={step === 'still' ? '#22c55e' : '#9ca3af'} strokeWidth="1.2" />
                <circle cx="63" cy="42" r="3" fill="none" stroke={step === 'still' ? '#22c55e' : '#9ca3af'} strokeWidth="1.2" />
              </>
            )}
            {/* Nose Bridge */}
            <path d="M50 40 L50 60 L46 64" stroke={step === 'still' ? '#22c55e' : '#4b5563'} />
            {/* Mouth outline */}
            <path d="M40 75 Q50 78 60 75" stroke={step === 'still' ? '#22c55e' : '#4b5563'} strokeWidth="1.5" fill="none" />
          </svg>
        </div>

        {/* Live Scan Tracker Lines */}
        {step === 'processing' && (
          <div className="absolute w-full h-1 bg-indigo-500 shadow-[0_0_10px_#6366f1] top-1/2 left-0 animate-bounce" />
        )}

        {/* Status Text overlay inside view */}
        <div className="absolute bottom-6 left-0 right-0 text-center pointer-events-none">
          <span className="bg-gray-900/95 border border-gray-800 text-white font-mono text-[10px] px-2.5 py-1 rounded-full uppercase tracking-wider">
            {step === 'align' && 'Phase 1: Aligning Face'}
            {step === 'blink' && 'Phase 2: Liveness Test'}
            {step === 'still' && 'Phase 3: 3D Depth Check'}
            {step === 'processing' && 'Enclave Encryption...'}
          </span>
        </div>
      </div>

      {/* Quality Guidance Display / Corrector Status */}
      <div className="bg-gray-50 border border-gray-100 rounded-xl p-4 mb-5 text-center min-h-[72px] flex flex-col justify-center items-center">
        <p className="text-sm font-semibold text-gray-800 transition-all duration-300">
          {correctiveText}
        </p>
        
        {/* spoken-text assistive audio button */}
        <div className="flex items-center gap-1.5 mt-2">
          <button
            type="button"
            onClick={speakText}
            title="Read corrective audio instructions aloud"
            className={`flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-medium border transition ${
              voiceSynthesized 
                ? 'bg-green-50 border-green-200 text-green-700' 
                : 'bg-white border-gray-200 text-gray-600 hover:bg-gray-100'
            }`}
          >
            <Volume2 className="w-3.5 h-3.5" />
            {voiceSynthesized ? 'Reading guidance aloud...' : 'Assistive Spoken Audio'}
          </button>
        </div>
      </div>

      {/* Progress Bar indicator */}
      <div className="w-full bg-gray-100 h-2 rounded-full overflow-hidden mb-6">
        <div 
          className="bg-indigo-600 h-full transition-all duration-500 ease-out"
          style={{ width: `${progress}%` }}
        />
      </div>

      {/* Actions */}
      <div className="flex items-center justify-between">
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 border border-gray-200 hover:bg-gray-50 text-gray-700 text-xs font-semibold rounded-xl transition"
        >
          Cancel Ceremony
        </button>

        <span className="text-[11px] text-gray-400 font-mono flex items-center gap-1">
          <Camera className="w-3.5 h-3.5" /> Direct Enclave Bound • No Media Saved
        </span>
      </div>
    </div>
  );
};
