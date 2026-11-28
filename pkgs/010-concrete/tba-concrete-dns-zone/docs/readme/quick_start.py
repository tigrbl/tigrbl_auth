from tba_concrete_dns_zone.zone import Zone

zone = Zone('example.com.')
assert zone.origin is not None
