import { walkthrough } from "../../_prototype/dashboard";
import "../../_prototype/styles.css";

walkthrough("Public Identity", "Walk through sample identity screens. This local demo uses no credentials and creates no session.", {
  "Sign in": [
    "Choose a sign-in method for the sample account.",
    "Review the sample account and continue to the signed-in screen."
  ],
  "Register": [
    "Review the fields a new account would provide.",
    "Preview the email verification screen."
  ],
  "Recover access": [
    "Choose the sample recovery channel.",
    "Review the confirmation shown after a recovery request."
  ],
  "OAuth consent": [
    "Review the sample application’s request for profile access.",
    "Preview the return to the requesting application."
  ]
});
