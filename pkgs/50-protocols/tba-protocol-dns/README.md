# tba-protocol-dns

DNS zone transfers, dynamic updates, DNSSEC, ZONEMD, verified resolver
discovery, and GSS-TSIG negotiation. The package uses
[tba-provider-dns-resolver](../../20-providers/tba-provider-dns-resolver) for network exchange
and [tba-concrete-dns-zone](../../10-concrete/tba-concrete-dns-zone) for zone
state. Install `tba-protocol-dns[dnssec]` to sign and validate DNSSEC
records.

Import protocol modules from `tba_protocol_dns` and zones from
`tba_concrete_dns_zone.zone` or `tba_concrete_dns_zone.btreezone`. Use
`tba_protocol_dns.ddr.try_ddr(resolver)` or
`await tba_protocol_dns.ddr.try_ddr_async(resolver)` for verified discovery.

The [DNS interoperability suite](../../120-tests/tba-tests-interop-dns)
exercises GSS-TSIG against BIND and Kerberos.
