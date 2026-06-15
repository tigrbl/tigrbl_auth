
import React from 'react';
import { Card } from '../components/UI';
import { User } from '../types';
import './ProfilePage.css';

interface ProfilePageProps {
  user: User;
}

export const ProfilePage: React.FC<ProfilePageProps> = ({ user }) => {
  const myAccountUrl = import.meta.env.VITE_TIGRBL_AUTH_MY_ACCOUNT_UIX_URL || 'http://localhost:3019';

  return (
    <div className="profile-page profile-stack u-animate-in">
      <div className="profile-header">
        <img
          src={user.picture}
          className="profile-avatar"
          alt={user.name}
        />
        <div>
          <h1 className="profile-title">{user.name}</h1>
          <p className="profile-subtitle">Logged in via tigrbl_auth</p>
        </div>
      </div>

      <div className="profile-grid">
        <Card className="profile-metric-card profile-metric-stack">
          <p className="profile-label">Email Identity</p>
          <p className="profile-value">{user.email}</p>
        </Card>
        <Card className="profile-metric-card profile-metric-stack">
          <p className="profile-label">Global ID</p>
          <p className="profile-value">{user.id}</p>
        </Card>
        <Card className="profile-metric-card profile-metric-stack">
          <p className="profile-label">Account Status</p>
          <div className="profile-status">
             <div className="profile-status-dot"></div>
             <p className="profile-status-text">Verified</p>
          </div>
        </Card>
      </div>

      <div className="profile-self-service">
        <div>
          <h2 className="profile-self-service-title">Account self-service</h2>
          <p className="profile-self-service-text">Manage profile details, sessions, credentials, and authorized apps.</p>
        </div>
        <a className="profile-self-service-link" href={myAccountUrl}>
          Open My Account
        </a>
      </div>

      <Card className="profile-session-card">
        <div className="profile-session-header">
          <h3 className="profile-session-title">Active Session Metadata</h3>
          <span className="profile-session-badge">OIDC Context</span>
        </div>
        <div className="profile-session-body">
          <pre className="profile-session-code">
            {JSON.stringify({
              iss: 'tigrbl_auth',
              sub: user.id,
              aud: 'tigrbl-auth-public-uix',
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
