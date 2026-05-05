
import React from 'react';
import { Card } from '../components/UI';
import { User } from '../types';

interface ProfilePageProps {
  user: User;
}

export const ProfilePage: React.FC<ProfilePageProps> = ({ user }) => {
  return (
    <div className="max-w-4xl mx-auto py-12 px-6 space-y-8 animate-in fade-in zoom-in-95 duration-500">
      <div className="flex items-center gap-6">
        <img
          src={user.picture}
          className="w-24 h-24 rounded-2xl border-4 border-white shadow-xl"
          alt={user.name}
        />
        <div>
          <h1 className="text-3xl font-bold text-slate-900">{user.name}</h1>
          <p className="text-slate-500 font-medium">Logged in via {user.provider.charAt(0).toUpperCase() + user.provider.slice(1)}</p>
        </div>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        <Card className="p-6 space-y-2">
          <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">Email Identity</p>
          <p className="text-lg font-semibold text-slate-800 truncate">{user.email}</p>
        </Card>
        <Card className="p-6 space-y-2">
          <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">Global ID</p>
          <p className="text-lg font-semibold text-slate-800">{user.id}</p>
        </Card>
        <Card className="p-6 space-y-2">
          <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">Account Status</p>
          <div className="flex items-center gap-2">
             <div className="w-2 h-2 rounded-full bg-emerald-500"></div>
             <p className="text-lg font-semibold text-emerald-600">Verified</p>
          </div>
        </Card>
      </div>

      <Card className="overflow-hidden">
        <div className="bg-slate-50 px-6 py-4 border-b border-slate-100 flex justify-between items-center">
          <h3 className="font-bold text-slate-700">Active Session Metadata</h3>
          <span className="text-xs bg-indigo-100 text-indigo-700 px-2 py-1 rounded font-bold uppercase">OIDC Context</span>
        </div>
        <div className="p-6">
          <pre className="bg-slate-900 text-indigo-300 p-4 rounded-xl text-sm overflow-x-auto font-mono leading-relaxed">
            {JSON.stringify({
              iss: user.provider === 'google' ? 'https://accounts.google.com' : 'https://github.com',
              sub: user.id,
              aud: 'nexus-app-client',
              iat: Math.floor(Date.now() / 1000),
              exp: Math.floor(Date.now() / 1000) + 3600,
              provider: user.provider
            }, null, 2)}
          </pre>
        </div>
      </Card>
    </div>
  );
};
