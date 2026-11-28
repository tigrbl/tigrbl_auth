from tba_protocol_jwt import capability_report

report = capability_report()
assert report
print(sorted(report))
