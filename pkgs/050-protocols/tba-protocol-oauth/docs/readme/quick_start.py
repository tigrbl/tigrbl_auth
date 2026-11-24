from tba_protocol_oauth import capability_report

report = capability_report()
assert report
print(sorted(report))
