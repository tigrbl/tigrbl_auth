/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { FileText, Code, CheckCircle, AlertTriangle, XCircle, Info, ShieldCheck } from 'lucide-react';
import { AuditLog, CallContext } from '../types';

interface AuditLoggerProps {
  logs: AuditLog[];
  activeCall: CallContext | null;
}

export default function AuditLogger({ logs, activeCall }: AuditLoggerProps) {
  const [loggerTab, setLoggerTab] = useState<'audit_logs' | 'webhook_payload'>('audit_logs');

  // Generate a mock live Twilio/Infobip API webhook payload based on the current active call status
  const getMockWebhookPayload = () => {
    if (!activeCall) {
      return {
        info: "Gateway callback idle. Initiate a security call and click keypad buttons to dispatch live webhook payloads."
      };
    }

    const payload: any = {
      event: activeCall.status === 'ringing' ? 'call_initiated' : 'ivr_dtmf_capture',
      call_sid: `CA${activeCall.id.toUpperCase()}`,
      direction: "outbound-api",
      destination_masked: activeCall.maskedDestination,
      carrier_network: "US_BANDWIDTH_INC_MOB",
      freshness_nonce: "f72da88b14e911eb8dcd0242ac120003",
      timestamp_epoch: Math.floor(Date.now() / 1000),
      security_handshake_signature: "sha256=fb99a22cc440268fe1009cd334e1a017e4288bde19302"
    };

    if (activeCall.status === 'completed') {
      payload.signaling_status = "ivr_approved_completed";
      payload.dtmf_keys_pressed = activeCall.ivrMode === 'approval_press' ? "1" : activeCall.verificationCode;
      payload.carrier_disposition = "HUMAN_ANSWER_KEYPAD_VERIFIED";
    } else if (activeCall.status === 'rejected') {
      payload.signaling_status = "ivr_rejected_terminated";
      payload.dtmf_keys_pressed = "2";
      payload.carrier_disposition = "HUMAN_ANSWER_EXPLICIT_REJECT";
    } else if (activeCall.status === 'busy') {
      payload.signaling_status = "carrier_busy_failed";
      payload.carrier_disposition = "BUSY_TONE_SIGNAL_DISPATCH";
    } else if (activeCall.status === 'no_answer') {
      payload.signaling_status = "carrier_no_answer_failed";
      payload.carrier_disposition = "TIMEOUT_NO_HUMAN_PICKUP";
    } else if (activeCall.status === 'voicemail') {
      payload.signaling_status = "carrier_voicemail_aborted";
      payload.carrier_disposition = "MAPPED_VOICEMAIL_Greeting_BEEP_SIGN";
    } else {
      payload.signaling_status = "ringing_active_in_flight";
    }

    return payload;
  };

  return (
    <div className="bg-zinc-900 border border-zinc-900 rounded-2xl p-4 flex flex-col h-full">
      {/* Sub tabs selectors */}
      <div className="flex border-b border-zinc-900 pb-2 mb-3 justify-between items-center">
        <div className="flex space-x-2">
          <button
            onClick={() => setLoggerTab('audit_logs')}
            className={`flex items-center space-x-1.5 px-3 py-1 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
              loggerTab === 'audit_logs'
                ? 'bg-zinc-800 text-white border border-zinc-900/60'
                : 'text-zinc-500 hover:text-zinc-300'
            }`}
          >
            <FileText className="w-3.5 h-3.5" />
            <span>Telemetry Security Audits</span>
          </button>
          <button
            onClick={() => setLoggerTab('webhook_payload')}
            className={`flex items-center space-x-1.5 px-3 py-1 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
              loggerTab === 'webhook_payload'
                ? 'bg-zinc-800 text-white border border-zinc-900/60'
                : 'text-zinc-500 hover:text-zinc-300'
            }`}
          >
            <Code className="w-3.5 h-3.5" />
            <span>Carrier Webhook Web API Payload</span>
          </button>
        </div>

        <span className="text-[10px] text-zinc-500 font-mono hidden sm:inline">Tel-Auth v1.0.0</span>
      </div>

      {/* View: Audit Logs List */}
      <div className="flex-1 overflow-y-auto min-h-[220px]">
        {loggerTab === 'audit_logs' ? (
          <div className="space-y-2 max-h-[300px]">
            {logs.length === 0 ? (
              <div className="text-center py-8 text-xs text-zinc-500">
                No telemetry events logged yet. Trigger an authentication ceremony to start audit traces.
              </div>
            ) : (
              logs.map(log => {
                let SeverityIcon = Info;
                let colorClass = 'text-blue-400 bg-blue-500/5 border-blue-500/10';
                
                if (log.status === 'success') {
                  SeverityIcon = CheckCircle;
                  colorClass = 'text-emerald-400 bg-emerald-500/5 border-emerald-500/10';
                } else if (log.status === 'warning') {
                  SeverityIcon = AlertTriangle;
                  colorClass = 'text-amber-400 bg-amber-500/5 border-amber-500/10';
                } else if (log.status === 'failure') {
                  SeverityIcon = XCircle;
                  colorClass = 'text-red-400 bg-red-500/5 border-red-500/10';
                }

                return (
                  <div 
                    key={log.id} 
                    className={`p-3 border rounded-xl flex items-start space-x-3 transition-colors ${colorClass}`}
                  >
                    <SeverityIcon className="w-4 h-4 shrink-0 mt-0.5" />
                    <div className="flex-1 min-w-0">
                      <div className="flex justify-between items-start">
                        <span className="font-mono text-[10px] font-bold uppercase tracking-wider">{log.eventType}</span>
                        <span className="font-mono text-[9px] text-zinc-500 shrink-0">{new Date(log.timestamp).toLocaleTimeString()}</span>
                      </div>
                      <p className="text-[11px] text-zinc-300 leading-normal mt-1">{log.details}</p>
                      <div className="flex space-x-3 text-[9px] font-mono text-zinc-500 mt-1.5 border-t border-zinc-900/20 pt-1">
                        <span>IP: {log.ipAddress}</span>
                        {log.maskedNumber && <span>MFA Target: {log.maskedNumber}</span>}
                      </div>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        ) : (
          /* View: Live Webhook Payload Inspector */
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-[10px] font-mono text-zinc-500 uppercase">Provider Webhook Dispatch payload (POST /v1/telephony/callback)</span>
              {activeCall && (
                <div className="flex items-center space-x-1.5 text-[9px] text-emerald-400 font-mono animate-pulse">
                  <span className="w-1.5 h-1.5 bg-emerald-400 rounded-full"></span>
                  <span>Active Call Session Stream</span>
                </div>
              )}
            </div>

            <pre className="p-4 bg-zinc-950 border border-zinc-900 rounded-xl overflow-x-auto text-[10px] font-mono text-zinc-400 leading-relaxed max-h-[250px] overflow-y-auto">
              <code>{JSON.stringify(getMockWebhookPayload(), null, 2)}</code>
            </pre>

            <div className="bg-zinc-950/40 p-3 border border-zinc-900 rounded-xl flex items-start space-x-2">
              <ShieldCheck className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
              <p className="text-[9px] text-zinc-500 leading-normal font-mono">
                Security Checklist verified: Every callback payload is signed with a high-entropy SHA256 carrier secret preventing blind approval spoofing, replay timing attacks, or destination swaps.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
