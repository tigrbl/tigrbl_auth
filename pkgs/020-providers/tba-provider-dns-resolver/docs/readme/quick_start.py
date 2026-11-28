from tba_provider_dns_resolver import Resolver

resolver = Resolver(configure=False)
assert not resolver.nameservers
