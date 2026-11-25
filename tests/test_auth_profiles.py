"""Auth flows that touch the `profiles` table. No network.

`profiles` has row level security, so these lookups must use the
service-role client: the anon client sees no rows, which silently let taken
emails and usernames through. A bad token must give 401, not 500.
"""

from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

import src.auth.supabase_service as svc
import src.database.supabase_credits as credits_module
from src.api.main import app


class _Result:
    def __init__(self, data):
        self.data = data


class _Query:
    def __init__(self, db):
        self.db = db
        self.filters = []
        self.row = None

    def select(self, *_args, **_kwargs):
        return self

    def eq(self, column, value):
        self.filters.append((column, value))
        return self

    def insert(self, row):
        self.row = row
        return self

    def execute(self):
        if self.row is not None:
            self.db.rows.append(self.row)
            return _Result([self.row])
        return _Result([r for r in self.db.rows if all(r.get(c) == v for c, v in self.filters)])


class FakeServiceDB:
    def __init__(self, rows=None):
        self.rows = list(rows or [])

    def table(self, name):
        assert name == "profiles"
        return _Query(self)


class FakeAnon:
    """Anon client: auth calls are allowed, table reads are not."""

    def __init__(self, auth):
        self.auth = auth

    def table(self, _name):
        raise AssertionError("profiles was read with the anon client")


@pytest.fixture
def db(monkeypatch):
    database = FakeServiceDB([{"id": "u-1", "email": "taken@example.com", "username": "taken", "credits": 5}])
    monkeypatch.setattr(svc, "get_service_client", lambda: database)
    monkeypatch.setattr(credits_module, "get_service_client", lambda: database)
    return database


def _auth(**methods):
    return SimpleNamespace(**methods)


def _raise(*_args, **_kwargs):
    raise RuntimeError("supabase said no")


# --- /auth/me ----------------------------------------------------------------

def test_me_with_bad_token_returns_401(monkeypatch, db):
    monkeypatch.setattr(svc, "supabase", FakeAnon(_auth(get_user=_raise)))
    response = TestClient(app).get("/auth/me", headers={"Authorization": "Bearer expired"})
    assert response.status_code == 401


def test_me_returns_balance_from_service_client(monkeypatch, db):
    user = SimpleNamespace(id="u-1", email="taken@example.com", user_metadata={})
    monkeypatch.setattr(svc, "supabase", FakeAnon(_auth(get_user=lambda _t: SimpleNamespace(user=user))))
    response = TestClient(app).get("/auth/me", headers={"Authorization": "Bearer ok"})
    assert response.status_code == 200
    assert response.json()["credits"] == 5
    assert response.json()["user"]["username"] == "taken"


# --- signup duplicate checks ---------------------------------------------------

def test_signup_rejects_registered_email(monkeypatch, db):
    monkeypatch.setattr(svc, "supabase", FakeAnon(_auth(sign_up=_raise)))
    with pytest.raises(ValueError, match="Email is already registered"):
        svc.signup_user("taken@example.com", "secret123", "newname")


def test_signup_rejects_taken_username(monkeypatch, db):
    monkeypatch.setattr(svc, "supabase", FakeAnon(_auth(sign_up=_raise)))
    with pytest.raises(ValueError, match="Username is already taken"):
        svc.signup_user("new@example.com", "secret123", "taken")


def test_resend_rejects_verified_email(monkeypatch, db):
    monkeypatch.setattr(svc, "supabase", FakeAnon(_auth(resend=_raise)))
    with pytest.raises(ValueError, match="already verified"):
        svc.resend_signup_otp("taken@example.com")


# --- verify creates the profile -------------------------------------------------

def test_verify_creates_profile_with_service_client(monkeypatch, db):
    user = SimpleNamespace(id="u-2", email="new@example.com", user_metadata={"username": "newbie"})
    session = SimpleNamespace(access_token="tok")
    verify = lambda _payload: SimpleNamespace(user=user, session=session)
    monkeypatch.setattr(svc, "supabase", FakeAnon(_auth(verify_otp=verify)))
    monkeypatch.setattr(svc, "claim_free_grant", lambda *_a: 20)

    payload = svc.verify_user_otp("new@example.com", "123456")

    created = [r for r in db.rows if r["id"] == "u-2"]
    assert created and created[0]["username"] == "newbie"
    assert payload["user"]["username"] == "newbie"
