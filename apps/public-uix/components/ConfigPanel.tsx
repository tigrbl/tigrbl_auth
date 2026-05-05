
import React, { useState, useEffect } from 'react';
import { Modal, Input } from './UI';
import { usePlatform } from '../hooks/usePlatform';
import { PlatformConfig } from '../types';

interface ConfigPanelProps {
  isOpen: boolean;
  onClose: () => void;
  showBrandingSettings: boolean;
  showAdapterSettings: boolean;
}

export const ConfigPanel: React.FC<ConfigPanelProps> = ({
  isOpen,
  onClose,
  showBrandingSettings,
  showAdapterSettings
}) => {
  const platform = usePlatform();
  const [config, setConfig] = useState({
    VITE_GOOGLE_CLIENT_ID: '',
    VITE_GITHUB_CLIENT_ID: '',
    VITE_KEYCLOAK_CLIENT_ID: '',
    VITE_KEYCLOAK_AUTHORITY: '',
    VITE_GENERIC_CLIENT_ID: '',
    VITE_GENERIC_AUTHORITY: '',
    VITE_GENERIC_SCOPE: '',
  });

  const [platformConfig, setPlatformConfig] = useState<PlatformConfig>({ ...platform });

  useEffect(() => {
    if (isOpen) {
      const newConfig = { ...config };
      Object.keys(config).forEach(key => {
        const val = localStorage.getItem(`nexus_env_${key}`);
        if (val) (newConfig as any)[key] = val;
      });
      setConfig(newConfig);
      setPlatformConfig({ ...platform });
    }
  }, [isOpen]);

  const handleSave = () => {
    Object.entries(config).forEach(([key, value]) => {
      if (value) localStorage.setItem(`nexus_env_${key}`, value as string);
      else localStorage.removeItem(`nexus_env_${key}`);
    });
    platform.updatePlatform(platformConfig);
    onClose();
    window.location.reload();
  };

  const handleClear = () => {
    localStorage.clear();
    onClose();
    window.location.reload();
  };

  const panelTitle = showBrandingSettings && showAdapterSettings
    ? 'Platform Whitelabeling & OIDC Settings'
    : showBrandingSettings
      ? 'Platform Whitelabeling Settings'
      : 'OIDC Adapter Settings';

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={panelTitle}>
      <div className="space-y-8">

        {/* IDENTITY SECTION */}
        {showBrandingSettings && (
          <div className="space-y-4">
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-widest border-b border-slate-100 pb-2">Identity & Branding</h3>
            <div className="grid grid-cols-2 gap-4">
              <Input
                label="App Name"
                value={platformConfig.name}
                onChange={e => setPlatformConfig({...platformConfig, name: e.target.value})}
              />
              <Input
                label="Logo Symbol"
                placeholder="N"
                value={platformConfig.logoLetter}
                onChange={e => setPlatformConfig({...platformConfig, logoLetter: e.target.value.slice(0, 1)})}
              />
            </div>
            <Input
              label="Support Contact"
              value={platformConfig.supportEmail}
              onChange={e => setPlatformConfig({...platformConfig, supportEmail: e.target.value})}
            />
          </div>
        )}

        {/* NAVIGATION SECTION */}
        {showBrandingSettings && (
          <div className="space-y-4">
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-widest border-b border-slate-100 pb-2">Navigation & Flow</h3>
            <Input
              label="Post-Login Landing URI"
              placeholder="#/profile"
              value={platformConfig.postLoginRedirectUri}
              onChange={e => setPlatformConfig({...platformConfig, postLoginRedirectUri: e.target.value})}
            />
            <p className="text-[10px] text-slate-400 italic">Determines where users are redirected after successful authentication.</p>
          </div>
        )}

        {/* VISUAL DESIGN TOKENS */}
        {showBrandingSettings && (
          <div className="space-y-4">
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-widest border-b border-slate-100 pb-2">Visual Style (CSS Tokens)</h3>
            <div className="grid grid-cols-2 gap-4">
               <div className="space-y-1.5">
                 <label className="text-xs font-semibold text-slate-700">Primary Color</label>
                 <input
                   type="color"
                   value={platformConfig.primaryColor}
                   onChange={e => setPlatformConfig({...platformConfig, primaryColor: e.target.value})}
                   className="w-full h-10 rounded-md cursor-pointer border border-slate-200"
                 />
               </div>
               <div className="space-y-1.5">
                 <label className="text-xs font-semibold text-slate-700">Surface Tint</label>
                 <input
                   type="color"
                   value={platformConfig.backgroundColor}
                   onChange={e => setPlatformConfig({...platformConfig, backgroundColor: e.target.value})}
                   className="w-full h-10 rounded-md cursor-pointer border border-slate-200"
                 />
               </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <Input
                label="Rounding (px)"
                placeholder="12px"
                value={platformConfig.borderRadius}
                onChange={e => setPlatformConfig({...platformConfig, borderRadius: e.target.value})}
              />
               <div className="space-y-1.5">
                 <label className="text-xs font-semibold text-slate-700">Secondary Accent</label>
                 <input
                   type="color"
                   value={platformConfig.secondaryColor}
                   onChange={e => setPlatformConfig({...platformConfig, secondaryColor: e.target.value})}
                   className="w-full h-10 rounded-md cursor-pointer border border-slate-200"
                 />
               </div>
            </div>
          </div>
        )}

        {/* CONTENT LABELS SECTION */}
        {showBrandingSettings && (
          <div className="space-y-4">
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-widest border-b border-slate-100 pb-2">Identity Hub Content</h3>
            <div className="space-y-4">
              <div className="p-3 bg-slate-50 rounded-brand space-y-3">
                <p className="text-[10px] font-bold text-slate-400 uppercase">Login Page Strings</p>
                <Input label="Login Title" value={platformConfig.loginTitle} onChange={e => setPlatformConfig({...platformConfig, loginTitle: e.target.value})} />
                <Input label="Login Subtitle" value={platformConfig.loginSubtitle} onChange={e => setPlatformConfig({...platformConfig, loginSubtitle: e.target.value})} />
              </div>
              <div className="p-3 bg-slate-50 rounded-brand space-y-3">
                <p className="text-[10px] font-bold text-slate-400 uppercase">Register Page Strings</p>
                <Input label="Register Title" value={platformConfig.registerTitle} onChange={e => setPlatformConfig({...platformConfig, registerTitle: e.target.value})} />
                <Input label="Register Subtitle" value={platformConfig.registerSubtitle} onChange={e => setPlatformConfig({...platformConfig, registerSubtitle: e.target.value})} />
              </div>
            </div>
          </div>
        )}

        {/* OIDC ADAPTERS SECTION */}
        {showAdapterSettings && (
          <div className="space-y-4">
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-widest border-b border-slate-100 pb-2">OIDC Adapter Engine</h3>
            <div className="space-y-3">
              <Input label="Google Client ID" value={config.VITE_GOOGLE_CLIENT_ID} onChange={e => setConfig({...config, VITE_GOOGLE_CLIENT_ID: e.target.value})} />
              <Input label="GitHub Client ID" value={config.VITE_GITHUB_CLIENT_ID} onChange={e => setConfig({...config, VITE_GITHUB_CLIENT_ID: e.target.value})} />
            </div>
          </div>
        )}

        <div className="flex gap-3 pt-4 border-t border-slate-100">
          <button
            onClick={handleSave}
            className="flex-grow bg-brand text-white py-3 rounded-brand font-bold shadow-lg shadow-brand/40 hover:opacity-90 transition-all"
          >
            Deploy Changes
          </button>
          <button
            onClick={handleClear}
            className="px-4 py-3 bg-white border border-slate-200 text-slate-600 rounded-brand font-bold hover:bg-slate-50 transition-all"
          >
            Reset
          </button>
        </div>
      </div>
    </Modal>
  );
};
