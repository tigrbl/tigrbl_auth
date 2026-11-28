from tba_provider_dns_txt import DnsTxtResolver

answer = DnsTxtResolver(timeout=3).lookup_txt("_dmarc.example.com")
print(answer.status.value, answer.records)
