# tigrbl-replay-bases

Shared protocol-neutral replay reservation behavior. Implementations must make
check-and-reserve atomic; the base does not select persistence or networking.
