"""Current-account self-service capability over injected operations."""

from __future__ import annotations

import inspect
from collections.abc import Callable
from typing import TypeAlias

from tigrbl_capability import Capability
from tigrbl_identity_contracts.account_self_service import (
    AccountConsent,
    AccountMutation,
    AccountNotFoundError,
    AccountPrincipal,
    AccountProfile,
    AccountProfileUpdate,
    AccountSession,
)
from tigrbl_identity_contracts.capabilities import (
    CapabilityDefinition,
    CapabilityOperation,
)


AccountOperation: TypeAlias = Callable[..., object]


async def _resolve(value: object) -> object:
    return await value if inspect.isawaitable(value) else value


class AccountSelfServiceCapability(Capability):
    def __init__(
        self,
        *,
        profile_reader: AccountOperation,
        profile_updater: AccountOperation,
        password_changer: AccountOperation,
        session_lister: AccountOperation,
        session_revoker: AccountOperation,
        consent_lister: AccountOperation,
        consent_revoker: AccountOperation,
        authorized_app_revoker: AccountOperation,
    ) -> None:
        delegates = {
            "get_profile": profile_reader,
            "update_profile": profile_updater,
            "change_password": password_changer,
            "list_sessions": session_lister,
            "revoke_session": session_revoker,
            "list_consents": consent_lister,
            "list_authorized_apps": consent_lister,
            "revoke_consent": consent_revoker,
            "revoke_authorized_app": authorized_app_revoker,
        }
        invalid = tuple(
            sorted(name for name, target in delegates.items() if not callable(target))
        )
        if invalid:
            raise TypeError(
                f"account self-service delegates must be callable: {invalid}"
            )
        self._delegates = delegates
        super().__init__(
            CapabilityDefinition("account.self-service", "1.0"),
            operations={
                name: CapabilityOperation(target=getattr(self, name), delegated=True)
                for name in delegates
            },
        )

    @staticmethod
    def _principal(value: AccountPrincipal) -> AccountPrincipal:
        if not isinstance(value, AccountPrincipal):
            raise TypeError("account self-service requires AccountPrincipal")
        return value

    async def get_profile(self, principal: AccountPrincipal) -> AccountProfile:
        profile = await _resolve(
            self._delegates["get_profile"](self._principal(principal))
        )
        if not isinstance(profile, AccountProfile):
            raise TypeError("profile reader returned an invalid record")
        return profile

    async def update_profile(
        self, principal: AccountPrincipal, spec: AccountProfileUpdate
    ) -> AccountProfile:
        profile = await _resolve(
            self._delegates["update_profile"](self._principal(principal), spec)
        )
        if not isinstance(profile, AccountProfile):
            raise TypeError("profile updater returned an invalid record")
        return profile

    async def change_password(
        self,
        principal: AccountPrincipal,
        current_password: str,
        new_password: str,
    ) -> AccountMutation:
        result = await _resolve(
            self._delegates["change_password"](
                self._principal(principal), current_password, new_password
            )
        )
        if not isinstance(result, AccountMutation):
            raise TypeError("password changer returned an invalid result")
        return result

    async def list_sessions(
        self, principal: AccountPrincipal
    ) -> tuple[AccountSession, ...]:
        sessions = tuple(
            await _resolve(self._delegates["list_sessions"](self._principal(principal)))
        )
        if not all(isinstance(session, AccountSession) for session in sessions):
            raise TypeError("session lister returned an invalid record")
        return sessions

    async def revoke_session(
        self, principal: AccountPrincipal, session_id: str
    ) -> AccountMutation:
        result = await _resolve(
            self._delegates["revoke_session"](self._principal(principal), session_id)
        )
        if result is None:
            raise AccountNotFoundError("session not found")
        if not isinstance(result, AccountMutation):
            raise TypeError("session revoker returned an invalid result")
        return result

    async def list_consents(
        self, principal: AccountPrincipal
    ) -> tuple[AccountConsent, ...]:
        consents = tuple(
            await _resolve(self._delegates["list_consents"](self._principal(principal)))
        )
        if not all(isinstance(consent, AccountConsent) for consent in consents):
            raise TypeError("consent lister returned an invalid record")
        return consents

    async def list_authorized_apps(
        self, principal: AccountPrincipal
    ) -> tuple[AccountConsent, ...]:
        return await self.list_consents(principal)

    async def revoke_consent(
        self, principal: AccountPrincipal, consent_id: str
    ) -> AccountConsent:
        consent = await _resolve(
            self._delegates["revoke_consent"](self._principal(principal), consent_id)
        )
        if consent is None:
            raise AccountNotFoundError("consent not found")
        if not isinstance(consent, AccountConsent):
            raise TypeError("consent revoker returned an invalid record")
        return consent

    async def revoke_authorized_app(
        self, principal: AccountPrincipal, client_id: str
    ) -> tuple[AccountConsent, ...]:
        consents = tuple(
            await _resolve(
                self._delegates["revoke_authorized_app"](
                    self._principal(principal), client_id
                )
            )
        )
        if not consents:
            raise AccountNotFoundError("authorized app not found")
        if not all(isinstance(consent, AccountConsent) for consent in consents):
            raise TypeError("authorized app revoker returned an invalid record")
        return consents


__all__ = ["AccountOperation", "AccountSelfServiceCapability"]
