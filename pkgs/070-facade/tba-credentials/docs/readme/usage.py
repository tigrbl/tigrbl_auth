from tba_credentials import (
    CredentialKind,
    create_password_credential,
    verify_credential,
)
from tba_credentials import digital, workload

credential = create_password_credential("subject:alice", "correct horse battery staple")
assert credential.kind is CredentialKind.PASSWORD
assert verify_credential(credential, "correct horse battery staple")
