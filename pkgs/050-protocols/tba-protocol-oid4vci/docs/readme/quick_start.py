from tba_protocol_oid4vci import capability_report

report = capability_report()
assert report
print(sorted(report))
