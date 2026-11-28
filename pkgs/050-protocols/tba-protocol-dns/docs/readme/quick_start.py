from tba_protocol_dns.update import Update

update = Update('example.com.')
assert update.changes == []
