import React, { useState, useEffect } from "react";
import { 
  Key, 
  Shield, 
  Lock, 
  Smartphone, 
  RefreshCw, 
  AlertTriangle, 
  FileCode, 
  Terminal, 
  CheckCircle2, 
  XCircle, 
  User, 
  Settings, 
  Globe, 
  Eye, 
  EyeOff, 
  Copy, 
  Check, 
  AlertCircle,
  HelpCircle,
  ChevronRight,
  Database
} from "lucide-react";
import { AuthenticatorEnum, DisplayCategory, CeremonyState } from "../types";

// Spacing & Design Tokens implemented via Tailwind utility classes:
// Primary deep green: bg-emerald-600, text-emerald-800, hover:bg-emerald-700
// Soft green tint: bg-emerald-50, border-emerald-200
// Text: text-slate-700, text-slate-900
// Radius: rounded-lg (8px), rounded-md (6px)
// Spacing scale: p-4 (16px), p-3 (12px), p-2 (8px), gap-2

export const AuthenticatorKindIcon: React.FC<{ type: AuthenticatorEnum; className?: string }> = ({ type, className = "w-5 h-5" }) => {
  switch (type) {
    case AuthenticatorEnum.PASSWORD_LOCAL:
      return <Lock className={`${className} text-slate-500`} />;
    case AuthenticatorEnum.OTP_LOCAL:
      return <Smartphone className={`${className} text-blue-500`} />;
    case AuthenticatorEnum.WEBAUTHN_LOCAL:
      return <Shield className={`${className} text-emerald-600`} />;
    case AuthenticatorEnum.FEDERATED_OIDC:
      return <Globe className={`${className} text-indigo-500`} />;
    case AuthenticatorEnum.RECOVERY_CODE_LOCAL:
      return <FileCode className={`${className} text-amber-500`} />;
    case AuthenticatorEnum.CLIENT_SECRET_LOCAL:
      return <Key className={`${className} text-slate-600`} />;
    case AuthenticatorEnum.API_KEY_LOCAL:
      return <Terminal className={`${className} text-purple-500`} />;
    case AuthenticatorEnum.SERVICE_KEY_LOCAL:
      return <Database className={`${className} text-cyan-600`} />;
    case AuthenticatorEnum.MTLS_CLIENT_CERT:
      return <FileCode className={`${className} text-teal-600`} />;
    default:
      return <Key className={`${className} text-slate-500`} />;
  }
};

export const AuthenticatorStatusBadge: React.FC<{ status: string }> = ({ status }) => {
  let classes = "bg-slate-100 text-slate-700 border-slate-200";
  let label = status.replace("_", " ");

  if (status === "active") {
    classes = "bg-emerald-50 text-emerald-700 border-emerald-200";
  } else if (status === "suspended") {
    classes = "bg-amber-50 text-amber-700 border-amber-200";
  } else if (status === "revoked") {
    classes = "bg-red-50 text-red-700 border-red-200";
  } else if (status === "expired" || status === "replacement_required") {
    classes = "bg-rose-50 text-rose-700 border-rose-200 animate-pulse";
  } else if (status === "enrollment_pending") {
    classes = "bg-blue-50 text-blue-700 border-blue-200";
  }

  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border ${classes} capitalize font-sans`}>
      {label}
    </span>
  );
};

export const AuthenticatorRoleBadge: React.FC<{ category: DisplayCategory }> = ({ category }) => {
  let classes = "bg-slate-100 text-slate-700";
  if (category === DisplayCategory.HUMAN) {
    classes = "bg-sky-50 text-sky-800 border-sky-100";
  } else if (category === DisplayCategory.RECOVERY) {
    classes = "bg-amber-50 text-amber-800 border-amber-100";
  } else if (category === DisplayCategory.MACHINE) {
    classes = "bg-purple-50 text-purple-800 border-purple-100";
  } else if (category === DisplayCategory.SUPPORTING) {
    classes = "bg-indigo-50 text-indigo-800 border-indigo-100";
  }

  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium border ${classes} font-sans`}>
      {category}
    </span>
  );
};

export const AssurancePropertyBadge: React.FC<{ label: string; verified: boolean }> = ({ label, verified }) => {
  return (
    <span 
      className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-xs font-mono border ${
        verified 
          ? "bg-emerald-50 text-emerald-800 border-emerald-200" 
          : "bg-slate-50 text-slate-500 border-slate-200 opacity-60"
      }`}
    >
      {verified ? <Check className="w-3 h-3 text-emerald-600" /> : <span className="w-1.5 h-1.5 rounded-full bg-slate-300" />}
      {label}
    </span>
  );
};

export const ChallengeCountdown: React.FC<{ expiry: string; onExpire?: () => void }> = ({ expiry, onExpire }) => {
  const [secondsLeft, setSecondsLeft] = useState<number>(120);

  useEffect(() => {
    const calculateSeconds = () => {
      const diff = Math.floor((new Date(expiry).getTime() - Date.now()) / 1000);
      return diff > 0 ? diff : 0;
    };

    setSecondsLeft(calculateSeconds());

    const interval = setInterval(() => {
      const remaining = calculateSeconds();
      setSecondsLeft(remaining);
      if (remaining <= 0) {
        clearInterval(interval);
        if (onExpire) onExpire();
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [expiry, onExpire]);

  const minutes = Math.floor(secondsLeft / 60);
  const secs = secondsLeft % 60;
  const isUrgent = secondsLeft < 30;

  return (
    <div 
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md border text-xs font-mono font-medium ${
        isUrgent 
          ? "bg-rose-50 text-rose-700 border-rose-200 animate-pulse" 
          : "bg-slate-50 text-slate-600 border-slate-200"
      }`}
      aria-live="polite"
    >
      <RefreshCw className={`w-3.5 h-3.5 ${secondsLeft > 0 ? "animate-spin" : ""}`} style={{ animationDuration: isUrgent ? "1s" : "3s" }} />
      <span>
        Expires in: {minutes.toString().padStart(2, "0")}:{secs.toString().padStart(2, "0")}
      </span>
    </div>
  );
};

