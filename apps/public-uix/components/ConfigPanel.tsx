import React, { useState, useEffect } from 'react';
import { Modal, Input } from './UI';
import { usePlatform } from '../hooks/usePlatform';
import { PlatformConfig } from '../types';
import './ConfigPanel.css';

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
    VITE_TIGRBL_AUTH_CLIENT_ID: '',
  });

  const [platformConfig, setPlatformConfig] = useState<PlatformConfig>({ ...platform });

  useEffect(() => {
    if (isOpen) {
      const newConfig = { ...config };
      Object.keys(config).forEach(key => {
        const val = localStorage.getItem(`tigrbl_auth_env_${key}`);
        if (val) (newConfig as any)[key] = val;
      });
      setConfig(newConfig);
      setPlatformConfig({ ...platform });
    }
  }, [isOpen]);

  const handleSave = () => {
    Object.entries(config).forEach(([key, value]) => {
      if (value) localStorage.setItem(`tigrbl_auth_env_${key}`, value as string);
      else localStorage.removeItem(`tigrbl_auth_env_${key}`);
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
      <div className="config-panel-stack">
        {showBrandingSettings && (
          <div className="config-panel-section">
            <h3 className="config-panel-title">Identity & Branding</h3>
            <div className="config-panel-grid">
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

        {showBrandingSettings && (
          <div className="config-panel-section">
            <h3 className="config-panel-title">Navigation & Flow</h3>
            <Input
              label="Post-Login Landing URI"
              placeholder="#/profile"
              value={platformConfig.postLoginRedirectUri}
              onChange={e => setPlatformConfig({...platformConfig, postLoginRedirectUri: e.target.value})}
            />
            <p className="config-panel-note">Determines where users are redirected after successful authentication.</p>
          </div>
        )}

        {showBrandingSettings && (
          <div className="config-panel-section">
            <h3 className="config-panel-title">Visual Style (CSS Tokens)</h3>
            <div className="config-panel-grid">
              <div className="config-panel-color-field">
                <label className="config-panel-label">Primary Color</label>
                <input
                  type="color"
                  value={platformConfig.primaryColor}
                  onChange={e => setPlatformConfig({...platformConfig, primaryColor: e.target.value})}
                  className="config-panel-color-input"
                />
              </div>
              <div className="config-panel-color-field">
                <label className="config-panel-label">Surface Tint</label>
                <input
                  type="color"
                  value={platformConfig.backgroundColor}
                  onChange={e => setPlatformConfig({...platformConfig, backgroundColor: e.target.value})}
                  className="config-panel-color-input"
                />
              </div>
            </div>
            <div className="config-panel-grid">
              <Input
                label="Rounding (px)"
                placeholder="12px"
                value={platformConfig.borderRadius}
                onChange={e => setPlatformConfig({...platformConfig, borderRadius: e.target.value})}
              />
              <div className="config-panel-color-field">
                <label className="config-panel-label">Secondary Accent</label>
                <input
                  type="color"
                  value={platformConfig.secondaryColor}
                  onChange={e => setPlatformConfig({...platformConfig, secondaryColor: e.target.value})}
                  className="config-panel-color-input"
                />
              </div>
            </div>
          </div>
        )}

        {showBrandingSettings && (
          <div className="config-panel-section">
            <h3 className="config-panel-title">Identity Hub Content</h3>
            <div className="config-panel-content-stack">
              <div className="config-panel-string-group">
                <p className="config-panel-string-title">Login Page Strings</p>
                <Input label="Login Title" value={platformConfig.loginTitle} onChange={e => setPlatformConfig({...platformConfig, loginTitle: e.target.value})} />
                <Input label="Login Subtitle" value={platformConfig.loginSubtitle} onChange={e => setPlatformConfig({...platformConfig, loginSubtitle: e.target.value})} />
              </div>
              <div className="config-panel-string-group">
                <p className="config-panel-string-title">Register Page Strings</p>
                <Input label="Register Title" value={platformConfig.registerTitle} onChange={e => setPlatformConfig({...platformConfig, registerTitle: e.target.value})} />
                <Input label="Register Subtitle" value={platformConfig.registerSubtitle} onChange={e => setPlatformConfig({...platformConfig, registerSubtitle: e.target.value})} />
              </div>
            </div>
          </div>
        )}

        {showAdapterSettings && (
          <div className="config-panel-section">
            <h3 className="config-panel-title">OIDC Client</h3>
            <div className="config-panel-section">
              <Input label="Client ID" value={config.VITE_TIGRBL_AUTH_CLIENT_ID} onChange={e => setConfig({...config, VITE_TIGRBL_AUTH_CLIENT_ID: e.target.value})} />
            </div>
          </div>
        )}

        <div className="config-panel-actions">
          <button
            onClick={handleSave}
            className="config-panel-save"
          >
            Deploy Changes
          </button>
          <button
            onClick={handleClear}
            className="config-panel-reset"
          >
            Reset
          </button>
        </div>
      </div>
    </Modal>
  );
};
