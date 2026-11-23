from tba_protocol_oidc_relying_party import capability_report

report = capability_report()
assert report
print(sorted(report))