export const OneTimeSecretReveal: React.FC<{ secret: string; label?: string }> = ({ secret, label = "Temporary Secret Key" }) => {
  const [revealed, setRevealed] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(secret);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-slate-50 border border-slate-200 rounded-lg p-4 font-sans">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-medium text-slate-800">{label}</span>
        <span className="text-xs text-amber-600 font-medium flex items-center gap-1">
          <AlertTriangle className="w-3.5 h-3.5" /> Shows only once!
        </span>
      </div>

      <div className="relative flex items-center bg-white border border-slate-200 rounded-md p-2.5 font-mono text-sm break-all">
        <span className={`w-full pr-16 ${revealed ? "text-slate-900" : "select-none blur-sm text-slate-300"}`}>
          {revealed ? secret : "••••••••••••••••••••••••••••••••"}
        </span>
        
        <div className="absolute right-1.5 flex items-center gap-1">
          <button
            onClick={() => setRevealed(!revealed)}
            className="p-1.5 hover:bg-slate-100 rounded-md text-slate-500 hover:text-slate-800 transition-colors"
            title={revealed ? "Hide Secret" : "Reveal Secret"}
            aria-label={revealed ? "Hide Secret" : "Reveal Secret"}
          >
            {revealed ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
          </button>
          
          <button
            onClick={handleCopy}
            className="p-1.5 hover:bg-slate-100 rounded-md text-slate-500 hover:text-slate-800 transition-colors"
            title="Copy to clipboard"
            aria-label="Copy secret to clipboard"
          >
            {copied ? <Check className="w-4 h-4 text-emerald-600" /> : <Copy className="w-4 h-4" />}
          </button>
        </div>
      </div>
      
      {copied && (
        <span className="text-xs text-emerald-700 font-medium mt-1.5 block" aria-live="polite">
          Copied successfully to clipboard! Do not share it.
        </span>
      )}
    </div>
  );
};

