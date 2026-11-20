from tba_protocol_oauth import OAuthClient, OAuthProtocolService

service = OAuthProtocolService()
client = OAuthClient(
    client_id="client-a", redirect_uris=("https://app.example/callback",)
)
