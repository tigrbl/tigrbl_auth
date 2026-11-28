# RFC 8785 JCS evidence

Evidence for `feat:target-rfc-8785` and `feat:jcs-canonical-json` is the
pytest conformance suite for `tba-codec-jcs` at
`pkgs/120-tests/tba-tests-wire-codecs/tests/conformance/backlog/test_rfc8785_jcs.py`.

Verified command:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests\conformance\backlog\test_rfc8785_jcs.py
```

Observed result:

```text
11 passed
```
