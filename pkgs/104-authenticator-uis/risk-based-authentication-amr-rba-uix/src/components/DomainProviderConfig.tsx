/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { Database, Plus, ShieldCheck, Key, RefreshCw, Trash2, CheckCircle, HelpCircle, Edit } from 'lucide-react';
import { EnterpriseDomain, ServicePrincipalName } from '../types';

interface DomainProviderConfigProps {
  domains: EnterpriseDomain[];
  spns: ServicePrincipalName[];
  onAddDomain: (domain: Omit<EnterpriseDomain, 'id'>) => void;
  onDeleteDomain: (id: string) => void;
  onAddSpn: (spn: Omit<ServicePrincipalName, 'id'>) => void;
  onDeleteSpn: (id: string) => void;
  onRotateSpnKey: (id: string) => void;
}

export default function DomainProviderConfig({
  domains,
  spns,
  onAddDomain,
  onDeleteDomain,
  onAddSpn,
  onDeleteSpn,
  onRotateSpnKey,
}: DomainProviderConfigProps) {
  const [showAddDomain, setShowAddDomain] = useState(false);
  const [domainName, setDomainName] = useState('');
  const [kdcServer, setKdcServer] = useState('');
  const [trustType, setTrustType] = useState<'bidirectional' | 'one-way-incoming' | 'one-way-outgoing' | 'none'>('bidirectional');

  const [showAddSpn, setShowAddSpn] = useState(false);
  const [newSpn, setNewSpn] = useState('');
  const [serviceAccount, setServiceAccount] = useState('');
  const [realm, setRealm] = useState('');
  const [selectedEnc, setSelectedEnc] = useState<string[]>(['AES256-CTS-HMAC-SHA1-96']);

  const handleDomainSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!domainName || !kdcServer) return;
    onAddDomain({
      name: domainName,
      verified: true,
      trustType,
      kdcServer,
      mappedUsersCount: 0,
      lastSync: new Date().toISOString(),
    });
    setDomainName('');
    setKdcServer('');
    setShowAddDomain(false);
  };

  const handleSpnSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newSpn || !serviceAccount || !realm) return;
    onAddSpn({
      spn: newSpn,
      serviceAccount,
      realm,
      encryptionTypes: selectedEnc,
      delegationAllowed: true,
      delegationAllowlist: ['HTTP/*', 'LDAP/*'],
    });
    setNewSpn('');
    setServiceAccount('');
    setRealm('');
    setShowAddSpn(false);
  };

  const toggleEncType = (type: string) => {
    if (selectedEnc.includes(type)) {
      setSelectedEnc(selectedEnc.filter((t) => t !== type));
    } else {
      setSelectedEnc([...selectedEnc, type]);
    }
  };

  return (
    <div id="domain-provider-config" className="space-y-6">
      {/* Active Directory Domains Section */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 space-y-4 shadow-sm">
        <div className="flex justify-between items-center">
          <div>
            <h3 className="font-display font-semibold text-slate-800 text-lg flex items-center gap-2">
              <Database className="w-5 h-5 text-slate-600" />
              Verified Active Directory Domains
            </h3>
            <p className="text-xs text-slate-500">Domains whose workstation Kerberos authentication payloads are authorized on this tenant.</p>
          </div>
          <button
            onClick={() => setShowAddDomain(!showAddDomain)}
            id="btn-add-domain-toggle"
            className="py-1.5 px-3 bg-slate-900 hover:bg-slate-800 text-white rounded-lg text-xs font-semibold flex items-center gap-1 cursor-pointer transition-all"
          >
            <Plus className="w-3.5 h-3.5" /> Register Domain
          </button>
        </div>

        {showAddDomain && (
          <form onSubmit={handleDomainSubmit} className="p-4 bg-slate-50 rounded-xl border border-slate-200 grid grid-cols-1 md:grid-cols-4 gap-4 items-end animate-fadeIn">
            <div>
              <label htmlFor="dom-name" className="block text-[10px] font-medium text-slate-500 uppercase tracking-wider mb-1">Domain FQDN</label>
              <input
                type="text"
                id="dom-name"
                required
                placeholder="e.g. corp.enterprise.local"
                value={domainName}
                onChange={(e) => setDomainName(e.target.value)}
                className="w-full px-2.5 py-1.5 text-xs rounded border border-slate-300 bg-white"
              />
            </div>
            <div>
              <label htmlFor="kdc-host" className="block text-[10px] font-medium text-slate-500 uppercase tracking-wider mb-1">KDC Domain Controller</label>
              <input
                type="text"
                id="kdc-host"
                required
                placeholder="e.g. dc1.corp.enterprise.local"
                value={kdcServer}
                onChange={(e) => setKdcServer(e.target.value)}
                className="w-full px-2.5 py-1.5 text-xs rounded border border-slate-300 bg-white"
              />
            </div>
            <div>
              <label htmlFor="trust-select" className="block text-[10px] font-medium text-slate-500 uppercase tracking-wider mb-1">Realm Trust Level</label>
              <select
                id="trust-select"
                value={trustType}
                onChange={(e: any) => setTrustType(e.target.value)}
                className="w-full px-2 py-1.5 text-xs rounded border border-slate-300 bg-white"
              >
                <option value="bidirectional">Bidirectional Forest Trust</option>
                <option value="one-way-incoming">One-Way Incoming Trust</option>
                <option value="one-way-outgoing">One-Way Outgoing Trust</option>
                <option value="none">External (Untrusted)</option>
              </select>
            </div>
            <button
              type="submit"
              className="py-1.5 px-4 bg-blue-600 hover:bg-blue-700 text-white rounded text-xs font-semibold cursor-pointer"
            >
              Add Domain Realm
            </button>
          </form>
        )}

        <div className="overflow-x-auto border border-slate-100 rounded-xl">
          <table className="w-full text-left text-xs border-collapse">
            <thead className="bg-slate-50 text-[10px] font-semibold text-slate-400 uppercase tracking-wider border-b border-slate-100">
              <tr>
                <th className="p-3">Domain Realm FQDN</th>
                <th className="p-3">Primary KDC DC Host</th>
                <th className="p-3">Forest Trust Path</th>
                <th className="p-3">Active Users</th>
                <th className="p-3">Last Verified</th>
                <th className="p-3 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 font-sans text-slate-700">
              {domains.map((dom) => (
                <tr key={dom.id} className="hover:bg-slate-50/50">
                  <td className="p-3 font-semibold font-mono text-slate-900">{dom.name}</td>
                  <td className="p-3 font-mono text-slate-600">{dom.kdcServer}</td>
                  <td className="p-3">
                    <span className="bg-blue-50 text-blue-800 px-2 py-0.5 rounded text-[10px] font-medium border border-blue-100">
                      {dom.trustType}
                    </span>
                  </td>
                  <td className="p-3 font-mono">{dom.mappedUsersCount}</td>
                  <td className="p-3 text-slate-400 font-mono text-[11px]">{new Date(dom.lastSync).toLocaleDateString()}</td>
                  <td className="p-3 text-right">
                    <button
                      onClick={() => onDeleteDomain(dom.id)}
                      className="text-slate-400 hover:text-rose-600 transition-colors p-1 cursor-pointer"
                      title="Remove Domain Realm"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Service Principal Name (SPN) / SSO Providers Section */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 space-y-4 shadow-sm">
        <div className="flex justify-between items-center">
          <div>
            <h3 className="font-display font-semibold text-slate-800 text-lg flex items-center gap-2">
              <Key className="w-5 h-5 text-slate-600" />
              Service Principal Name (SPN) Registries
            </h3>
            <p className="text-xs text-slate-500">SPN mappings registered in your local KDC directory to grant tickets specifically for this Web Portal.</p>
          </div>
          <button
            onClick={() => setShowAddSpn(!showAddSpn)}
            id="btn-add-spn-toggle"
            className="py-1.5 px-3 bg-slate-900 hover:bg-slate-800 text-white rounded-lg text-xs font-semibold flex items-center gap-1 cursor-pointer transition-all"
          >
            <Plus className="w-3.5 h-3.5" /> Register SPN Map
          </button>
        </div>

        {showAddSpn && (
          <form onSubmit={handleSpnSubmit} className="p-4 bg-slate-50 rounded-xl border border-slate-200 grid grid-cols-1 md:grid-cols-4 gap-4 items-end animate-fadeIn">
            <div>
              <label htmlFor="spn-string" className="block text-[10px] font-medium text-slate-500 uppercase tracking-wider mb-1">SPN Value (Format: service/host)</label>
              <input
                type="text"
                id="spn-string"
                required
                placeholder="e.g. HTTP/sso.corp.com"
                value={newSpn}
                onChange={(e) => setNewSpn(e.target.value)}
                className="w-full px-2.5 py-1.5 text-xs rounded border border-slate-300 bg-white"
              />
            </div>
            <div>
              <label htmlFor="svc-acc" className="block text-[10px] font-medium text-slate-500 uppercase tracking-wider mb-1">AD Service Account</label>
              <input
                type="text"
                id="svc-acc"
                required
                placeholder="e.g. svc_webgateway"
                value={serviceAccount}
                onChange={(e) => setServiceAccount(e.target.value)}
                className="w-full px-2.5 py-1.5 text-xs rounded border border-slate-300 bg-white"
              />
            </div>
            <div>
              <label htmlFor="realm-val" className="block text-[10px] font-medium text-slate-500 uppercase tracking-wider mb-1">KDC Domain Realm</label>
              <input
                type="text"
                id="realm-val"
                required
                placeholder="CORP.ENTERPRISE.LOCAL"
                value={realm}
                onChange={(e) => setRealm(e.target.value)}
                className="w-full px-2.5 py-1.5 text-xs rounded border border-slate-300 bg-white"
              />
            </div>
            <div className="flex flex-col">
              <span className="text-[10px] font-medium text-slate-500 uppercase tracking-wider mb-1">Encryption types</span>
              <div className="flex gap-2">
                <label className="flex items-center gap-1 text-[11px] cursor-pointer">
                  <input
                    type="checkbox"
                    checked={selectedEnc.includes('AES256-CTS-HMAC-SHA1-96')}
                    onChange={() => toggleEncType('AES256-CTS-HMAC-SHA1-96')}
                  />
                  AES256
                </label>
                <label className="flex items-center gap-1 text-[11px] cursor-pointer">
                  <input
                    type="checkbox"
                    checked={selectedEnc.includes('RC4-HMAC')}
                    onChange={() => toggleEncType('RC4-HMAC')}
                  />
                  RC4
                </label>
              </div>
            </div>
            <div className="md:col-span-4 flex justify-end">
              <button
                type="submit"
                className="py-1.5 px-4 bg-blue-600 hover:bg-blue-700 text-white rounded text-xs font-semibold cursor-pointer"
              >
                Register Mapped SPN
              </button>
            </div>
          </form>
        )}

        <div className="overflow-x-auto border border-slate-100 rounded-xl">
          <table className="w-full text-left text-xs border-collapse">
            <thead className="bg-slate-50 text-[10px] font-semibold text-slate-400 uppercase tracking-wider border-b border-slate-100">
              <tr>
                <th className="p-3">SPN (ServicePrincipalName)</th>
                <th className="p-3">AD Mapped Service Account</th>
                <th className="p-3">Target Realm</th>
                <th className="p-3">Allowed Encryption Suite</th>
                <th className="p-3">Delegation Bound</th>
                <th className="p-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 font-sans text-slate-700">
              {spns.map((s) => (
                <tr key={s.id} className="hover:bg-slate-50/50">
                  <td className="p-3 font-semibold font-mono text-blue-600">{s.spn}</td>
                  <td className="p-3 font-mono text-slate-800">{s.serviceAccount}</td>
                  <td className="p-3 font-mono">{s.realm}</td>
                  <td className="p-3">
                    <div className="flex flex-wrap gap-1">
                      {s.encryptionTypes.map((enc, idx) => (
                        <span key={idx} className="bg-slate-100 text-slate-600 px-1.5 py-0.5 rounded text-[10px] font-mono border border-slate-200">
                          {enc}
                        </span>
                      ))}
                    </div>
                  </td>
                  <td className="p-3">
                    <span className="text-[10px] px-1.5 py-0.5 rounded font-mono bg-emerald-50 text-emerald-800 border border-emerald-100">
                      Delegation Allowed
                    </span>
                  </td>
                  <td className="p-3 text-right space-x-2">
                    <button
                      onClick={() => onRotateSpnKey(s.id)}
                      className="text-blue-600 hover:text-blue-800 transition-colors p-1 cursor-pointer inline-flex items-center gap-1"
                      title="Rotate Kerberos Keytab password"
                    >
                      <RefreshCw className="w-3.5 h-3.5" />
                      <span className="text-[10px] font-semibold font-sans">Rotate Key</span>
                    </button>
                    <button
                      onClick={() => onDeleteSpn(s.id)}
                      className="text-slate-400 hover:text-rose-600 transition-colors p-1 cursor-pointer"
                      title="Delete SPN Map"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
