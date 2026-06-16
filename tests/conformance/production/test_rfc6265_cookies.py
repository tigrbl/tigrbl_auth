from tigrbl_auth.standards.http.cookies import (
    COOKIE_VALUE_VERSION,
    build_session_cookie_value,
    extract_session_cookie,
    parse_session_cookie_value,
)


def test_opaque_session_cookie_roundtrip_uses_versioned_value():
    value = build_session_cookie_value('00000000-0000-0000-0000-000000000001', 'secret')
    assert value.startswith(f"{COOKIE_VALUE_VERSION}.")
    parsed = parse_session_cookie_value(value)
    assert parsed is not None
    assert str(parsed.session_id) == '00000000-0000-0000-0000-000000000001'
    assert parsed.secret == 'secret'


def test_extract_session_cookie_prefers_materialized_cookie_mapping():
    class Request:
        cookies = {'sid': 'v1.00000000-0000-0000-0000-000000000001.secret'}
        headers = {'cookie': 'sid=ignored'}

    assert extract_session_cookie(Request()) == 'v1.00000000-0000-0000-0000-000000000001.secret'


def test_extract_session_cookie_falls_back_to_cookie_header():
    class Request:
        cookies = None
        headers = {
            'cookie': 'theme=dark; sid=v1.00000000-0000-0000-0000-000000000001.secret; other=value'
        }

    assert extract_session_cookie(Request()) == 'v1.00000000-0000-0000-0000-000000000001.secret'


def test_extract_session_cookie_falls_back_to_tuple_headers():
    class Request:
        cookies = None
        headers = [
            ('host', 'localhost'),
            ('cookie', 'theme=dark; sid=v1.00000000-0000-0000-0000-000000000001.secret; other=value'),
        ]

    assert extract_session_cookie(Request()) == 'v1.00000000-0000-0000-0000-000000000001.secret'


def test_extract_session_cookie_falls_back_to_asgi_byte_headers():
    class Request:
        cookies = None
        headers = [
            (b'host', b'localhost'),
            (b'cookie', b'theme=dark; sid=v1.00000000-0000-0000-0000-000000000001.secret; other=value'),
        ]

    assert extract_session_cookie(Request()) == 'v1.00000000-0000-0000-0000-000000000001.secret'
