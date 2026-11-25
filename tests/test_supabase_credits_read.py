"""Regression: balances must be read with the service-role client.

`profiles` has row level security, so the anon client sees no rows unless a
user session happens to be attached to it. Reading with the anon key made
every balance show as 0 on a freshly started server.
"""

import src.database.supabase_credits as credits_module


class _Result:
    def __init__(self, data):
        self.data = data


class _Query:
    def __init__(self, data):
        self._data = data

    def select(self, *_args, **_kwargs):
        return self

    def eq(self, *_args, **_kwargs):
        return self

    def execute(self):
        return _Result(self._data)


class _Client:
    def __init__(self, data):
        self._data = data

    def table(self, name):
        assert name == "profiles"
        return _Query(self._data)


class _AnonClientMustNotBeUsed:
    def table(self, _name):
        raise AssertionError("balance read used the anon client")


def test_balance_is_read_with_service_client(monkeypatch):
    monkeypatch.setattr(credits_module, "supabase", _AnonClientMustNotBeUsed(), raising=False)
    monkeypatch.setattr(credits_module, "get_service_client", lambda: _Client([{"credits": 23}]))
    assert credits_module.get_supabase_credits("user-1") == 23


def test_missing_profile_reads_as_zero(monkeypatch):
    monkeypatch.setattr(credits_module, "get_service_client", lambda: _Client([]))
    assert credits_module.get_supabase_credits("user-1") == 0
