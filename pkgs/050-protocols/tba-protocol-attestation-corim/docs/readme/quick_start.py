from tba_protocol_attestation_corim import capability_report

report = capability_report()
assert report
print(sorted(report))
