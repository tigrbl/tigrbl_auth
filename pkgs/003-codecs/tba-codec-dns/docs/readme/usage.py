from tba_codec_dns.wire import Message, make_query

query = make_query('example.com.', 'TXT')
assert Message.from_wire(query.to_wire()).questions == query.questions
