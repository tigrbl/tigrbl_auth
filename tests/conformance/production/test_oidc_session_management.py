from tigrbl_auth_protocol_oidc.standards.session_mgmt import (
    compute_session_state,
    describe,
    validate_session_state,
)



def test_session_state_depends_on_client_redirect_and_salt():
    sid = '00000000-0000-0000-0000-000000000001'
    state_one = compute_session_state(client_id='client', redirect_uri='https://rp.example/cb', session_id=sid, salt='salt-a')
    state_two = compute_session_state(client_id='client', redirect_uri='https://rp.example/cb', session_id=sid, salt='salt-b')
    assert state_one != state_two
    assert state_one.endswith('.salt-a')



def test_session_state_validation_is_origin_bound():
    sid = '00000000-0000-0000-0000-000000000001'
    presented = compute_session_state(client_id='client', redirect_uri='https://rp.example/cb', session_id=sid, salt='salt-a')
    valid = validate_session_state(
        presented_session_state=presented,
        client_id='client',
        redirect_uri='https://rp.example/cb',
        session_id=sid,
    )
    invalid = validate_session_state(
        presented_session_state=presented,
        client_id='client',
        redirect_uri='https://other.example/cb',
        session_id=sid,
    )
    assert valid.valid is True
    assert invalid.valid is False



def test_session_management_description_remains_truthful_about_current_claims():
    description = describe()
    assert description['session_state_validation_supported'] is True
    assert description['check_session_iframe_claimed'] is False
