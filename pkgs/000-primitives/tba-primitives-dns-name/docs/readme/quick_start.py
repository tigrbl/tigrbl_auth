from tba_primitives_dns_name.name import from_text

name = from_text('example.com.')
assert name.is_absolute()
