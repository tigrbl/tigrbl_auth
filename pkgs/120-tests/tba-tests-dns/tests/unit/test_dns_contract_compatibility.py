from tba_contracts_dns import TxtResult, TxtStatus
from tba_provider_dns_txt.contracts import TxtResult as LegacyTxtResult
from tba_provider_dns_txt.contracts import TxtStatus as LegacyTxtStatus


def test_dns_contract_exports_remain_identical():
    assert LegacyTxtResult is TxtResult
    assert LegacyTxtStatus is TxtStatus
