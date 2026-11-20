from tba_protocol_security_event_set import capability_report

report = capability_report()
assert report
print(sorted(report))
