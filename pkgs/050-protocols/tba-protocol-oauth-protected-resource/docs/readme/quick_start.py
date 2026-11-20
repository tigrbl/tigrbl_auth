from tba_protocol_oauth_protected_resource import capability_report

report = capability_report()
assert report
print(sorted(report))
