from tba_protocol_security_jose import capability_report

report = capability_report()
assert report
print(sorted(report))
