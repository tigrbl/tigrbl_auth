from tba_protocol_dns.update import Update

update = Update('example.com.')
update.add('www', 60, 'A', '192.0.2.10')
assert len(update.changes) == 1
