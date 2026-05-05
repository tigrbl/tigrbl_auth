
import React from 'react';
import { Card } from '../components/UI';

export const TermsOfServicePage: React.FC = () => {
  return (
    <div className="flex-grow bg-slate-50 py-12 px-6">
      <div className="max-w-3xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-extrabold text-slate-900 tracking-tight">Terms of Service</h1>
          <p className="text-slate-500">Last updated: {new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}</p>
        </div>

        <Card className="p-8 md:p-12 prose prose-slate max-w-none">
          <div className="space-y-10">
            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-slate-800 border-b border-slate-100 pb-2">1. Acceptance of Terms</h2>
              <p className="text-slate-600 leading-relaxed">
                By accessing and using tigrbl_auth Auth ("the Service"), you agree to be bound by these Terms of Service. If you do not agree to these terms, please do not use our services. We reserve the right to modify these terms at any time, and your continued use of the Service signifies your acceptance of any updated terms.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-slate-800 border-b border-slate-100 pb-2">2. User Accounts & Identity</h2>
              <p className="text-slate-600 leading-relaxed">
                tigrbl_auth Auth provides identity federation services via OIDC and OAuth2 protocols. You are responsible for maintaining the confidentiality of your account credentials and for all activities that occur under your account. You agree to notify us immediately of any unauthorized use of your account.
              </p>
              <ul className="list-disc list-inside text-slate-600 space-y-2 ml-4">
                <li>You must provide accurate and complete registration information.</li>
                <li>You may not use the identity of another person or entity.</li>
                <li>Accounts found to be engaging in fraudulent activity will be terminated without notice.</li>
              </ul>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-slate-800 border-b border-slate-100 pb-2">3. Prohibited Conduct</h2>
              <p className="text-slate-600 leading-relaxed">
                You agree not to engage in any of the following prohibited activities:
              </p>
              <ul className="list-disc list-inside text-slate-600 space-y-2 ml-4">
                <li>Attempting to bypass security measures or reverse engineer the authentication protocols.</li>
                <li>Using the Service for any illegal purpose or in violation of any local, state, or international laws.</li>
                <li>Automated scraping or mass-collection of user data.</li>
                <li>Interfering with the proper working of the Service.</li>
              </ul>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-slate-800 border-b border-slate-100 pb-2">4. Privacy and Data Protection</h2>
              <p className="text-slate-600 leading-relaxed">
                Your privacy is important to us. Our use of your personal information is governed by our Privacy Policy. By using the Service, you consent to the collection and use of information by the configured tigrbl_auth public identity surface.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-slate-800 border-b border-slate-100 pb-2">5. Limitation of Liability</h2>
              <p className="text-slate-600 leading-relaxed">
                tigrbl_auth Auth is provided "as is" without any warranties. In no event shall tigrbl_auth Auth, its affiliates, or its partners be liable for any indirect, incidental, special, or consequential damages arising out of or in connection with the use of the Service.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-slate-800 border-b border-slate-100 pb-2">6. Governing Law</h2>
              <p className="text-slate-600 leading-relaxed">
                These Terms shall be governed by and construed in accordance with the laws of the jurisdiction in which tigrbl_auth Auth operates, without regard to its conflict of law provisions.
              </p>
            </section>

            <div className="pt-8 flex flex-col sm:flex-row gap-4 justify-between items-center">
              <button
                onClick={() => window.history.back()}
                className="text-slate-500 font-semibold hover:text-indigo-600 transition-colors flex items-center gap-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
                Go Back
              </button>
              <button
                onClick={() => window.location.hash = '#/register'}
                className="bg-indigo-600 text-white px-8 py-3 rounded-xl font-bold shadow-lg hover:bg-indigo-700 transition-all"
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
