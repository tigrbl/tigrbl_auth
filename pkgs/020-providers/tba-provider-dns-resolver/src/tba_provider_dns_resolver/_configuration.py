"""Default DNS resolver configuration on Windows and POSIX."""

import ipaddress
import sys
from collections.abc import Iterable
from pathlib import Path


def _windows_nameservers() -> Iterable[str]:
    import ctypes
    from ctypes import wintypes

    class Address(ctypes.Structure):
        pass

    Address._fields_ = [
        ("next", ctypes.POINTER(Address)),
        ("address", ctypes.c_char * 16),
        ("mask", ctypes.c_char * 16),
        ("context", wintypes.DWORD),
    ]

    class FixedInfo(ctypes.Structure):
        _fields_ = [
            ("hostname", ctypes.c_char * 132),
            ("domain", ctypes.c_char * 132),
            ("current", ctypes.POINTER(Address)),
            ("servers", Address),
        ]

    get_params = ctypes.WinDLL("iphlpapi").GetNetworkParams
    get_params.argtypes = [ctypes.c_void_p, ctypes.POINTER(wintypes.ULONG)]
    get_params.restype = wintypes.DWORD
    size = wintypes.ULONG()
    if get_params(None, ctypes.byref(size)) != 111:
        return
    buffer = ctypes.create_string_buffer(size.value)
    if get_params(buffer, ctypes.byref(size)) != 0:
        return
    server = FixedInfo.from_buffer(buffer).servers
    while True:
        if server.address and server.address != b"0.0.0.0":
            yield server.address.decode("ascii")
        if not server.next:
            return
        server = server.next.contents


def _resolver_configuration() -> tuple[list[str], list[str], int]:
    if sys.platform == "win32":
        return list(_windows_nameservers()), [], 1
    try:
        config = Path("/etc/resolv.conf").read_text(encoding="ascii", errors="replace")
    except OSError:
        return [], [], 1
    return _parse_resolv_conf(config)


def _parse_resolv_conf(config: str) -> tuple[list[str], list[str], int]:
    servers = []
    suffixes = []
    ndots = 1
    for line in config.splitlines():
        tokens = line.partition("#")[0].partition(";")[0].split()
        if len(tokens) >= 2 and tokens[0] == "nameserver":
            try:
                servers.append(str(ipaddress.ip_address(tokens[1])))
            except ValueError:
                continue
        elif len(tokens) >= 2 and tokens[0] in ("search", "domain"):
            suffixes = tokens[1:] if tokens[0] == "search" else tokens[1:2]
        elif tokens and tokens[0] == "options":
            for token in tokens[1:]:
                name, _, value = token.partition(":")
                if name == "ndots" and value.isascii() and value.isdecimal():
                    ndots = min(15, int(value))
    return servers, suffixes, ndots
