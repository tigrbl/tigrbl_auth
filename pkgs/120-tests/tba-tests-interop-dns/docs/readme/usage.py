from pathlib import Path

recipe = Path('pkgs/120-tests/tba-tests-interop-dns/Dockerfile').read_text()
assert 'FROM ' in recipe
