from tba_protocol_oid4vp import capability_report

report = capability_report()
assert report
print(sorted(report))
