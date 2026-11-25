from tba_runtime_hosted_authorization_continuation import ValidatedAuthorizationRequest

request = ValidatedAuthorizationRequest.from_parameters(
    'https://issuer.example.test',
    {'client_id': 'example-app', 'redirect_uri': 'https://rp.example.test/callback'},
)
assert request.client_id == 'example-app'
