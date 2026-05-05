
import React from 'react';
import { usePlatform } from '../hooks/usePlatform';

interface LayoutProps {
  children: React.ReactNode;
  user?: any;
  onLogout?: () => void;
}

export const Layout: React.FC<LayoutProps> = ({ children, user, onLogout }) => {
  const platform = usePlatform();

  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-white border-b border-slate-200 py-4 px-6 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div
            className="text-2xl font-bold text-slate-900 cursor-pointer flex items-center gap-2 group"
            onClick={() => window.location.hash = '/'}
          >
            <div className="w-8 h-8 bg-brand rounded-lg flex items-center justify-center text-white transition-transform group-hover:scale-105">
              {platform.logoLetter}
            </div>
            <span className="group-hover:text-brand transition-colors">{platform.name}</span>
          </div>
          <nav>
            {user ? (
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                  <img src={user.picture} className="w-8 h-8 rounded-full border border-slate-200" alt="Profile" />
                  <span className="hidden sm:inline text-sm font-medium text-slate-700">{user.name}</span>
                </div>
                <button
                  onClick={onLogout}
                  className="text-sm font-semibold text-slate-500 hover:text-brand transition-colors"
                >
                  Sign Out
                </button>
              </div>
            ) : (
              <div className="flex gap-4">
                <button
                  onClick={() => window.location.hash = '/login'}
                  className="text-sm font-semibold text-slate-600 hover:text-brand transition-colors"
                >
                  Sign In
                </button>
                <button
                  onClick={() => window.location.hash = '/register'}
                  className="text-sm font-semibold bg-brand text-white px-4 py-2 rounded-lg hover:opacity-90 transition-all shadow-sm"
                >
                  Join {platform.name}
                </button>
              </div>
            )}
          </nav>
        </div>
      </header>
      <main className="flex-grow flex flex-col">
        {children}
      </main>
      <footer className="bg-white border-t border-slate-100 py-6 px-6">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row justify-between items-center gap-4">
          <div className="text-slate-400 text-sm">
            &copy; {new Date().getFullYear()} {platform.name} {platform.footerText}
          </div>
          <div className="flex gap-6">
            <button
              onClick={() => window.location.hash = '/terms'}
              className="text-xs font-bold text-slate-400 hover:text-brand transition-colors"
            >
              Terms of Service
            </button>
            <button
              className="text-xs font-bold text-slate-400 hover:text-brand transition-colors"
            >
              Privacy Policy
            </button>
            <button
              className="text-xs font-bold text-slate-400 hover:text-brand transition-colors"
            >
              Contact Support
            </button>
          </div>
        </div>
      </footer>
    </div>
  );
};
