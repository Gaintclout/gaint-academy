from app.core.auth import new_session_token, token_hash
def test_session_token_is_hashed():
    raw,digest=new_session_token()
    assert raw != digest
    assert token_hash(raw)==digest
    assert len(digest)==64
