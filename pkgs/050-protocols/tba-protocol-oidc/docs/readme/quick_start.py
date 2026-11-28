from tba_protocol_oidc import capability_report

report = capability_report()
assert report
print(sorted(report))
