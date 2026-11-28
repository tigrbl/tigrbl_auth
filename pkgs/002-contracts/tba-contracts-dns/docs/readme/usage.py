from tba_contracts_dns import TxtResult, TxtStatus


class StaticDns:
    def lookup_txt(self, name: str) -> TxtResult:
        if name == "_dmarc.example.com":
            return TxtResult(TxtStatus.FOUND, (b"v=DMARC1; p=reject",))
        return TxtResult(TxtStatus.ABSENT)
