from tba_concrete_dns_zone.btreezone import Zone

zone = Zone.from_text('$ORIGIN example.com.\n$TTL 300\n@ SOA ns admin 1 1800 600 86400 60\n@ NS ns\nns A 192.0.2.53\n')
assert zone.get_soa().serial == 1
