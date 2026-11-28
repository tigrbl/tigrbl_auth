import { walkthrough } from "../../_prototype/dashboard";
import "../../_prototype/styles.css";

walkthrough("Universal Authenticator", "Preview enrollment and verification ceremonies with sample data. No hardware or live identity service is required.", {
  "Passkey enrollment": [
    "Choose the sample account and review the passkey enrollment prompt.",
    "Preview confirmation after a device registers a passkey."
  ],
  "One-time code verification": [
    "Review how a one-time code prompt looks for the sample account.",
    "Preview the confirmation after the code is accepted."
  ],
  "Recovery codes": [
    "Review the recovery code rotation prompt.",
    "Preview the confirmation that the previous codes have been replaced."
  ]
});
