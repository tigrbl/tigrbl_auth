from tigrbl_cwt_concrete import CwtClaimsSet, decode_cwt_claims
class CwtProtocol:
    def __init__(self,cose_protocol,profile): self.cose_protocol,self.profile=cose_protocol,profile
    def issue(self,claims:CwtClaimsSet,*,key_reference:str,headers:dict[object,object]): return self.cose_protocol.sign1(claims.encode(),key_reference=key_reference,headers=headers)
    def verify(self,envelope):
        result=self.cose_protocol.verify1(envelope)
        if result.payload is None: raise ValueError("verified CWT has no payload")
        claims=decode_cwt_claims(result.payload); self.profile.validate(claims.claims,"Sign1"); return claims,result