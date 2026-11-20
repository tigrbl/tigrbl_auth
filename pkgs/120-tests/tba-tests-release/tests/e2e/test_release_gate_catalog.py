
from pathlib import Path
import yaml

def test_release_gate_order_exists():
    root = Path(__file__).resolve().parents[5]
    data = yaml.safe_load((root / 'compliance' / 'gates' / 'gate-order.yaml').read_text())
    assert data['ordered_gates']