export const RecentAuthenticationGate: React.FC<{
  onVerifySuccess: () => void;
  title?: string;
  description?: string;
}> = ({ onVerifySuccess, title = "Verification Required", description = "For security reasons, you must confirm your credentials before modifying authenticators." }) => {
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await fetch("/api/ceremonies/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ purpose: "verification", type: AuthenticatorEnum.PASSWORD_LOCAL })
      });
      const data = await response.json();
      
      const verifyRes = await fetch(`/api/ceremonies/${data.ceremony.id}/finish`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ secret: password })
      });

      if (!verifyRes.ok) {
        const errData = await verifyRes.json();
        throw new Error(errData.error || "Incorrect credentials");
      }

      onVerifySuccess();
    } catch (err: any) {
      setError(err.message || "Failed to verify identity");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white border border-slate-200 rounded-lg p-5 shadow-sm max-w-md mx-auto">
      <div className="flex items-start gap-3 mb-4">
        <div className="bg-amber-50 text-amber-600 p-2.5 rounded-full border border-amber-100">
          <Shield className="w-5 h-5" />
        </div>
        <div>
          <h4 className="text-base font-semibold text-slate-900">{title}</h4>
          <p className="text-sm text-slate-500 mt-1">{description}</p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-3">
        <div>
          <label className="block text-xs font-medium text-slate-700 uppercase tracking-wider mb-1">Confirm Password</label>
          <input
            type="password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Type your account password"
            className="w-full px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 text-sm"
          />
          <p className="text-xs text-slate-400 mt-1">Hint: Try password "correct-password" or "password"</p>
        </div>

        {error && (
          <div className="flex items-center gap-2 p-2.5 bg-red-50 border border-red-100 rounded-md text-red-700 text-xs">
            <AlertCircle className="w-4 h-4 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-2 px-4 rounded-md transition-colors text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2 disabled:opacity-50"
        >
          {loading ? "Verifying..." : "Confirm Credentials"}
        </button>
      </form>
    </div>
  );
};

export const CompatibilityNotice: React.FC<{ browserSupported: boolean }> = ({ browserSupported }) => {
  return (
    <div className={`p-4 rounded-lg border flex gap-3 ${browserSupported ? "bg-emerald-50 border-emerald-100 text-emerald-800" : "bg-rose-50 border-rose-100 text-rose-800"}`}>
      <AlertCircle className={`w-5 h-5 flex-shrink-0 ${browserSupported ? "text-emerald-600" : "text-rose-600"}`} />
      <div>
        <p className="text-sm font-semibold">
          {browserSupported ? "WebAuthn Capabilities Verified" : "WebAuthn Not fully Supported"}
        </p>
        <p className="text-xs mt-1 leading-relaxed">
          {browserSupported 
            ? "Your browser supports phishing-resistant passkeys, secure biometric user verification, and roaming FIDO2 security keys." 
            : "Your current user agent indicates restricted hardware WebAuthn capabilities. Fallback OTP methods are advised."
          }
        </p>
      </div>
    </div>
  );
};

export const AuthenticatorCard: React.FC<{
  authenticator: any;
  onAction?: (action: string, id: string) => void;
  adminMode?: boolean;
}> = ({ authenticator, onAction, adminMode = false }) => {
  const isPasskey = authenticator.type === AuthenticatorEnum.WEBAUTHN_LOCAL;
  
  return (
    <div className="bg-white border border-slate-200 rounded-lg p-4 hover:shadow-md transition-shadow duration-200 flex flex-col justify-between">
      <div>
        <div className="flex items-start justify-between gap-2 mb-2">
          <div className="flex items-center gap-2">
            <AuthenticatorKindIcon type={authenticator.type} className="w-5 h-5" />
            <h4 className="text-sm font-semibold text-slate-800 line-clamp-1">{authenticator.name}</h4>
          </div>
          <AuthenticatorStatusBadge status={authenticator.status} />
        </div>

        <p className="text-xs text-slate-500 mb-3">
          Enrolled on {new Date(authenticator.created).toLocaleDateString()}
          {authenticator.lastUsed && ` • Last used ${new Date(authenticator.lastUsed).toLocaleDateString()}`}
        </p>

        {/* Technical metadata summary */}
        {authenticator.metadata && (
          <div className="bg-slate-50 rounded p-2.5 border border-slate-100 mb-3 font-mono text-[11px] text-slate-600 leading-normal space-y-0.5">
            {Object.entries(authenticator.metadata).map(([k, v]) => (
              v && typeof v !== "object" && (
                <div key={k} className="flex justify-between">
                  <span className="text-slate-400 capitalize">{k}:</span>
                  <span className="text-slate-700 font-medium truncate max-w-[150px]">{v.toString()}</span>
                </div>
              )
            ))}
          </div>
        )}

        {/* Assurance Properties Section */}
        {authenticator.properties && (
          <div className="flex flex-wrap gap-1.5 mt-2">
            <AssurancePropertyBadge label="Phishing-Resistant" verified={authenticator.properties.phishingResistant} />
            <AssurancePropertyBadge label="Hardware-Backed" verified={authenticator.properties.hardwareProtected} />
            <AssurancePropertyBadge label="User Present" verified={authenticator.properties.userPresent} />
            <AssurancePropertyBadge label="User Verified" verified={authenticator.properties.userVerified} />
          </div>
        )}
      </div>

      <div className="border-t border-slate-100 mt-4 pt-3 flex gap-2 justify-end">
        {onAction && (
          <>
            {adminMode ? (
              <>
                {authenticator.status === "active" && (
                  <button 
                    onClick={() => onAction("suspend", authenticator.id)}
                    className="text-xs font-semibold text-amber-700 hover:bg-amber-50 px-2.5 py-1 rounded border border-amber-200"
                  >
                    Suspend
                  </button>
                )}
                {authenticator.status === "suspended" && (
                  <button 
                    onClick={() => onAction("activate", authenticator.id)}
                    className="text-xs font-semibold text-emerald-700 hover:bg-emerald-50 px-2.5 py-1 rounded border border-emerald-200"
                  >
                    Activate
                  </button>
                )}
                <button 
                  onClick={() => onAction("revoke", authenticator.id)}
                  className="text-xs font-semibold text-red-600 hover:bg-red-50 px-2.5 py-1 rounded border border-red-200"
                >
                  Revoke
                </button>
              </>
            ) : (
              <>
                {authenticator.type === AuthenticatorEnum.RECOVERY_CODE_LOCAL ? (
                  <button 
                    onClick={() => onAction("rotate", authenticator.id)}
                    className="text-xs font-semibold text-slate-700 hover:bg-slate-50 px-2.5 py-1.5 rounded border border-slate-200"
                  >
                    Rotate Codes
                  </button>
                ) : (
                  <>
                    <button 
                      onClick={() => onAction("rename", authenticator.id)}
                      className="text-xs font-semibold text-slate-700 hover:bg-slate-50 px-2.5 py-1.5 rounded border border-slate-200"
                    >
                      Rename
                    </button>
                    <button 
                      onClick={() => onAction("delete", authenticator.id)}
                      className="text-xs font-semibold text-rose-600 hover:bg-rose-50 px-2.5 py-1.5 rounded border border-rose-200"
                    >
                      Remove
                    </button>
                  </>
                )}
              </>
            )}
          </>
        )}
      </div>
    </div>
  );
};
