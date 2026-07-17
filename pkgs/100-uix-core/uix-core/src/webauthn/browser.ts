import { decodeBase64Url, encodeBase64Url } from "./base64url";

function descriptors(values?: PublicKeyCredentialDescriptorJSON[]): PublicKeyCredentialDescriptor[] | undefined {
  return values?.map((value) => ({
    type: "public-key",
    id: decodeBase64Url(value.id),
    transports: value.transports as AuthenticatorTransport[] | undefined,
  }));
}

export function creationOptionsFromJSON(value: PublicKeyCredentialCreationOptionsJSON): PublicKeyCredentialCreationOptions {
  return {
    ...value,
    challenge: decodeBase64Url(value.challenge),
    user: { ...value.user, id: decodeBase64Url(value.user.id) },
    excludeCredentials: descriptors(value.excludeCredentials),
  } as unknown as PublicKeyCredentialCreationOptions;
}

export function requestOptionsFromJSON(value: PublicKeyCredentialRequestOptionsJSON): PublicKeyCredentialRequestOptions {
  return {
    ...value,
    challenge: decodeBase64Url(value.challenge),
    allowCredentials: descriptors(value.allowCredentials),
  } as unknown as PublicKeyCredentialRequestOptions;
}

export function credentialToJSON(credential: PublicKeyCredential): Record<string, unknown> {
  const response = credential.response;
  const shared = {
    clientDataJSON: encodeBase64Url(response.clientDataJSON),
  };
  const responseJSON = response instanceof AuthenticatorAttestationResponse
    ? {
        ...shared,
        attestationObject: encodeBase64Url(response.attestationObject),
        transports: response.getTransports?.() ?? [],
      }
    : {
        ...shared,
        authenticatorData: encodeBase64Url((response as AuthenticatorAssertionResponse).authenticatorData),
        signature: encodeBase64Url((response as AuthenticatorAssertionResponse).signature),
        userHandle: (response as AuthenticatorAssertionResponse).userHandle
          ? encodeBase64Url((response as AuthenticatorAssertionResponse).userHandle!)
          : null,
      };
  return {
    id: credential.id,
    rawId: encodeBase64Url(credential.rawId),
    type: credential.type,
    authenticatorAttachment: credential.authenticatorAttachment,
    clientExtensionResults: credential.getClientExtensionResults(),
    response: responseJSON,
  };
}
