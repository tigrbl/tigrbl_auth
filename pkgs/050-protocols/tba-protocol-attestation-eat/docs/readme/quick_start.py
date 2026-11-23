from tba_protocol_attestation_eat import capability_report

report = capability_report()
assert report
print(sorted(report))
