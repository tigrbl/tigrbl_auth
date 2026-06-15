import React from 'react';
import { Card } from '../components/UI';
import './TermsOfServicePage.css';

export const TermsOfServicePage: React.FC = () => {
  return (
    <div className="terms-page">
      <div className="terms-shell u-animate-in">
        <div className="terms-heading">
          <h1 className="terms-title">Terms of Service</h1>
          <p className="terms-updated">Last updated: {new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}</p>
        </div>

        <Card className="terms-card">
          <div className="terms-content">
            <section className="terms-section">
              <h2 className="terms-section-title">1. Acceptance of Terms</h2>
              <p className="terms-copy">
                By accessing and using tigrbl_auth Auth ("the Service"), you agree to be bound by these Terms of Service. If you do not agree to these terms, please do not use our services. We reserve the right to modify these terms at any time, and your continued use of the Service signifies your acceptance of any updated terms.
              </p>
            </section>

            <section className="terms-section">
              <h2 className="terms-section-title">2. User Accounts & Identity</h2>
              <p className="terms-copy">
                tigrbl_auth Auth provides identity federation services via OIDC and OAuth2 protocols. You are responsible for maintaining the confidentiality of your account credentials and for all activities that occur under your account. You agree to notify us immediately of any unauthorized use of your account.
              </p>
              <ul className="terms-list">
                <li>You must provide accurate and complete registration information.</li>
                <li>You may not use the identity of another person or entity.</li>
                <li>Accounts found to be engaging in fraudulent activity will be terminated without notice.</li>
              </ul>
            </section>

            <section className="terms-section">
              <h2 className="terms-section-title">3. Prohibited Conduct</h2>
              <p className="terms-copy">
                You agree not to engage in any of the following prohibited activities:
              </p>
              <ul className="terms-list">
                <li>Attempting to bypass security measures or reverse engineer the authentication protocols.</li>
                <li>Using the Service for any illegal purpose or in violation of any local, state, or international laws.</li>
                <li>Automated scraping or mass-collection of user data.</li>
                <li>Interfering with the proper working of the Service.</li>
              </ul>
            </section>

            <section className="terms-section">
              <h2 className="terms-section-title">4. Privacy and Data Protection</h2>
              <p className="terms-copy">
                Your privacy is important to us. Our use of your personal information is governed by our Privacy Policy. By using the Service, you consent to the collection and use of information by the configured tigrbl_auth public identity surface.
              </p>
            </section>

            <section className="terms-section">
              <h2 className="terms-section-title">5. Limitation of Liability</h2>
              <p className="terms-copy">
                tigrbl_auth Auth is provided "as is" without any warranties. In no event shall tigrbl_auth Auth, its affiliates, or its partners be liable for any indirect, incidental, special, or consequential damages arising out of or in connection with the use of the Service.
              </p>
            </section>

            <section className="terms-section">
              <h2 className="terms-section-title">6. Governing Law</h2>
              <p className="terms-copy">
                These Terms shall be governed by and construed in accordance with the laws of the jurisdiction in which tigrbl_auth Auth operates, without regard to its conflict of law provisions.
              </p>
            </section>

            <div className="terms-actions">
              <button
                onClick={() => window.history.back()}
                className="terms-back"
              >
                <svg className="terms-back-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
                Go Back
              </button>
              <button
                onClick={() => window.location.hash = '#/register'}
                className="terms-register"
              >
                Return to Registration
              </button>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};
