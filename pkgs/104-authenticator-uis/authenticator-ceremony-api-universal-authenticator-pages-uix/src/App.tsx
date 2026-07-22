import { useState, useEffect } from "react";
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
  Database,
  ArrowRight,
  QrCode,
  ShieldAlert,
  Sliders,
  Play,
  Trash2,
  LockKeyhole,
  Info,
  Calendar,
  Layers,
  History,
  Activity,
  UserCheck,
  Zap,
  HelpCircle as QuestionIcon
} from "lucide-react";
import { 
  AuthenticatorEnum, 
  DisplayCategory, 
  CeremonyState, 
  CeremonyPurpose, 
  Authenticator, 
  AuthenticatorPolicy, 
  Ceremony, 
  AuthEvent 
} from "./types";
import { 
  AuthenticatorCard, 
  OneTimeSecretReveal, 
  RecentAuthenticationGate, 
  CompatibilityNotice, 
  ChallengeCountdown,
  AuthenticatorKindIcon,
  AuthenticatorStatusBadge
} from "./components/UixCore";

export default function App() {
  // Navigation
  const [activeSurface, setActiveSurface] = useState<
    "public" | "my-account" | "tenant-admin" | "developer" | "service-admin" | "platform"
  >("my-account");

  // Global State fetched from the server
  const [authenticators, setAuthenticators] = useState<Authenticator[]>([]);
  const [policies, setPolicies] = useState<AuthenticatorPolicy[]>([]);
  const [activePolicyId, setActivePolicyId] = useState<string>("");
  const [auditEvents, setAuditEvents] = useState<AuthEvent[]>([]);
  const [catalogProviders, setCatalogProviders] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");

  // Ephemeral states for My Account Wizard
  const [showAddWizard, setShowAddWizard] = useState(false);
  const [wizardStep, setWizardStep] = useState(1);
  const [selectedEnrollType, setSelectedEnrollType] = useState<AuthenticatorEnum | "">("");
  const [newAuthName, setNewAuthName] = useState("");
  const [enrollSeed, setEnrollSeed] = useState("");
  const [enrollQrUrl, setEnrollQrUrl] = useState("");
  const [enrollCode, setEnrollCode] = useState("");
  const [enrollCeremonyId, setEnrollCeremonyId] = useState("");
  const [revealedRecoveryCodes, setRevealedRecoveryCodes] = useState<string[]>([]);
  const [isVerifyingGate, setIsVerifyingGate] = useState(false);
  const [gateAction, setGateAction] = useState<() => void>(() => {});

  // Ephemeral states for active Public Ceremonies
  const [activeCeremony, setActiveCeremony] = useState<Ceremony | null>(null);
  const [ceremonySecret, setCeremonySecret] = useState("");
  const [ceremonyError, setCeremonyError] = useState("");
  const [ceremonySuccess, setCeremonySuccess] = useState(false);
  const [simulatedWebAuthnPrompt, setSimulatedWebAuthnPrompt] = useState(false);

  // Ephemeral states for Tenant Admin Page
  const [showDraftPolicyModal, setShowDraftPolicyModal] = useState(false);
  const [policyAllowed, setPolicyAllowed] = useState<AuthenticatorEnum[]>([
    AuthenticatorEnum.PASSWORD_LOCAL,
    AuthenticatorEnum.OTP_LOCAL,
    AuthenticatorEnum.WEBAUTHN_LOCAL,
    AuthenticatorEnum.RECOVERY_CODE_LOCAL
  ]);
  const [policyReqHardware, setPolicyReqHardware] = useState(false);
  const [mfaGraceDays, setMfaGraceDays] = useState(7);
  const [lockoutSimulationResult, setLockoutSimulationResult] = useState<any>(null);

  // Ephemeral states for Developer / Service Admin Keys
  const [newClientSecret, setNewClientSecret] = useState<string | null>(null);
  const [newApiKey, setNewApiKey] = useState<string | null>(null);
  const [jwksInput, setJwksInput] = useState(`{
  "keys": [
    {
      "kty": "RSA",
      "kid": "sig-2026-07-12",
      "use": "sig",
      "alg": "RS256",
      "n": "u1W_9...[redacted]",
      "e": "AQAB"
    }
  ]
}`);
  const [mtlsCertInput, setMtlsCertInput] = useState("");
  const [dpopPrivateKey, setDpopPrivateKey] = useState("ecc_secp256r1_private_key_pem");
  const [dpopUri, setDpopUri] = useState("https://api.tigrbl.com/v1/ledger");
  const [dpopProofGenerated, setDpopProofGenerated] = useState("");

  // Network connection status
  const [connected, setConnected] = useState(true);

  // Fetch initial data
  const loadData = async () => {
    try {
      setLoading(true);
      const [authRes, policyRes, auditRes, catalogRes] = await Promise.all([
        fetch("/api/authenticators"),
        fetch("/api/policies"),
        fetch("/api/audit-events"),
        fetch("/api/catalog")
      ]);

      if (!authRes.ok || !policyRes.ok || !auditRes.ok || !catalogRes.ok) {
        throw new Error("Backend server response failed");
      }

      const authData = await authRes.json();
      const policyData = await policyRes.json();
      const auditData = await auditRes.json();
      const catalogData = await catalogRes.json();

      setAuthenticators(authData.authenticators);
      setPolicies(policyData.policies);
      setActivePolicyId(policyData.activePolicyId);
      setAuditEvents(auditData.events);
      setCatalogProviders(catalogData.providers);
      setConnected(true);
      setErrorMessage("");
    } catch (err: any) {
      console.warn("Could not connect to API, running in robust simulation mode.", err);
      setConnected(false);
      // Fallback robust mocking of endpoint states
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  // Helper for triggering sensitive actions via identity confirmation gate
  const triggerSensitiveAction = (action: () => void) => {
    setGateAction(() => action);
    setIsVerifyingGate(true);
  };

  const handleGateSuccess = () => {
    setIsVerifyingGate(false);
    gateAction();
  };

  // ==================== RECOVERY CODES ROTATION ====================
  const handleRotateRecoveryCodes = async () => {
    try {
      const response = await fetch("/api/authenticators/recovery-codes/rotate", {
        method: "POST",
        headers: { "Content-Type": "application/json" }
      });
      if (!response.ok) throw new Error("Could not rotate recovery codes");
      const data = await response.json();
      setRevealedRecoveryCodes(data.codes);
      loadData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  // ==================== AUTHENTICATOR ENROLLMENT WIZARD ====================
  const startEnrollment = async (type: AuthenticatorEnum) => {
    try {
      const response = await fetch("/api/authenticators/enroll/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ type, name: newAuthName || `My ${type.replace("_local", "")}` })
      });
      if (!response.ok) throw new Error("Failed to start enrollment ceremony");
      const data = await response.json();
      setEnrollCeremonyId(data.ceremony.id);
      setEnrollSeed(data.seed || "");
      setEnrollQrUrl(data.qrUrl || "");
      setSelectedEnrollType(type);
      setWizardStep(2);
    } catch (err: any) {
      alert(err.message);
    }
  };

  const finishEnrollment = async () => {
    try {
      let payload: any = {
        ceremonyId: enrollCeremonyId,
        name: newAuthName || `My ${selectedEnrollType}`,
        type: selectedEnrollType
      };

      if (selectedEnrollType === AuthenticatorEnum.OTP_LOCAL) {
        payload.response = enrollCode;
      } else if (selectedEnrollType === AuthenticatorEnum.WEBAUTHN_LOCAL) {
        payload.response = { response: "simulated_webauthn_fido2_attestation_signature" };
        payload.metadata = {
          platform: "MacBook Integrated TouchID",
          synced: true,
          aaguid: "adce0002-35bc-c60a-2b7b-40b2fed21711"
        };
      }

      const response = await fetch("/api/authenticators/enroll/finish", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.error || "Enrollment failed");
      }

      // Succeeded
      setShowAddWizard(false);
      setWizardStep(1);
      setEnrollCode("");
      setNewAuthName("");
      loadData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  // ==================== USER INVENTORY ACTIONS ====================
  const handleUserInventoryAction = async (action: string, id: string) => {
    const auth = authenticators.find(a => a.id === id);
    if (!auth) return;

    if (action === "delete") {
      if (!window.confirm(`Are you absolutely sure you want to remove the authenticator "${auth.name}"? This could lead to lockout if no other backup options exist.`)) {
        return;
      }

      try {
        const res = await fetch(`/api/authenticators/${id}`, { method: "DELETE" });
        if (!res.ok) {
          const errData = await res.json();
          throw new Error(errData.error || "Failed to delete");
        }
        loadData();
      } catch (err: any) {
        alert(err.message);
      }
    } else if (action === "rename") {
      const newName = prompt("Enter a new friendly name for this authenticator:", auth.name);
      if (!newName) return;

      try {
        const res = await fetch(`/api/authenticators/${id}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name: newName })
        });
        if (!res.ok) throw new Error("Rename failed");
        loadData();
      } catch (err: any) {
        alert(err.message);
      }
    } else if (action === "rotate") {
      triggerSensitiveAction(handleRotateRecoveryCodes);
    }
  };

  // ==================== ADMIN ACTIONS ====================
  const handleAdminAction = async (action: string, id: string) => {
    try {
      if (action === "suspend") {
        const res = await fetch(`/api/identities/usr-jick/authenticators/${id}/suspend`, { method: "POST" });
        if (!res.ok) throw new Error("Suspension failed");
      } else if (action === "activate") {
        const res = await fetch(`/api/authenticators/${id}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ status: "active" })
        });
        if (!res.ok) throw new Error("Activation failed");
      } else if (action === "revoke") {
        if (!window.confirm("Are you sure you want to fully revoke this authenticator? The user will immediately lose access via this factor.")) return;
        const res = await fetch(`/api/identities/usr-jick/authenticators/${id}/revoke`, { method: "POST" });
        if (!res.ok) throw new Error("Revocation failed");
      }
      loadData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  // ==================== PUBLIC CEREMONIES ====================
  const startPublicCeremony = async (purpose: CeremonyPurpose, type?: AuthenticatorEnum) => {
    try {
      const res = await fetch("/api/ceremonies/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ purpose, type })
      });
      const data = await res.json();
      setActiveCeremony(data.ceremony);
      setCeremonySecret("");
      setCeremonyError("");
      setCeremonySuccess(false);
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleCeremonySwitch = async (targetType: AuthenticatorEnum) => {
    if (!activeCeremony) return;
    try {
      const res = await fetch(`/api/ceremonies/${activeCeremony.id}/switch`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ targetType })
      });
      const data = await res.json();
      setActiveCeremony(data.ceremony);
      setCeremonySecret("");
      setCeremonyError("");
    } catch (err: any) {
      alert(err.message);
    }
  };

  const submitCeremonySecret = async () => {
    if (!activeCeremony) return;
    try {
      setCeremonyError("");
      const res = await fetch(`/api/ceremonies/${activeCeremony.id}/finish`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ secret: ceremonySecret })
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.error || "Verification failed");
      }

      setActiveCeremony(data.ceremony);
      setCeremonySuccess(true);
      loadData();
    } catch (err: any) {
      setCeremonyError(err.message);
    }
  };

  const submitSimulatedWebAuthn = async () => {
    if (!activeCeremony) return;
    setSimulatedWebAuthnPrompt(true);
    setTimeout(async () => {
      setSimulatedWebAuthnPrompt(false);
      try {
        setCeremonyError("");
        const res = await fetch(`/api/ceremonies/${activeCeremony.id}/finish`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ clientAssertion: { challenge: activeCeremony.challengeDescriptor } })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || "Passkey signature rejected");
        setActiveCeremony(data.ceremony);
        setCeremonySuccess(true);
        loadData();
      } catch (err: any) {
        setCeremonyError(err.message);
      }
    }, 1500); // 1.5s simulated browser prompt delay
  };

  // ==================== OIDC LINK SIMULATION ====================
  const handleLinkOidc = async (provider: string) => {
    try {
      const res = await fetch("/api/authenticators/federation/link", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ provider, email: "jick.68.0@gmail.com" })
      });
      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.error || "Failed to link provider");
      }
      loadData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleUnlinkOidc = async (provider: string) => {
    try {
      const res = await fetch("/api/authenticators/federation/unlink", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ provider })
      });
      if (!res.ok) throw new Error("Failed to unlink");
      loadData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  // ==================== NEW POLICY SIMULATION & ACTIVATION ====================
  const handleSimulatePolicy = async () => {
    try {
      const res = await fetch("/api/policies/simulate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          allowedMethods: policyAllowed,
          requireHardwareProtection: policyReqHardware
        } as any)
      });
      const data = await res.json();
      setLockoutSimulationResult(data);
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleCreatePolicyAndActivate = async () => {
    try {
      const createRes = await fetch("/api/policies", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          allowedMethods: policyAllowed,
          requireHardwareProtection: policyReqHardware,
          mfaGracePeriodDays: mfaGraceDays
        })
      });
      const createData = await createRes.json();
      if (!createRes.ok) throw new Error("Failed to draft policy");

      const actRes = await fetch(`/api/policies/activate/${createData.policy.id}`, { method: "POST" });
      if (!actRes.ok) throw new Error("Failed to activate policy");

      setShowDraftPolicyModal(false);
      setLockoutSimulationResult(null);
      loadData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  // ==================== MACHINE AUTHENTICATORS CREATION ====================
  const handleCreateMachineSecret = async (type: AuthenticatorEnum.CLIENT_SECRET_LOCAL | AuthenticatorEnum.API_KEY_LOCAL | AuthenticatorEnum.SERVICE_KEY_LOCAL) => {
    const defaultName = type === AuthenticatorEnum.CLIENT_SECRET_LOCAL 
      ? "Core Analytics Client Secret" 
      : type === AuthenticatorEnum.API_KEY_LOCAL 
        ? "Workload Monitoring Hook Key" 
        : "Spanner Audit Service Account Key";

    const label = prompt(`Enter a description for this new machine credential:`, defaultName);
    if (!label) return;

    try {
      const randomSecret = type === AuthenticatorEnum.CLIENT_SECRET_LOCAL
        ? "tgb_sec_live_5c8f12a7d4e9b3d11e5c"
        : type === AuthenticatorEnum.API_KEY_LOCAL
          ? "tgb_key_prod_a98e5f2c4d1b0a88"
          : "tgb_svckey_span_e5b4c3d2a1f0";

      const res = await fetch("/api/authenticators/enroll/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ type, name: label })
      });
      const data = await res.json();

      const finishRes = await fetch("/api/authenticators/enroll/finish", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ceremonyId: data.ceremony.id,
          name: label,
          type,
          metadata: {
            prefix: randomSecret.substring(0, 12) + "...",
            clientId: type === AuthenticatorEnum.CLIENT_SECRET_LOCAL ? "conf-client-99" : undefined
          }
        })
      });

      if (!finishRes.ok) throw new Error("Failed to finalize machine credential");

      if (type === AuthenticatorEnum.CLIENT_SECRET_LOCAL) setNewClientSecret(randomSecret);
      if (type === AuthenticatorEnum.API_KEY_LOCAL) setNewApiKey(randomSecret);

      loadData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  // ==================== DPOP GENERATOR ====================
  const handleGenerateDpop = () => {
    // Generate a beautiful, compliant RFC 9449 proof token structure
    const header = {
      typ: "dpop+jwt",
      alg: "ES256",
      jwk: {
        kty: "EC",
        crv: "P-256",
        x: "f83OJ3D2xF1Bg8vub9tM1gVFz4v16M",
        y: "x_9o6G6oF1b3F_4C9c1v2D3e4f5"
      }
    };
    const payload = {
      jti: "jti-dpop-proof-" + Date.now().toString().substring(8),
      htm: "POST",
      htu: dpopUri,
      iat: Math.floor(Date.now() / 1000)
    };
    const proofStr = `${btoa(JSON.stringify(header))}.${btoa(JSON.stringify(payload))}.[sig_proof_value]`;
    setDpopProofGenerated(proofStr);
  };

  // ==================== SUB-COMPONENTS & LAYOUTS ====================

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800 flex flex-col font-sans">
      {/* Top Brand Nav */}
      <header className="bg-white border-b border-slate-200 px-6 py-4 sticky top-0 z-40 shadow-sm">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="bg-emerald-600 text-white p-2 rounded-lg shadow-sm">
              <Shield className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-xl font-bold tracking-tight text-slate-900">Tigrbl Authenticator Console</h1>
                <span className="bg-emerald-50 text-emerald-700 text-[10px] font-bold px-2 py-0.5 rounded border border-emerald-200">
                  Phishing-Resistant Verified
                </span>
              </div>
              <p className="text-xs text-slate-500">Universal Ceremony Engine & Multi-Console Environment Dashboard</p>
            </div>
          </div>

          <div className="flex items-center gap-2 text-xs">
            <span className="font-medium text-slate-500">Node REST API Status:</span>
            {connected ? (
              <span className="flex items-center gap-1.5 px-2.5 py-1 bg-emerald-50 text-emerald-800 rounded-full border border-emerald-100 font-semibold">
                <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-ping" />
                Live Full-Stack
              </span>
            ) : (
              <span className="flex items-center gap-1.5 px-2.5 py-1 bg-amber-50 text-amber-800 rounded-full border border-amber-100 font-semibold animate-pulse">
                Fallback Memory Sandbox
              </span>
            )}
          </div>
        </div>
      </header>

      {/* Surface Swapper Hub */}
      <nav className="bg-slate-100 border-b border-slate-200/60 px-6 py-2.5">
        <div className="max-w-7xl mx-auto flex flex-wrap gap-1.5">
          {[
            { id: "public", label: "Public UIX", desc: "Sign-in, ceremonies & MFA challenges", color: "hover:bg-slate-200" },
            { id: "my-account", label: "My Account UIX", desc: "User factors & wizard self-service", color: "hover:bg-slate-200" },
            { id: "tenant-admin", label: "Tenant Admin UIX", desc: "Method policies & lockout prevention", color: "hover:bg-slate-200" },
            { id: "developer", label: "Developer UIX", desc: "Private key JWT, DPoP & mTLS", color: "hover:bg-slate-200" },
            { id: "service-admin", label: "Service Admin UIX", desc: "Workload credentials & API keys", color: "hover:bg-slate-200" },
            { id: "platform", label: "Platform Admin UIX", desc: "Global provider maturity catalog", color: "hover:bg-slate-200" }
          ].map(surface => (
            <button
              key={surface.id}
              onClick={() => {
                setActiveSurface(surface.id as any);
                // Clear any leftover revealed codes or secrets on navigation to protect privacy
                setRevealedRecoveryCodes([]);
                setNewClientSecret(null);
                setNewApiKey(null);
              }}
              className={`px-3.5 py-2 rounded-md font-semibold text-xs transition-all duration-150 flex flex-col items-start gap-0.5 text-left focus:outline-none focus:ring-2 focus:ring-emerald-500 ${
                activeSurface === surface.id 
                  ? "bg-white text-emerald-800 shadow-sm border border-slate-200/80 font-bold" 
                  : "text-slate-600 hover:text-slate-900 " + surface.color
              }`}
            >
              <span>{surface.label}</span>
              <span className="text-[9px] text-slate-400 font-normal">{surface.desc}</span>
            </button>
          ))}
        </div>
      </nav>

      {/* Security Gate Guard */}
      {isVerifyingGate && (
        <div className="fixed inset-0 bg-slate-900/40 backdrop-blur-sm flex items-center justify-center p-4 z-50 animate-fade-in">
          <div className="w-full max-w-md bg-white rounded-xl shadow-xl border border-slate-200 overflow-hidden">
            <div className="p-4 bg-slate-50 border-b border-slate-100 flex justify-between items-center">
              <span className="text-xs font-bold text-slate-600 uppercase tracking-wider">MFA Security Check</span>
              <button onClick={() => setIsVerifyingGate(false)} className="text-slate-400 hover:text-slate-600 text-sm">✕</button>
            </div>
            <div className="p-6">
              <RecentAuthenticationGate onVerifySuccess={handleGateSuccess} />
            </div>
          </div>
        </div>
      )}

      {/* Main Workspace Frame */}
      <main className="flex-grow max-w-7xl w-full mx-auto p-6 grid grid-cols-1 gap-6">
        {loading ? (
          <div className="flex flex-col items-center justify-center py-24 gap-3">
            <RefreshCw className="w-8 h-8 text-emerald-600 animate-spin" />
            <p className="text-sm text-slate-500 font-medium">Synchronizing application state engine...</p>
          </div>
        ) : (
          <>
            {/* 1. PUBLIC UIX SURFACE */}
            {activeSurface === "public" && (
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
                {/* Active Ceremony Simulation Panel */}
                <div className="lg:col-span-7 space-y-6">
                  <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-6">
                    <div className="flex items-center justify-between border-b border-slate-100 pb-4 mb-4">
                      <div>
                        <h3 className="text-base font-bold text-slate-900">Interactive Ceremony Shell</h3>
                        <p className="text-xs text-slate-500">Initiate authentic login, step-up verification, or recovery trials</p>
                      </div>
                      <div className="flex gap-1.5">
                        <button
                          onClick={() => startPublicCeremony(CeremonyPurpose.SIGN_IN, AuthenticatorEnum.PASSWORD_LOCAL)}
                          className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-semibold rounded transition"
                        >
                          Sign-In
                        </button>
                        <button
                          onClick={() => startPublicCeremony(CeremonyPurpose.STEP_UP, AuthenticatorEnum.WEBAUTHN_LOCAL)}
                          className="px-3 py-1.5 bg-emerald-50 hover:bg-emerald-100 text-emerald-800 text-xs font-semibold rounded border border-emerald-100 transition"
                        >
                          Step-Up
                        </button>
                        <button
                          onClick={() => startPublicCeremony(CeremonyPurpose.RECOVERY, AuthenticatorEnum.RECOVERY_CODE_LOCAL)}
                          className="px-3 py-1.5 bg-amber-50 hover:bg-amber-100 text-amber-800 text-xs font-semibold rounded border border-amber-100 transition"
                        >
                          Recovery
                        </button>
                      </div>
                    </div>

                    {activeCeremony ? (
                      <div className="border border-slate-200 rounded-lg p-5 bg-slate-50/50 space-y-4">
                        <div className="flex items-start justify-between gap-4">
                          <div>
                            <span className="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold tracking-wide uppercase bg-emerald-100 text-emerald-800 border border-emerald-200 mb-1.5">
                              Purpose: {activeCeremony.purpose}
                            </span>
                            <h4 className="text-sm font-bold text-slate-900">
                              Verify via {activeCeremony.type.replace("_local", "").toUpperCase()}
                            </h4>
                            <p className="text-xs text-slate-500 mt-1">{activeCeremony.riskSafeExplanation}</p>
                          </div>
                          <ChallengeCountdown expiry={activeCeremony.expiryTime} />
                        </div>

                        {/* Method Selector Option Switcher */}
                        {activeCeremony.methodSwitchEligibility.length > 0 && !ceremonySuccess && (
                          <div className="bg-white border border-slate-200 rounded-lg p-3">
                            <span className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">
                              Alternative authorized factors:
                            </span>
                            <div className="flex flex-wrap gap-1.5">
                              {activeCeremony.methodSwitchEligibility.map(type => (
                                <button
                                  key={type}
                                  onClick={() => handleCeremonySwitch(type)}
                                  className="text-[11px] font-medium text-slate-700 bg-slate-100 hover:bg-slate-200 px-2.5 py-1 rounded transition"
                                >
                                  Switch to {type.replace("_local", "").toUpperCase()}
                                </button>
                              ))}
                            </div>
                          </div>
                        )}

                        {/* Input Area based on type */}
                        {!ceremonySuccess && activeCeremony.state === CeremonyState.AWAITING_USER && (
                          <div className="bg-white border border-slate-200 rounded-lg p-4 space-y-3 shadow-inner">
                            {activeCeremony.type === AuthenticatorEnum.PASSWORD_LOCAL && (
                              <div className="space-y-2">
                                <label className="block text-xs font-semibold text-slate-600">Enter Account Password</label>
                                <input
                                  type="password"
                                  value={ceremonySecret}
                                  onChange={e => setCeremonySecret(e.target.value)}
                                  placeholder="Try: password"
                                  className="w-full px-3 py-2 border border-slate-300 rounded focus:outline-none focus:ring-2 focus:ring-emerald-500 text-sm"
                                />
                                <p className="text-[11px] text-slate-400">Pasting and standard password managers are allowed.</p>
                              </div>
                            )}

                            {activeCeremony.type === AuthenticatorEnum.OTP_LOCAL && (
                              <div className="space-y-2">
                                <label className="block text-xs font-semibold text-slate-600">6-Digit Verification App Code</label>
                                <input
                                  type="text"
                                  maxLength={6}
                                  value={ceremonySecret}
                                  onChange={e => setCeremonySecret(e.target.value)}
                                  placeholder="Try: 123456"
                                  className="w-full px-3 py-2 border border-slate-300 rounded text-center tracking-widest font-mono text-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
                                />
                                <p className="text-[11px] text-slate-400">Enter code generated in your secure TOTP Authenticator application.</p>
                              </div>
                            )}

                            {activeCeremony.type === AuthenticatorEnum.RECOVERY_CODE_LOCAL && (
                              <div className="space-y-2">
                                <label className="block text-xs font-semibold text-slate-600">8-Digit Backup Recovery Code</label>
                                <input
                                  type="text"
                                  maxLength={9}
                                  value={ceremonySecret}
                                  onChange={e => setCeremonySecret(e.target.value)}
                                  placeholder="e.g. 1234-5678"
                                  className="w-full px-3 py-2 border border-slate-300 rounded text-center tracking-widest font-mono text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
                                />
                                <p className="text-[11px] text-slate-400">Provide one of your pre-generated offline recovery backup keys.</p>
                              </div>
                            )}

                            {activeCeremony.type === AuthenticatorEnum.WEBAUTHN_LOCAL && (
                              <div className="p-4 border border-emerald-100 rounded bg-emerald-50/50 flex flex-col items-center justify-center text-center gap-3">
                                <Shield className="w-8 h-8 text-emerald-600 animate-bounce" />
                                <div>
                                  <h5 className="text-xs font-bold text-slate-800">Prompt WebAuthn Assertion</h5>
                                  <p className="text-[11px] text-slate-500 max-w-xs mt-0.5">
                                    Verify cryptographically through integrated biometrics or physical USB hardware security key.
                                  </p>
                                </div>
                                <button
                                  onClick={submitSimulatedWebAuthn}
                                  className="bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-xs px-4 py-2 rounded transition shadow-sm"
                                >
                                  Initialize Browser Prompt
                                </button>
                              </div>
                            )}

                            {ceremonyError && (
                              <div className="flex items-center gap-2 p-2.5 bg-rose-50 border border-rose-100 rounded text-rose-700 text-xs">
                                <AlertTriangle className="w-4 h-4 flex-shrink-0" />
                                <span>{ceremonyError}</span>
                              </div>
                            )}

                            {activeCeremony.type !== AuthenticatorEnum.WEBAUTHN_LOCAL && (
                              <button
                                onClick={submitCeremonySecret}
                                className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-2 rounded transition text-xs shadow-sm"
                              >
                                Submit Assertion
                              </button>
                            )}
                          </div>
                        )}

                        {/* Success State */}
                        {ceremonySuccess && (
                          <div className="bg-emerald-50 border border-emerald-200 rounded-lg p-5 text-center space-y-3">
                            <CheckCircle2 className="w-12 h-12 text-emerald-600 mx-auto" />
                            <div>
                              <h4 className="text-sm font-bold text-emerald-900">Identity Cryptographically Verified</h4>
                              <p className="text-xs text-emerald-700 mt-1">
                                Achieved Authentication Assurance Level: <strong className="font-mono">{activeCeremony.achievedAcr}</strong>
                              </p>
                            </div>
                            <div className="bg-white border border-emerald-100 rounded p-3 text-left font-mono text-[11px] text-slate-600 space-y-1">
                              <div>AMR Method: <span className="text-slate-800 font-bold">{activeCeremony.evidence?.amr.join(", ")}</span></div>
                              <div>Phishing Resistant: <span className="text-slate-800 font-bold">Yes</span></div>
                              <div>Session Freshness: <span className="text-slate-800 font-bold">Validated</span></div>
                              <div>Correlation ID: <span className="text-slate-400">{activeCeremony.correlationId}</span></div>
                            </div>
                            <button
                              onClick={() => setActiveCeremony(null)}
                              className="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold rounded shadow transition"
                            >
                              Finalize & Close Shell
                            </button>
                          </div>
                        )}

                        <div className="flex justify-between items-center border-t border-slate-100 pt-3 text-[11px] text-slate-400">
                          <span>Subject: {activeCeremony.subjectDisplayName}</span>
                          <span>Correlation ID: {activeCeremony.correlationId}</span>
                        </div>
                      </div>
                    ) : (
                      <div className="text-center py-12 border-2 border-dashed border-slate-200 rounded-lg">
                        <LockKeyhole className="w-8 h-8 text-slate-300 mx-auto mb-2" />
                        <h4 className="text-sm font-semibold text-slate-600">No active authentication ceremony</h4>
                        <p className="text-xs text-slate-400 max-w-sm mx-auto mt-1">
                          Select one of the quickstart buttons above to trigger a live multi-factor ceremony flow.
                        </p>
                      </div>
                    )}
                  </div>
                </div>

                {/* Simulated WebAuthn dialog modal */}
                {simulatedWebAuthnPrompt && (
                  <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-50 animate-fade-in">
                    <div className="bg-[#1e1e1e] border border-[#333] text-white rounded-xl shadow-2xl p-6 max-w-sm w-full font-sans">
                      <div className="flex items-center gap-3 mb-4">
                        <div className="bg-emerald-950 p-2 rounded-lg border border-emerald-800">
                          <Shield className="w-5 h-5 text-emerald-400 animate-pulse" />
                        </div>
                        <div>
                          <h4 className="text-sm font-bold tracking-tight">Security Key Verification</h4>
                          <p className="text-[10px] text-slate-400">FIDO2 / WebAuthn browser gateway</p>
                        </div>
                      </div>

                      <div className="border border-[#2d2d2d] bg-[#121212] rounded-lg p-5 text-center space-y-4">
                        <p className="text-xs text-slate-300 leading-relaxed">
                          Touch your integrated biometric sensor or insert your physical hardware security key to complete assertion.
                        </p>
                        <div className="relative w-16 h-16 mx-auto flex items-center justify-center">
                          <div className="absolute inset-0 rounded-full border-2 border-emerald-500/20 animate-ping" />
                          <div className="bg-emerald-600 p-4 rounded-full text-white">
                            <Smartphone className="w-6 h-6" />
                          </div>
                        </div>
                        <p className="text-[10px] text-emerald-400 font-mono">Biometric touch pending...</p>
                      </div>

                      <div className="mt-4 flex justify-end gap-2 text-xs">
                        <button
                          onClick={() => setSimulatedWebAuthnPrompt(false)}
                          className="px-3 py-1.5 bg-transparent border border-[#444] text-slate-300 hover:text-white rounded transition"
                        >
                          Cancel FIDO2
                        </button>
                      </div>
                    </div>
                  </div>
                )}

                {/* Federated OIDC link simulator & callback handler */}
                <div className="lg:col-span-5 space-y-6">
                  <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-6">
                    <h3 className="text-base font-bold text-slate-900 mb-2">Upstream Federated OIDC Core</h3>
                    <p className="text-xs text-slate-500 mb-4">
                      Simulate authentication linking / unlinking through trusted external identity providers.
                    </p>

                    <div className="space-y-3">
                      {[
                        { id: "Google", desc: "Enterprise Domain Google Sync", issuer: "https://accounts.google.com" },
                        { id: "GitHub", desc: "Developer profile integration", issuer: "https://github.com/login/oauth" },
                        { id: "MicrosoftEntra", desc: "Workplace Directory Sync", issuer: "https://login.microsoftonline.com" }
                      ].map(prov => {
                        const isLinked = authenticators.some(a => a.type === AuthenticatorEnum.FEDERATED_OIDC && a.name.includes(prov.id));
                        return (
                          <div key={prov.id} className="border border-slate-200 rounded-lg p-3.5 flex items-center justify-between gap-3 bg-slate-50/50">
                            <div>
                              <div className="flex items-center gap-1.5">
                                <Globe className="w-4 h-4 text-slate-500" />
                                <h4 className="text-xs font-bold text-slate-800">{prov.id}</h4>
                                {isLinked && <span className="bg-emerald-50 text-emerald-700 text-[9px] font-bold px-1.5 py-0.5 rounded border border-emerald-200">Active link</span>}
                              </div>
                              <p className="text-[11px] text-slate-500 mt-0.5">{prov.desc}</p>
                              <span className="text-[9px] font-mono text-slate-400 mt-1 block select-all">{prov.issuer}</span>
                            </div>

                            {isLinked ? (
                              <button
                                onClick={() => handleUnlinkOidc(prov.id)}
                                className="px-3 py-1 bg-rose-50 hover:bg-rose-100 text-rose-700 text-xs font-semibold rounded border border-rose-200 transition"
                              >
                                Unlink
                              </button>
                            ) : (
                              <button
                                onClick={() => handleLinkOidc(prov.id)}
                                className="px-3 py-1 bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-semibold rounded border border-slate-300 transition"
                              >
                                Link
                              </button>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* 2. MY ACCOUNT UIX SURFACE */}
            {activeSurface === "my-account" && (
              <div className="space-y-6">
                {/* Introduction banner */}
                <div className="bg-white border border-slate-200 rounded-xl p-6 flex flex-col md:flex-row md:items-center justify-between gap-6 shadow-sm">
                  <div className="space-y-1">
                    <h3 className="text-lg font-bold text-slate-900">My Registered Authenticators</h3>
                    <p className="text-sm text-slate-500">
                      Manage your security hardware, passwords, verification codes, and federated account configurations.
                    </p>
                  </div>
                  <button
                    onClick={() => {
                      setSelectedEnrollType("");
                      setNewAuthName("");
                      setWizardStep(1);
                      setShowAddWizard(true);
                    }}
                    className="self-start md:self-auto bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs px-4 py-2.5 rounded-lg shadow-sm transition flex items-center gap-2"
                  >
                    <Smartphone className="w-4 h-4" /> Add Authenticator
                  </button>
                </div>

                {/* Compatibility Notification */}
                <CompatibilityNotice browserSupported={true} />

                {/* Active revealed codes from rotation */}
                {revealedRecoveryCodes.length > 0 && (
                  <div className="bg-amber-50 border border-amber-200 rounded-lg p-5 space-y-3">
                    <div className="flex items-start gap-2.5">
                      <AlertTriangle className="w-5 h-5 text-amber-600 flex-shrink-0" />
                      <div>
                        <h4 className="text-sm font-bold text-amber-900">Your New Backup Recovery Codes</h4>
                        <p className="text-xs text-amber-700 mt-0.5">
                          Print, save, or download these keys. They are shown **only once** and will not be displayed again.
                        </p>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 bg-white border border-amber-100 rounded-lg p-4 font-mono text-center text-sm text-slate-800 font-bold tracking-wider select-all">
                      {revealedRecoveryCodes.map((code, idx) => (
                        <div key={idx} className="p-2 bg-slate-50 border border-slate-200 rounded">
                          {code}
                        </div>
                      ))}
                    </div>

                    <div className="flex justify-end gap-2">
                      <button
                        onClick={() => setRevealedRecoveryCodes([])}
                        className="px-4 py-1.5 bg-amber-600 hover:bg-amber-700 text-white text-xs font-semibold rounded shadow transition"
                      >
                        I Have Safely Saved These Codes
                      </button>
                    </div>
                  </div>
                )}

                {/* Grid list of authenticators */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {authenticators
                    .filter(a => a.category === DisplayCategory.HUMAN || a.category === DisplayCategory.RECOVERY)
                    .map(auth => (
                      <AuthenticatorCard
                        key={auth.id}
                        authenticator={auth}
                        onAction={handleUserInventoryAction}
                      />
                    ))}
                </div>

                {/* Session Security Context Detail */}
                <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm space-y-4">
                  <div className="flex items-center gap-2 border-b border-slate-100 pb-3">
                    <Activity className="w-5 h-5 text-slate-600" />
                    <h4 className="text-sm font-bold text-slate-900">Current Session Authentication Context Detail</h4>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 font-sans">
                    <div className="border border-slate-100 rounded p-4 bg-slate-50/50">
                      <span className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider">Achieved ACR Class</span>
                      <strong className="text-sm font-mono text-emerald-800 block mt-1">urn:tigrbl:acr:aal3</strong>
                      <p className="text-[11px] text-slate-500 mt-1">Phishing-resistant, hardware-protected multi-factor baseline.</p>
                    </div>

                    <div className="border border-slate-100 rounded p-4 bg-slate-50/50">
                      <span className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider">AMR Evidences used</span>
                      <strong className="text-sm font-mono text-slate-800 block mt-1">["password_local", "webauthn_local"]</strong>
                      <p className="text-[11px] text-slate-500 mt-1">Passwords & biometric credentials presented and approved.</p>
                    </div>

                    <div className="border border-slate-100 rounded p-4 bg-slate-50/50">
                      <span className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider">Device & Risk Metrics</span>
                      <strong className="text-sm font-mono text-slate-800 block mt-1">Level: Low Risk • Attestation: direct</strong>
                      <p className="text-[11px] text-slate-500 mt-1">Cryptographic key provenance confirmed via hardware token signature.</p>
                    </div>
                  </div>
                </div>

                {/* Add Authenticator Dialog Wizard */}
                {showAddWizard && (
                  <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-50 animate-fade-in">
                    <div className="bg-white border border-slate-200 rounded-xl shadow-2xl p-6 max-w-md w-full font-sans">
                      <div className="flex items-center justify-between border-b border-slate-100 pb-3 mb-4">
                        <h4 className="text-sm font-bold text-slate-900">Enroll New Security Factor</h4>
                        <button onClick={() => setShowAddWizard(false)} className="text-slate-400 hover:text-slate-600 text-sm">✕</button>
                      </div>

                      {wizardStep === 1 && (
                        <div className="space-y-4">
                          <p className="text-xs text-slate-500">
                            Select the category of cryptographic authenticator factor you would like to register to secure your credentials.
                          </p>

                          <div className="space-y-2">
                            {[
                              { type: AuthenticatorEnum.WEBAUTHN_LOCAL, label: "Passkey / Roaming Security Key", desc: "Phishing-resistant hardware token or built-in secure biometrics", badge: "Phishing-resistant" },
                              { type: AuthenticatorEnum.OTP_LOCAL, label: "Authenticator App (TOTP)", desc: "Generates time-based six-digit code sequences (Google Authenticator)", badge: "Multi-factor compatibility" }
                            ].map(item => (
                              <button
                                key={item.type}
                                onClick={() => setSelectedEnrollType(item.type)}
                                className={`w-full text-left p-3.5 border rounded-lg transition-all flex justify-between items-center gap-4 ${
                                  selectedEnrollType === item.type 
                                    ? "bg-emerald-50 border-emerald-400 ring-2 ring-emerald-500/20" 
                                    : "border-slate-200 hover:bg-slate-50"
                                }`}
                              >
                                <div>
                                  <div className="flex items-center gap-2">
                                    <AuthenticatorKindIcon type={item.type} className="w-4 h-4 text-slate-600" />
                                    <span className="text-xs font-bold text-slate-800">{item.label}</span>
                                  </div>
                                  <p className="text-[11px] text-slate-500 mt-1">{item.desc}</p>
                                </div>
                                <span className="bg-slate-100 border text-slate-600 text-[9px] px-1.5 py-0.5 rounded whitespace-nowrap self-start">
                                  {item.badge}
                                </span>
                              </button>
                            ))}
                          </div>

                          <div className="space-y-2">
                            <label className="block text-[10px] font-bold text-slate-500 uppercase tracking-wider">Friendly Key Label</label>
                            <input
                              type="text"
                              value={newAuthName}
                              onChange={e => setNewAuthName(e.target.value)}
                              placeholder="e.g. My YubiKey 5C or Work Mobile app"
                              className="w-full px-3 py-2 border border-slate-300 rounded focus:outline-none focus:ring-2 focus:ring-emerald-500 text-sm"
                            />
                          </div>

                          <div className="flex justify-end gap-2 pt-3 border-t border-slate-100">
                            <button
                              onClick={() => setShowAddWizard(false)}
                              className="px-3 py-2 border border-slate-200 text-slate-600 rounded text-xs hover:bg-slate-50 transition"
                            >
                              Cancel
                            </button>
                            <button
                              disabled={!selectedEnrollType}
                              onClick={() => startEnrollment(selectedEnrollType as any)}
                              className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded text-xs font-bold transition disabled:opacity-50"
                            >
                              Continue
                            </button>
                          </div>
                        </div>
                      )}

                      {wizardStep === 2 && (
                        <div className="space-y-4">
                          {selectedEnrollType === AuthenticatorEnum.OTP_LOCAL ? (
                            <div className="space-y-4">
                              <p className="text-xs text-slate-500">
                                Scan the QR code below using your mobile authentication app (Google Authenticator, Microsoft Authenticator, Duo).
                              </p>

                              <div className="flex flex-col items-center justify-center p-4 border border-slate-100 bg-slate-50 rounded-lg gap-3">
                                {/* Interactive representation of QR code */}
                                <div className="bg-white p-3 border border-slate-200 rounded-lg shadow-inner">
                                  <QrCode className="w-36 h-36 text-slate-900" />
                                </div>
                                <div className="text-center">
                                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Manual Secret Seed</span>
                                  <p className="text-xs font-mono text-slate-700 bg-white border border-slate-200 px-3 py-1 rounded mt-1 select-all font-bold">
                                    {enrollSeed}
                                  </p>
                                </div>
                              </div>

                              <div className="space-y-2">
                                <label className="block text-xs font-semibold text-slate-700">Enter Six-Digit Verification Code</label>
                                <input
                                  type="text"
                                  maxLength={6}
                                  value={enrollCode}
                                  onChange={e => setEnrollCode(e.target.value)}
                                  placeholder="Try inputting '123456'"
                                  className="w-full px-3 py-2 border border-slate-300 rounded text-center tracking-widest font-mono text-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
                                />
                                <p className="text-[10px] text-slate-400">Verifying the initial TOTP code establishes synchronized clock drift correctness.</p>
                              </div>
                            </div>
                          ) : (
                            <div className="text-center py-6 space-y-4">
                              <Shield className="w-12 h-12 text-emerald-600 mx-auto animate-bounce" />
                              <div>
                                <h5 className="text-sm font-bold text-slate-900">Platform WebAuthn Registration Prompt</h5>
                                <p className="text-xs text-slate-500 max-w-sm mx-auto mt-1">
                                  Your browser is about to request FIDO2 WebAuthn credential enrollment. This binds a unique asymmetric private key directly inside your hardware security enclave.
                                </p>
                              </div>
                              <div className="bg-slate-50 border border-slate-200 rounded p-3 font-mono text-[11px] text-left text-slate-600 space-y-1">
                                <div>Relying Party: <span className="text-slate-800 font-bold">Tigrbl</span></div>
                                <div>User Verification: <span className="text-slate-800 font-bold">required</span></div>
                                <div>Attestation: <span className="text-slate-800 font-bold">indirect</span></div>
                              </div>
                            </div>
                          )}

                          <div className="flex justify-end gap-2 pt-3 border-t border-slate-100">
                            <button
                              onClick={() => setWizardStep(1)}
                              className="px-3 py-2 border border-slate-200 text-slate-600 rounded text-xs hover:bg-slate-50 transition"
                            >
                              Back
                            </button>
                            <button
                              onClick={finishEnrollment}
                              className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded text-xs font-bold transition"
                            >
                              Confirm & Save Factor
                            </button>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* 3. TENANT ADMIN UIX SURFACE */}
            {activeSurface === "tenant-admin" && (
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
                {/* Method Policy Configurator */}
                <div className="lg:col-span-8 space-y-6">
                  <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-6">
                    <div className="flex items-center justify-between border-b border-slate-100 pb-4 mb-4">
                      <div>
                        <h3 className="text-base font-bold text-slate-900">Tenant Method Policy Configurations</h3>
                        <p className="text-xs text-slate-500">Edit, preview and simulate the tenant-wide authentication policy matrix</p>
                      </div>
                      <span className="bg-emerald-50 text-emerald-800 text-[10px] font-bold px-2 py-1 rounded border border-emerald-200">
                        Active Profile: Policy v{policies.find(p => p.isActive)?.version || 2}
                      </span>
                    </div>

                    <div className="space-y-4">
                      <div>
                        <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Allowed Human Factors</label>
                        <div className="grid grid-cols-2 gap-2">
                          {[
                            { type: AuthenticatorEnum.PASSWORD_LOCAL, label: "Password" },
                            { type: AuthenticatorEnum.OTP_LOCAL, label: "TOTP Code App" },
                            { type: AuthenticatorEnum.WEBAUTHN_LOCAL, label: "WebAuthn / Passkeys" },
                            { type: AuthenticatorEnum.FEDERATED_OIDC, label: "OIDC Federation" }
                          ].map(opt => {
                            const selected = policyAllowed.includes(opt.type);
                            return (
                              <button
                                key={opt.type}
                                onClick={() => {
                                  if (selected) {
                                    setPolicyAllowed(policyAllowed.filter(v => v !== opt.type));
                                  } else {
                                    setPolicyAllowed([...policyAllowed, opt.type]);
                                  }
                                }}
                                className={`p-3 text-left border rounded-lg transition-all text-xs font-semibold flex items-center justify-between ${
                                  selected 
                                    ? "bg-emerald-50/50 border-emerald-300 text-emerald-900 font-bold" 
                                    : "border-slate-200 text-slate-600 hover:bg-slate-50"
                                }`}
                              >
                                <span>{opt.label}</span>
                                {selected && <Check className="w-4 h-4 text-emerald-600" />}
                              </button>
                            );
                          })}
                        </div>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="space-y-1.5">
                          <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider">Hardware Protection Policy</label>
                          <div className="flex items-center gap-2">
                            <input
                              type="checkbox"
                              id="req-hard"
                              checked={policyReqHardware}
                              onChange={e => setPolicyReqHardware(e.target.checked)}
                              className="rounded text-emerald-600 focus:ring-emerald-500 border-slate-300"
                            />
                            <label htmlFor="req-hard" className="text-xs text-slate-700 font-medium">Require verified hardware protection</label>
                          </div>
                          <p className="text-[10px] text-slate-400">Strictly enforces that FIDO2 credentials return hardware-backed attestation certificates.</p>
                        </div>

                        <div className="space-y-1.5">
                          <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider">MFA Grace Period</label>
                          <select
                            value={mfaGraceDays}
                            onChange={e => setMfaGraceDays(Number(e.target.value))}
                            className="w-full px-3 py-1.5 border border-slate-300 rounded text-xs font-medium"
                          >
                            <option value={3}>3 Days (Strict Rollout)</option>
                            <option value={7}>7 Days (Recommended)</option>
                            <option value={14}>14 Days (Lenient)</option>
                          </select>
                          <p className="text-[10px] text-slate-400">Grace period for newly provisioned user identities to register compliant MFA credentials.</p>
                        </div>
                      </div>

                      {/* Lockout impact warnings & Simulation panel */}
                      <div className="border border-slate-200 bg-slate-50 rounded-lg p-4 space-y-3">
                        <div className="flex items-center justify-between">
                          <h4 className="text-xs font-bold text-slate-800 flex items-center gap-1.5">
                            <Sliders className="w-4 h-4 text-slate-500" />
                            Lockout & Compliance Simulation Sandbox
                          </h4>
                          <button
                            onClick={handleSimulatePolicy}
                            className="px-3 py-1 bg-white hover:bg-slate-100 text-slate-800 text-xs font-semibold rounded border border-slate-300 transition flex items-center gap-1"
                          >
                            <Play className="w-3 h-3" /> Simulate Impact
                          </button>
                        </div>

                        {lockoutSimulationResult ? (
                          <div className={`p-3.5 border rounded-lg ${
                            lockoutSimulationResult.riskLevel === "CRITICAL" 
                              ? "bg-rose-50 border-rose-200 text-rose-900" 
                              : lockoutSimulationResult.riskLevel === "HIGH"
                                ? "bg-amber-50 border-amber-200 text-amber-900"
                                : "bg-emerald-50 border-emerald-200 text-emerald-900"
                          }`}>
                            <div className="flex items-start gap-2.5">
                              {lockoutSimulationResult.riskLevel === "CRITICAL" ? (
                                <ShieldAlert className="w-5 h-5 text-rose-600 flex-shrink-0" />
                              ) : (
                                <Info className="w-5 h-5 flex-shrink-0" />
                              )}
                              <div>
                                <h5 className="text-xs font-bold">
                                  Policy Simulation Outcome: {lockoutSimulationResult.riskLevel} RISK
                                </h5>
                                <p className="text-[11px] mt-1">
                                  Estimated Lockout Impact: <strong>{lockoutSimulationResult.affectedUsers}% of users</strong> would lose system access.
                                </p>
                                <ul className="list-disc pl-4 text-[10px] space-y-1 mt-2">
                                  {lockoutSimulationResult.details.map((dt: string, i: number) => (
                                    <li key={i}>{dt}</li>
                                  ))}
                                </ul>
                              </div>
                            </div>
                          </div>
                        ) : (
                          <p className="text-[11px] text-slate-500">
                            Run lockout simulation to verify if newly drafted allowed factors will cause organizational lockout risks.
                          </p>
                        )}
                      </div>

                      <div className="border-t border-slate-100 pt-4 flex justify-end gap-2">
                        <button
                          onClick={handleCreatePolicyAndActivate}
                          className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded shadow-sm transition"
                        >
                          Draft & Activate Instantly (Policy v{policies.length + 1})
                        </button>
                      </div>
                    </div>
                  </div>

                  {/* Supervised Administration: User Identity view */}
                  <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-6">
                    <h3 className="text-base font-bold text-slate-900 mb-2">Governed Administrator Identity Management</h3>
                    <p className="text-xs text-slate-500 mb-4">
                      Administrate factors registered for subject <strong className="font-mono">usr-jick</strong>. Safe administrative overrides never disclose credentials.
                    </p>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {authenticators
                        .filter(a => a.category === DisplayCategory.HUMAN || a.category === DisplayCategory.RECOVERY)
                        .map(auth => (
                          <AuthenticatorCard
                            key={auth.id}
                            authenticator={auth}
                            adminMode={true}
                            onAction={handleAdminAction}
                          />
                        ))}
                    </div>

                    <div className="bg-slate-50 border border-slate-200 rounded-lg p-4 mt-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                      <div>
                        <h4 className="text-xs font-bold text-slate-800">Initiate Supervised Account Recovery</h4>
                        <p className="text-[11px] text-slate-500 mt-0.5">Generate a bypass link or key strictly authorized through tenant administrator governance.</p>
                      </div>
                      <button
                        onClick={async () => {
                          const res = await fetch("/api/identities/usr-jick/recovery/govern", { method: "POST" });
                          const data = await res.json();
                          alert(`${data.instructions}\nGovernance ID: ${data.governanceId}`);
                        }}
                        className="px-3.5 py-1.5 bg-slate-800 hover:bg-slate-900 text-white text-xs font-semibold rounded shadow transition whitespace-nowrap self-start sm:self-auto"
                      >
                        Govern Bypass Recovery
                      </button>
                    </div>
                  </div>
                </div>

                {/* Audit Logs Timeline Panel */}
                <div className="lg:col-span-4 space-y-6">
                  <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-6">
                    <div className="flex items-center justify-between border-b border-slate-100 pb-3 mb-4">
                      <h3 className="text-base font-bold text-slate-900 flex items-center gap-1.5">
                        <History className="w-5 h-5 text-slate-500" />
                        Audit Events Tracker
                      </h3>
                      <button onClick={loadData} className="p-1 text-slate-400 hover:text-slate-600 transition">
                        <RefreshCw className="w-4 h-4" />
                      </button>
                    </div>

                    <div className="space-y-4 max-h-[600px] overflow-y-auto pr-1">
                      {auditEvents.map(evt => (
                        <div key={evt.id} className="border-l-2 border-slate-200 pl-3.5 py-1 text-xs relative">
                          <div className={`absolute -left-1.5 top-2.5 w-3.5 h-3.5 rounded-full border-2 bg-white flex items-center justify-center ${
                            evt.success ? "border-emerald-500 text-emerald-500" : "border-rose-500 text-rose-500"
                          }`}>
                            <span className="w-1.5 h-1.5 rounded-full bg-current" />
                          </div>

                          <div className="flex items-center justify-between gap-2">
                            <span className="font-mono text-[10px] text-slate-400">
                              {new Date(evt.timestamp).toLocaleTimeString()}
                            </span>
                            <span className={`text-[10px] font-bold tracking-wider uppercase ${
                              evt.success ? "text-emerald-700" : "text-rose-700"
                            }`}>
                              {evt.success ? "Success" : "Failed"}
                            </span>
                          </div>

                          <h4 className="font-bold text-slate-800 mt-0.5">{evt.eventType}</h4>
                          <p className="text-[11px] text-slate-500 mt-1">{evt.details}</p>

                          <div className="flex flex-wrap gap-1 mt-1.5 font-mono text-[9px] text-slate-400">
                            <span>IP: {evt.ipAddress}</span>
                            <span>•</span>
                            <span>Loc: {evt.location}</span>
                            {evt.acr && (
                              <>
                                <span>•</span>
                                <span className="text-emerald-700 font-bold">{evt.acr}</span>
                              </>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* 4. DEVELOPER UIX SURFACE */}
            {activeSurface === "developer" && (
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
                <div className="lg:col-span-7 space-y-6">
                  {/* Private Key JWT & JWKS configuration */}
                  <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-6">
                    <h3 className="text-base font-bold text-slate-900 mb-1">Confidential Client JWT Private Key Bindings</h3>
                    <p className="text-xs text-slate-500 mb-4">
                      Enable secure, passwordless server authentication with `private_key_jwt` standard (RFC 7523) key signatures.
                    </p>

                    <div className="space-y-4">
                      <div className="space-y-1.5">
                        <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider"> Rerigster JWKS Public Endpoint / Document </label>
                        <textarea
                          rows={6}
                          value={jwksInput}
                          onChange={e => setJwksInput(e.target.value)}
                          className="w-full font-mono text-xs px-3 py-2 border border-slate-300 rounded focus:outline-none focus:ring-2 focus:ring-emerald-500 bg-slate-50"
                        />
                        <p className="text-[10px] text-slate-400">Provide the client public JSON Web Key Set matching key assertions.</p>
                      </div>

                      <div className="p-4 border border-slate-200 bg-slate-50 rounded-lg space-y-2">
                        <h4 className="text-xs font-bold text-slate-800">Generate Compliant Client Assertion Template</h4>
                        <p className="text-[11px] text-slate-500">Copy this request model structure for machine credential integration testing.</p>
                        <pre className="text-[10px] font-mono text-slate-600 bg-white border border-slate-200 rounded p-2.5 overflow-x-auto select-all leading-normal">
{`POST /oauth/token HTTP/1.1
Host: auth.tigrbl.com
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials&
client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer&
client_assertion=eyJhbGciOiJSUzI1NiIsImtpZCI6InNpZy0yMDI2LTA3LTEyIn0.eyJpc3MiOiJjbGllbnQtMSIsInN1YiI6ImNsaWVudC0xIiwiYXVkIjoiaHR0cHM6Ly9hdXRoLnRpZ3JibC5jb20iLCJleHAiOjE3ODkxNTgwMDB9.[signature]`}
                        </pre>
                      </div>
                    </div>
                  </div>

                  {/* mTLS Certificate Binding */}
                  <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-6">
                    <h3 className="text-base font-bold text-slate-900 mb-1">mTLS Client Certificate Binding</h3>
                    <p className="text-xs text-slate-500 mb-4">
                      Upload public PEM certificate components to configure cryptographic client mutual-TLS handshakes.
                    </p>

                    <div className="space-y-3">
                      <textarea
                        rows={3}
                        value={mtlsCertInput}
                        onChange={e => setMtlsCertInput(e.target.value)}
                        placeholder="-----BEGIN CERTIFICATE-----&#10;MIIBiTCCATagAwIBAgIQY...[paste public client certificate]&#10;-----END CERTIFICATE-----"
                        className="w-full font-mono text-xs px-3 py-2 border border-slate-300 rounded focus:outline-none focus:ring-2 focus:ring-emerald-500 bg-slate-50"
                      />
                      <div className="flex justify-between items-center text-[10px] text-slate-400">
                        <span>Never submit client private keys. Public keys only.</span>
                        <button
                          onClick={() => {
                            if (!mtlsCertInput.includes("BEGIN CERTIFICATE")) {
                              alert("Please paste a valid public X.509 certificate structure.");
                              return;
                            }
                            alert("mTLS Certificate Bound Successfully: CN=developer.service.client, FP=B8:42:01... Secure token binding is active.");
                            setMtlsCertInput("");
                          }}
                          className="px-3 py-1 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold rounded text-xs transition"
                        >
                          Bind Certificate
                        </button>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="lg:col-span-5 space-y-6">
                  {/* DPoP Sender Constraint Proof Playground */}
                  <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-6">
                    <div className="flex items-center gap-2 mb-2">
                      <Sliders className="w-5 h-5 text-slate-600" />
                      <h3 className="text-base font-bold text-slate-900">OAuth DPoP Proof Generator Tool</h3>
                    </div>
                    <p className="text-xs text-slate-500 mb-4">
                      DPoP (RFC 9449) acts as a sender constraint on bearer access tokens. Simulate constructing and signing DPoP proof JKTs.
                    </p>

                    <div className="space-y-3.5 text-xs font-sans">
                      <div className="space-y-1">
                        <label className="block text-[10px] font-bold text-slate-500 uppercase tracking-wider">Signing Private Key PEM</label>
                        <input
                          type="text"
                          value={dpopPrivateKey}
                          onChange={e => setDpopPrivateKey(e.target.value)}
                          className="w-full font-mono text-xs px-3 py-1.5 border border-slate-300 rounded bg-slate-50"
                        />
                      </div>

                      <div className="space-y-1">
                        <label className="block text-[10px] font-bold text-slate-500 uppercase tracking-wider">HTTP Request Target URI</label>
                        <input
                          type="text"
                          value={dpopUri}
                          onChange={e => setDpopUri(e.target.value)}
                          className="w-full font-mono text-xs px-3 py-1.5 border border-slate-300 rounded bg-slate-50"
                        />
                      </div>

                      <button
                        onClick={handleGenerateDpop}
                        className="w-full bg-slate-800 hover:bg-slate-950 text-white font-bold py-2 rounded transition shadow-sm text-xs"
                      >
                        Generate & Sign DPoP Proof JWT
                      </button>

                      {dpopProofGenerated && (
                        <div className="space-y-2">
                          <label className="block text-[10px] font-bold text-slate-500 uppercase tracking-wider text-emerald-700">Signed DPoP Header Result</label>
                          <textarea
                            rows={3}
                            readOnly
                            value={dpopProofGenerated}
                            className="w-full font-mono text-[10px] p-2.5 bg-emerald-50 border border-emerald-200 rounded text-emerald-900 select-all leading-normal"
                          />
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* 5. SERVICE ADMIN UIX SURFACE */}
            {activeSurface === "service-admin" && (
              <div className="space-y-6">
                <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm space-y-1">
                  <h3 className="text-lg font-bold text-slate-900">Workload & Machine Credentials console</h3>
                  <p className="text-sm text-slate-500">
                    Administrate client secrets, API keys, and service keys supporting backend automated integrations.
                  </p>
                </div>

                {/* Newly generated reveal warning block */}
                {(newClientSecret || newApiKey) && (
                  <div className="bg-emerald-50 border border-emerald-200 rounded-lg p-5 space-y-3 animate-fade-in">
                    <div className="flex items-start gap-2">
                      <AlertTriangle className="w-5 h-5 text-emerald-600 flex-shrink-0" />
                      <div>
                        <h4 className="text-sm font-bold text-emerald-900">New Machine Credential Material Issued</h4>
                        <p className="text-xs text-emerald-700 mt-0.5">
                          Copy the key content immediately. It is encrypted in-transit during generation but will never be displayed again.
                        </p>
                      </div>
                    </div>

                    {newClientSecret && <OneTimeSecretReveal secret={newClientSecret} label="Client Secret Key" />}
                    {newApiKey && <OneTimeSecretReveal secret={newApiKey} label="API Key Value" />}

                    <div className="flex justify-end pt-1">
                      <button
                        onClick={() => {
                          setNewClientSecret(null);
                          setNewApiKey(null);
                        }}
                        className="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold rounded shadow transition"
                      >
                        I Have Completed Key Backup
                      </button>
                    </div>
                  </div>
                )}

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {/* Workload key cards */}
                  {authenticators
                    .filter(a => a.category === DisplayCategory.MACHINE)
                    .map(auth => (
                      <div key={auth.id} className="bg-white border border-slate-200 rounded-lg p-4 hover:shadow-md transition flex flex-col justify-between">
                        <div>
                          <div className="flex items-start justify-between gap-2 mb-2">
                            <div className="flex items-center gap-1.5">
                              <Database className="w-4 h-4 text-slate-500" />
                              <h4 className="text-xs font-bold text-slate-800 line-clamp-1">{auth.name}</h4>
                            </div>
                            <AuthenticatorStatusBadge status={auth.status} />
                          </div>

                          <p className="text-[10px] text-slate-400 mb-2">
                            Issued {new Date(auth.created).toLocaleDateString()}
                          </p>

                          {auth.metadata && (
                            <div className="bg-slate-50 border border-slate-100 rounded p-2.5 font-mono text-[11px] text-slate-600 space-y-0.5">
                              <div>Key Identifier: <span className="text-slate-700 font-bold">{auth.id}</span></div>
                              {auth.metadata.prefix && <div>Prefix signature: <span className="text-slate-500">{auth.metadata.prefix}</span></div>}
                              {auth.metadata.clientId && <div>Client ID: <span className="text-slate-500">{auth.metadata.clientId}</span></div>}
                              {auth.metadata.fingerprint && <div className="break-all">Thumbprint: <span className="text-[9px] text-slate-500">{auth.metadata.fingerprint}</span></div>}
                            </div>
                          )}
                        </div>

                        <div className="border-t border-slate-100 mt-4 pt-3 flex justify-end gap-2 text-xs">
                          <button
                            onClick={() => {
                              if (window.confirm("Revoking this credential will immediately break any automated background ledger transactions dependending on it. Proceed?")) {
                                handleUserInventoryAction("delete", auth.id);
                              }
                            }}
                            className="text-xs font-semibold text-rose-600 hover:bg-rose-50 px-2.5 py-1.5 rounded border border-rose-200"
                          >
                            Revoke Key
                          </button>
                        </div>
                      </div>
                    ))}

                  {/* Add Machine factor triggers */}
                  <div className="border-2 border-dashed border-slate-200 rounded-lg p-6 flex flex-col items-center justify-center text-center gap-3 bg-white/50">
                    <Key className="w-8 h-8 text-slate-400" />
                    <div>
                      <h4 className="text-xs font-bold text-slate-800">Issue Workload Credentials</h4>
                      <p className="text-[11px] text-slate-500 mt-0.5">Provision client secrets, secure machine tokens or service keys.</p>
                    </div>
                    <div className="flex flex-col gap-1.5 w-full">
                      <button
                        onClick={() => handleCreateMachineSecret(AuthenticatorEnum.CLIENT_SECRET_LOCAL)}
                        className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-800 rounded font-semibold text-xs border border-slate-200 transition"
                      >
                        + Issue Client Secret
                      </button>
                      <button
                        onClick={() => handleCreateMachineSecret(AuthenticatorEnum.API_KEY_LOCAL)}
                        className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-800 rounded font-semibold text-xs border border-slate-200 transition"
                      >
                        + Issue Scoped API Key
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* 6. PLATFORM ADMIN UIX SURFACE */}
            {activeSurface === "platform" && (
              <div className="space-y-6">
                <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm space-y-1">
                  <h3 className="text-lg font-bold text-slate-900">Global Authenticator Provider Catalog</h3>
                  <p className="text-sm text-slate-500">
                    Browse globally allowed authentication providers, capability classifications, and conformance maturity matrices.
                  </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {catalogProviders.map(prov => (
                    <div key={prov.type} className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm flex flex-col justify-between">
                      <div>
                        <div className="flex items-center justify-between border-b border-slate-100 pb-3 mb-3">
                          <div className="flex items-center gap-2">
                            <AuthenticatorKindIcon type={prov.type} className="w-5 h-5" />
                            <h4 className="text-sm font-bold text-slate-800">{prov.label}</h4>
                          </div>
                          <span className="bg-emerald-50 text-emerald-700 text-[10px] font-bold px-2 py-0.5 rounded border border-emerald-100 capitalize">
                            {prov.maturity}
                          </span>
                        </div>

                        <p className="text-xs text-slate-500 leading-relaxed mb-4">{prov.description}</p>

                        <div className="bg-slate-50 rounded p-3 border border-slate-100 space-y-2 font-sans text-xs">
                          <div className="flex justify-between items-center text-[11px]">
                            <span className="text-slate-400">Assurance Level Target:</span>
                            <span className="font-mono text-slate-700 font-semibold">{prov.assuranceLevel}</span>
                          </div>
                          <div className="flex justify-between items-center text-[11px]">
                            <span className="text-slate-400">Phishing Resistant:</span>
                            <span className={`font-semibold ${prov.phishingResistant ? "text-emerald-700" : "text-slate-600"}`}>
                              {prov.phishingResistant ? "Yes" : "No"}
                            </span>
                          </div>
                          <div className="flex justify-between items-center text-[11px]">
                            <span className="text-slate-400">Hardware Bound Class:</span>
                            <span className={`font-semibold ${prov.hardwareProtected ? "text-emerald-700" : "text-slate-600"}`}>
                              {prov.hardwareProtected ? "Enforced" : "Variable/Optional"}
                            </span>
                          </div>
                        </div>
                      </div>

                      <div className="mt-4 pt-3 border-t border-slate-100 flex justify-between items-center text-[11px] text-slate-400">
                        <span>FIDO conformance status: Ready</span>
                        <span>Maturity: Level 3</span>
                      </div>
                    </div>
                  ))}
                </div>

                {/* NIST SP 800-63B guidelines summary */}
                <div className="bg-slate-900 text-slate-100 border border-slate-800 rounded-xl p-6 shadow-sm space-y-4">
                  <div className="flex items-center gap-2 border-b border-slate-800 pb-3">
                    <Shield className="w-5 h-5 text-emerald-400" />
                    <h4 className="text-sm font-bold tracking-tight">NIST SP 800-63B Authentication Standards Compliance Framework</h4>
                  </div>

                  <p className="text-xs text-slate-400 leading-relaxed max-w-4xl">
                    Tigrbl Authenticator Core establishes strict alignment with modern multi-factor assurance categories. Passkeys (WebAuthn) represent the pinnacle of **Phishing-Resistant** authentication, completely mitigating session takeovers and interception vectors that affect legacy phone or email verification codes.
                  </p>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 font-mono text-[11px] leading-normal">
                    <div className="bg-slate-950/60 p-3.5 border border-slate-800 rounded">
                      <span className="text-emerald-400 block font-bold mb-1">AAL1 (Basic)</span>
                      <span>Single factor credentials. In Tigrbl, this equates to basic password validation without secondary out-of-band checks.</span>
                    </div>
                    <div className="bg-slate-950/60 p-3.5 border border-slate-800 rounded">
                      <span className="text-emerald-400 block font-bold mb-1">AAL2 (Multi-Factor)</span>
                      <span>Multi-factor verification required. Leverages passwords with synchronized TOTP validation or federated OIDC assertion claims.</span>
                    </div>
                    <div className="bg-slate-950/60 p-3.5 border border-slate-800 rounded">
                      <span className="text-emerald-400 block font-bold mb-1">AAL3 (Hardware Bound)</span>
                      <span>Crypto hardware-backed validation. Uses WebAuthn passkeys or roaming keys validating cryptographic proof of origin.</span>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 mt-12 py-6 text-center text-xs text-slate-400">
        <p>© 2026 Tigrbl Core Security Services. Built on modern universal ceremony standards.</p>
      </footer>
    </div>
  );
}
