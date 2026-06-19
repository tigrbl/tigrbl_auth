
import React from 'react';
import { Card } from '../components/UI';
import { User } from '../types';
import './ProfilePage.css';

interface ProfilePageProps {
  user: User;
}

const stringifyClaim = (value: unknown): string => {
  if (Array.isArray(value)) {
    return value.join(' ');
  }
  if (typeof value === 'boolean') {
    return value ? 'true' : 'false';
  }
  if (value === null || value === undefined || value === '') {
    return 'Not provided';
  }
  return String(value);
};

const claimValue = (claims: Record<string, unknown>, key: string): string => {
  return stringifyClaim(claims[key]);
};

export const ProfilePage: React.FC<ProfilePageProps> = ({ user }) => {
  const myAccountUrl = import.meta.env.VITE_TIGRBL_AUTH_MY_ACCOUNT_UIX_URL || 'http://localhost:3019';
  const oidcContext = user.oidcContext || {
    id_token: {
      sub: user.id,
    },
    access_token: {},
    userinfo: {
      sub: user.id,
      email: user.email,
      name: user.name,
      email_verified: user.isEmailVerified,
    },
    client: {
      provider: user.provider,
      client_id: 'unknown',
      issuer: 'unknown',
      scope: 'unknown',
    },
    authorization_request: {
      redirect_uri: 'unknown',
    },
  };
  const idToken = oidcContext.id_token || {};
  const accessToken = oidcContext.access_token || {};
  const userinfo = oidcContext.userinfo || {};
  const subject = claimValue(userinfo, 'sub') !== 'Not provided'
    ? claimValue(userinfo, 'sub')
    : claimValue(idToken, 'sub');
  const email = claimValue(userinfo, 'email') !== 'Not provided'
    ? claimValue(userinfo, 'email')
    : user.email;
  const name = claimValue(userinfo, 'name') !== 'Not provided'
    ? claimValue(userinfo, 'name')
    : user.name;
  const grantedScope = claimValue(accessToken, 'scope') !== 'Not provided'
    ? claimValue(accessToken, 'scope')
    : oidcContext.client.scope;

  return (
    <div className="profile-page profile-stack u-animate-in">
      <div className="profile-header">
        {user.picture ? (
          <img
            src={user.picture}
            className="profile-avatar"
            alt={user.name}
          />
        ) : (
          <div className="profile-avatar-fallback" aria-label={user.name}>
            {String(user.name || user.email || 'U').slice(0, 1).toUpperCase()}
          </div>
        )}
        <div>
          <h1 className="profile-title">{user.name}</h1>
          <p className="profile-subtitle">Logged in via tigrbl_auth</p>
        </div>
      </div>

      <div className="profile-grid">
        <Card className="profile-metric-card profile-metric-stack">
          <p className="profile-label">Email Identity</p>
          <p className="profile-value">{email}</p>
          <p className="profile-source">Source: UserInfo</p>
        </Card>
        <Card className="profile-metric-card profile-metric-stack">
          <p className="profile-label">Global ID</p>
          <p className="profile-value">{subject}</p>
          <p className="profile-source">Source: UserInfo subject</p>
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
          <div className="profile-oidc-summary" aria-label="OIDC context summary">
            <div className="profile-oidc-row">
              <span className="profile-oidc-key">Issuer</span>
              <span className="profile-oidc-value">{claimValue(idToken, 'iss')}</span>
              <span className="profile-oidc-source">ID token</span>
            </div>
            <div className="profile-oidc-row">
              <span className="profile-oidc-key">Subject</span>
              <span className="profile-oidc-value">{subject}</span>
              <span className="profile-oidc-source">UserInfo</span>
            </div>
            <div className="profile-oidc-row">
              <span className="profile-oidc-key">Audience</span>
              <span className="profile-oidc-value">{claimValue(idToken, 'aud')}</span>
              <span className="profile-oidc-source">ID token</span>
            </div>
            <div className="profile-oidc-row">
              <span className="profile-oidc-key">Issued At</span>
              <span className="profile-oidc-value">{claimValue(idToken, 'iat')}</span>
              <span className="profile-oidc-source">ID token</span>
            </div>
            <div className="profile-oidc-row">
              <span className="profile-oidc-key">Expires</span>
              <span className="profile-oidc-value">{claimValue(idToken, 'exp')}</span>
              <span className="profile-oidc-source">ID token</span>
            </div>
            <div className="profile-oidc-row">
              <span className="profile-oidc-key">Nonce</span>
              <span className="profile-oidc-value">{claimValue(idToken, 'nonce')}</span>
              <span className="profile-oidc-source">ID token</span>
            </div>
            <div className="profile-oidc-row">
              <span className="profile-oidc-key">Auth Time</span>
              <span className="profile-oidc-value">{claimValue(idToken, 'auth_time')}</span>
              <span className="profile-oidc-source">ID token</span>
            </div>
            <div className="profile-oidc-row">
              <span className="profile-oidc-key">Session ID</span>
              <span className="profile-oidc-value">{claimValue(idToken, 'sid')}</span>
              <span className="profile-oidc-source">ID token</span>
            </div>
            <div className="profile-oidc-row">
              <span className="profile-oidc-key">Token Type</span>
              <span className="profile-oidc-value">{stringifyClaim(oidcContext.client.token_type)}</span>
              <span className="profile-oidc-source">Token response</span>
            </div>
            <div className="profile-oidc-row">
              <span className="profile-oidc-key">Scope</span>
              <span className="profile-oidc-value">{grantedScope}</span>
              <span className="profile-oidc-source">Access token</span>
            </div>
            <div className="profile-oidc-row">
              <span className="profile-oidc-key">Email</span>
              <span className="profile-oidc-value">{email}</span>
              <span className="profile-oidc-source">UserInfo</span>
            </div>
            <div className="profile-oidc-row">
              <span className="profile-oidc-key">Name</span>
              <span className="profile-oidc-value">{name}</span>
              <span className="profile-oidc-source">UserInfo</span>
            </div>
            <div className="profile-oidc-row">
              <span className="profile-oidc-key">Email Verified</span>
              <span className="profile-oidc-value">{claimValue(userinfo, 'email_verified')}</span>
              <span className="profile-oidc-source">UserInfo</span>
            </div>
          </div>
          <pre className="profile-session-code">
            {JSON.stringify(oidcContext, null, 2)}
          </pre>
        </div>
      </Card>
    </div>
  );
};
