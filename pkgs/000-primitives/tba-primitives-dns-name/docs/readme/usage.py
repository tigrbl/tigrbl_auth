from tba_primitives_dns_name.name import from_text

name = from_text('www.example.com.')
assert name.to_text() == 'www.example.com.'
