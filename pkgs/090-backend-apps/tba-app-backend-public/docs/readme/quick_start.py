from tba_app_backend_public import PUBLIC_BACKEND_APP_CONTRACT, app

assert callable(app)
assert PUBLIC_BACKEND_APP_CONTRACT.product_surface == "public-app"
assert "openid-configuration" in PUBLIC_BACKEND_APP_CONTRACT.production_capabilities
