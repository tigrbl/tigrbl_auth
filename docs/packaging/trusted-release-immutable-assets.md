# Upload release assets before publishing immutable releases

The first TBA package release run, https://github.com/tigrbl/tigrbl_auth/actions/runs/40830079099 , successfully published tba-primitives-identity 0.4.0.dev2 to PyPI. Both distribution hashes and wheel metadata were verified against PyPI, and an isolated installation imported successfully. Six local primitive package tests passed.

Its GitHub release step failed after publishing the release: immutable releases reject subsequent asset uploads. Keep the release as a draft while the action uploads all distribution assets, then use the workflow token to publish the completed draft. Preserve prerelease and make-latest settings. Publishing occurs only after the asset step succeeds.

The already published first GitHub release cannot have missing assets appended. Its verified PyPI distributions remain available. Do not delete it or overwrite package tags to hide this history. Verify subsequent release assets through the GitHub API before advancing.
