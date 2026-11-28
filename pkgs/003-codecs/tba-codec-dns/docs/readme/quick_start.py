from tba_codec_dns.wire import make_query

query = make_query('example.com.', 'A')
assert query.to_wire()
