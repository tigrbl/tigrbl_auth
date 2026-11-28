from tba_provider_dns_resolver import AsyncResolver

resolver = AsyncResolver(configure=False)
resolver.nameservers = ['192.0.2.53']
assert resolver.nameservers == ('192.0.2.53',)
