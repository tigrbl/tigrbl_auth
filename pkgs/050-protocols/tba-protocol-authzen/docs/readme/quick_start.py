from tba_protocol_authzen import capability_report

report = capability_report()
assert report
print(sorted(report))
