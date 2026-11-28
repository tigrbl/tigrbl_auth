from tba_protocol_gnap import capability_report

report = capability_report()
assert report
print(sorted(report))
