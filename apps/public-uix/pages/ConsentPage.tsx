import React from "react";
import { Card } from "../components/UI";
import "./ConsentPage.css";

interface ConsentPageProps {
  approveTarget: string;
  cancelTarget: string;
  clientName: string;
  scopes: string[];
}

export const ConsentPage: React.FC<ConsentPageProps> = ({
  approveTarget,
  cancelTarget,
  clientName,
  scopes,
}) => {
  const requestedScopes = scopes.length > 0 ? scopes : ["openid"];

  return (
    <div className="consent-page">
      <div className="consent-shell u-animate-in">
        <div className="consent-heading">
          <h1 className="consent-title">Review consent</h1>
          <p className="consent-subtitle">
            Confirm the information {clientName} may access through the governed tigrbl_auth public UIX.
          </p>
        </div>

        <Card className="consent-card">
          <div className="consent-section">
            <p className="consent-label">Client application</p>
            <p className="consent-client">{clientName}</p>
          </div>

          <div className="consent-section consent-section--scopes">
            <p className="consent-label">Requested scopes</p>
            <div className="consent-scopes">
              {requestedScopes.map((scope) => (
                <span
                  key={scope}
                  className="consent-scope"
                >
                  {scope}
                </span>
              ))}
            </div>
          </div>

          <p className="consent-copy">
            Approval returns you only to governed public UIX routes. Administrative and control-plane surfaces
            remain excluded from this browser-facing flow.
          </p>

          <div className="consent-actions">
            <button
              type="button"
              onClick={() => {
                window.location.hash = approveTarget;
              }}
              className="consent-approve"
            >
              Approve access
            </button>
            <button
              type="button"
              onClick={() => {
                window.location.hash = cancelTarget;
              }}
              className="consent-cancel"
            >
              Cancel
            </button>
          </div>
        </Card>
      </div>
    </div>
  );
};
