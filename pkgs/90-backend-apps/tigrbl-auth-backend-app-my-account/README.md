# tigrbl-auth-backend-app-my-account

End-user self-service account API front door for Tigrbl Auth.

This package exposes the authenticated current subject's account surface:

- `GET /account/profile`
- `PATCH /account/profile`
- `GET /account/sessions`
- `DELETE /account/sessions/{session_id}`
- `GET /account/authorized-apps`
- `DELETE /account/authorized-apps/{client_id}`
- `GET /account/consents`
- `DELETE /account/consents/{consent_id}`
- `POST /account/password/change`

It does not expose platform administration, tenant-wide user management, RPC,
or table CRUD. All account operations are scoped to the authenticated end user.
