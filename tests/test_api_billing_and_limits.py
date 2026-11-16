"""API tests for billing rules, abuse limits and payments. No network."""

import json

import pytest
from fastapi.testclient import TestClient

from src.api import services
from src.api.config import is_allowed_redirect
from src.api.dependencies import get_optional_user_id_from_auth, get_user_id_from_auth
from src.api.main import app
from src.api.routers import jobs, payments
from src.credits import ledger
from src.credits.packs import CREDIT_PACKS, get_pack
from src.security import limits
from src.security.emails import is_disposable, normalize_email

DRAFT = {
    "title": "PM", "about_company": "A", "about_role": "B", "responsibilities": ["r"],
    "requirements": ["q"], "nice_to_haves": [], "benefits": [], "why_join_us": "", "equal_opportunity": "",
}
JOB_INFO = {"company_name": "Acme", "role_title": "PM"}


@pytest.fixture(autouse=True)
def clean_state(monkeypatch):
    limits.reset_for_tests()
    services.clear_cache()
    monkeypatch.delenv("TURNSTILE_SECRET_KEY", raising=False)
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def client():
    return TestClient(app)


def sign_in(user_id="user-1"):
    app.dependency_overrides[get_user_id_from_auth] = lambda: user_id
    app.dependency_overrides[get_optional_user_id_from_auth] = lambda: user_id


def parse_sse(response):
    return [json.loads(line[6:]) for line in response.text.splitlines() if line.startswith("data: ")]


def fake_generate(request):
    yield {"event": "chunk", "data": "x"}
    yield {"event": "done", "draft": DRAFT, "markdown": "# PM\n\nFULL TEXT", "quality": {"score": 90}}


# --- guests: generate is free and full ------------------------------------

def test_guest_gets_full_draft_without_login(client, monkeypatch):
    monkeypatch.setattr(jobs, "stream_generate_job_description", fake_generate)
    response = client.post("/generate", json={"job_info": JOB_INFO})
    events = parse_sse(response)
    assert response.status_code == 200
    assert events[-1]["markdown"] == "# PM\n\nFULL TEXT"
    assert "is_preview" not in events[-1]


def test_guest_daily_limit_blocks_after_ten(client, monkeypatch):
    monkeypatch.setattr(jobs, "stream_generate_job_description", fake_generate)
    for _ in range(limits.GUEST_DAILY_LIMIT):
        assert client.post("/generate", json={"job_info": JOB_INFO}).status_code == 200
    blocked = client.post("/generate", json={"job_info": JOB_INFO})
    assert blocked.status_code == 429


def test_signed_in_users_skip_guest_limit_and_are_not_charged(client, monkeypatch):
    sign_in()
    monkeypatch.setattr(jobs, "stream_generate_job_description", fake_generate)
    monkeypatch.setattr(jobs, "get_supabase_credits", lambda uid: 7)
    spent = []
    monkeypatch.setattr(ledger, "spend", lambda *a: spent.append(a) or 0)
    for _ in range(limits.GUEST_DAILY_LIMIT + 2):
        response = client.post("/generate", json={"job_info": JOB_INFO})
        assert response.status_code == 200
    assert spent == []
    assert parse_sse(response)[-1]["credits_remaining"] == 7


def test_global_cap_is_a_kill_switch(client, monkeypatch):
    monkeypatch.setattr(jobs, "stream_generate_job_description", fake_generate)
    monkeypatch.setattr(limits, "GLOBAL_DAILY_LLM_CALLS", 1)
    assert client.post("/generate", json={"job_info": JOB_INFO}).status_code == 200
    assert client.post("/generate", json={"job_info": JOB_INFO}).status_code == 503


def test_turnstile_required_for_guests_when_configured(client, monkeypatch):
    monkeypatch.setenv("TURNSTILE_SECRET_KEY", "secret")
    monkeypatch.setattr(jobs, "stream_generate_job_description", fake_generate)
    assert client.post("/generate", json={"job_info": JOB_INFO}).status_code == 400


def test_turnstile_not_required_for_signed_in_users(client, monkeypatch):
    monkeypatch.setenv("TURNSTILE_SECRET_KEY", "secret")
    sign_in()
    monkeypatch.setattr(jobs, "stream_generate_job_description", fake_generate)
    monkeypatch.setattr(jobs, "get_supabase_credits", lambda uid: 1)
    assert client.post("/generate", json={"job_info": JOB_INFO}).status_code == 200


# --- refine: typed feedback costs one credit -------------------------------

REFINE_BODY = {"company_name": "Acme", "current_draft": DRAFT, "user_request": "add a perk"}


def test_refine_requires_sign_in(client):
    assert client.post("/refine", json=REFINE_BODY).status_code == 401


def test_refine_charges_one_credit_on_success(client, monkeypatch):
    sign_in()
    calls = []
    monkeypatch.setattr(ledger, "spend", lambda uid, cost, key: calls.append((uid, cost)) or 19)
    monkeypatch.setattr(ledger, "refund", lambda *a: pytest.fail("must not refund"))
    monkeypatch.setattr(jobs, "stream_refine_job_description", fake_generate)
    events = parse_sse(client.post("/refine", json=REFINE_BODY))
    assert calls == [("user-1", 1)]
    assert events[-1]["event"] == "done" and events[-1]["credits_remaining"] == 19


def test_refine_returns_402_without_credits(client, monkeypatch):
    sign_in()
    monkeypatch.setattr(ledger, "spend", lambda *a: ledger.INSUFFICIENT)
    assert client.post("/refine", json=REFINE_BODY).status_code == 402


def test_refine_refunds_when_llm_fails(client, monkeypatch):
    sign_in()
    refunds = []
    monkeypatch.setattr(ledger, "spend", lambda *a: 19)
    monkeypatch.setattr(ledger, "refund", lambda uid, amount, key: refunds.append((uid, amount)) or 20)

    def failing(request):
        yield {"event": "chunk", "data": "x"}
        raise ValueError("bad json")

    monkeypatch.setattr(jobs, "stream_refine_job_description", failing)
    events = parse_sse(client.post("/refine", json=REFINE_BODY))
    assert [e["event"] for e in events][-2:] == ["error", "refunded"]
    assert events[-1]["credits_remaining"] == 20
    assert refunds == [("user-1", 1)]


def test_blank_or_huge_refine_text_is_rejected_before_charging(client, monkeypatch):
    sign_in()
    monkeypatch.setattr(ledger, "spend", lambda *a: pytest.fail("must not charge"))
    assert client.post("/refine", json={**REFINE_BODY, "user_request": "   "}).status_code == 422
    assert client.post("/refine", json={**REFINE_BODY, "user_request": "x" * 3000}).status_code == 422


# --- click-based edits are free ---------------------------------------------

def test_quick_edit_and_section_regen_are_free_for_guests(client, monkeypatch):
    monkeypatch.setattr(ledger, "spend", lambda *a: pytest.fail("must not charge"))
    result = {"draft": DRAFT, "markdown": "# PM", "quality": {"score": 1}}
    monkeypatch.setattr(jobs, "quick_edit_job_description", lambda *a: result)
    monkeypatch.setattr(jobs, "regenerate_section_job_description", lambda *a: result)
    body = {"current_draft": DRAFT, "action": "shorter"}
    assert client.post("/quick-edit", json=body).json()["markdown"] == "# PM"
    assert client.post("/regenerate-section", json={"current_draft": DRAFT, "section": "requirements"}).status_code == 200


def test_unknown_action_or_section_rejected(client):
    assert client.post("/quick-edit", json={"current_draft": DRAFT, "action": "hack"}).status_code == 422
    assert client.post("/regenerate-section", json={"current_draft": DRAFT, "section": "title"}).status_code == 422


def test_quality_endpoint_is_free_and_needs_no_llm(client):
    response = client.post("/quality", json={"draft": DRAFT, "job_info": {"jurisdiction": "US-CA"}})
    codes = {f["code"] for f in response.json()["findings"]}
    assert response.status_code == 200 and "pay_missing" in codes
    severity = next(f for f in response.json()["findings"] if f["code"] == "pay_missing")["severity"]
    assert severity == "error"


def test_config_lists_packs_and_free_grant(client):
    config = client.get("/config").json()
    assert config["free_signup_credits"] == 20
    assert [(p["price_cents"], p["credits"]) for p in config["packs"]] == [(500, 20), (1000, 40), (2000, 80)]
    assert any(j["code"] == "US-CA" for j in config["jurisdictions"])


def test_upload_is_free_for_guests_and_size_capped(client, monkeypatch):
    monkeypatch.setattr(jobs, "extract_job_info_from_doc", lambda b, n: {"data": {"role_title": "PM"}, "original_text": "t"})
    ok = client.post("/api/extract-doc", files={"file": ("jd.txt", b"hello")})
    assert ok.status_code == 200 and ok.json()["data"] == {"role_title": "PM"}
    big = client.post("/api/extract-doc", files={"file": ("jd.txt", b"x" * (services.MAX_UPLOAD_BYTES + 5))})
    assert big.status_code == 400
    bad = client.post("/api/extract-doc", files={"file": ("virus.exe", b"x")})
    assert bad.status_code == 400


def test_extracted_data_is_cleaned():
    cleaned = services._clean_extracted({
        "role_title": "PM", "evil_key": "x", "pay_min": -5, "pay_max": 100,
        "requirements": ["a"] * 100, "company_name": 5,
    })
    assert cleaned["role_title"] == "PM" and "evil_key" not in cleaned
    assert "pay_min" not in cleaned and cleaned["pay_max"] == 100
    assert len(cleaned["requirements"]) == 30 and "company_name" not in cleaned


# --- cache -----------------------------------------------------------------

def test_identical_generate_requests_hit_the_cache(monkeypatch):
    calls = {"n": 0}

    class FakeAgent:
        def stream_generate_draft(self, **kwargs):
            calls["n"] += 1
            yield {"event": "done", "draft": DRAFT, "markdown": "# PM"}

    monkeypatch.setattr(services, "JobAgent", FakeAgent)
    request = services.GenerateRequest(job_info=services.JobInfo(company_name="Acme"))
    first = list(services.stream_generate_job_description(request))
    second = list(services.stream_generate_job_description(request))
    assert calls["n"] == 1
    assert second[0].get("cached") is True and "quality" in first[-1]


# --- payments ---------------------------------------------------------------

def paid_session(**overrides):
    session = {
        "id": "cs_1", "payment_status": "paid", "client_reference_id": "user-1",
        "amount_total": 500, "metadata": {"user_id": "user-1", "pack_id": "starter"},
    }
    session.update(overrides)
    return session


def test_packs_are_four_credits_per_dollar_and_no_one_dollar_pack():
    assert all(p.credits * 25 == p.price_cents for p in CREDIT_PACKS)
    assert min(p.price_cents for p in CREDIT_PACKS) == 500
    assert get_pack("nope") is None


def test_fulfill_grants_pack_credits_once_keyed_on_session(monkeypatch):
    grants = []
    monkeypatch.setattr(ledger, "grant", lambda uid, amount, key, reason: grants.append((uid, amount, key)) or 25)
    assert payments._fulfill_session(paid_session()) == 25
    assert grants == [("user-1", 20, "stripe:cs_1")]


@pytest.mark.parametrize("override", [
    {"payment_status": "unpaid"},
    {"amount_total": 100},
    {"metadata": {"user_id": "user-1", "pack_id": "bogus"}},
    {"client_reference_id": None, "metadata": {"pack_id": "starter"}},
])
def test_fulfill_ignores_unpaid_or_tampered_sessions(monkeypatch, override):
    monkeypatch.setattr(ledger, "grant", lambda *a: pytest.fail("must not grant"))
    assert payments._fulfill_session(paid_session(**override)) is None


def test_webhook_rejects_bad_signature(client):
    response = client.post("/webhook", content=b"{}", headers={"stripe-signature": "bad"})
    assert response.status_code == 400


def test_webhook_fulfills_then_records_event(client, monkeypatch):
    order = []
    event = {"id": "evt_1", "type": "checkout.session.completed", "data": {"object": paid_session()}}
    monkeypatch.setattr(payments.stripe.Webhook, "construct_event", lambda *a: event)
    monkeypatch.setattr(ledger, "grant", lambda *a: order.append("grant") or 1)
    monkeypatch.setattr(ledger, "claim_stripe_event", lambda event_id: order.append("claim") or True)
    assert client.post("/webhook", content=b"{}", headers={"stripe-signature": "x"}).json() == {"status": "success"}
    assert order == ["grant", "claim"]


def test_webhook_failure_returns_500_so_stripe_retries(client, monkeypatch):
    event = {"id": "evt_1", "type": "checkout.session.completed", "data": {"object": paid_session()}}
    monkeypatch.setattr(payments.stripe.Webhook, "construct_event", lambda *a: event)
    monkeypatch.setattr(ledger, "grant", lambda *a: (_ for _ in ()).throw(RuntimeError("db down")))
    claimed = []
    monkeypatch.setattr(ledger, "claim_stripe_event", lambda event_id: claimed.append(event_id))
    assert client.post("/webhook", content=b"{}", headers={"stripe-signature": "x"}).status_code == 500
    assert claimed == []


def test_confirm_checkout_rejects_other_users_session(client, monkeypatch):
    sign_in("someone-else")
    monkeypatch.setattr(payments.stripe.checkout.Session, "retrieve", lambda sid: paid_session())
    assert client.post("/confirm-checkout?session_id=cs_1").status_code == 400


def test_confirm_checkout_credits_owner(client, monkeypatch):
    sign_in("user-1")
    monkeypatch.setattr(payments.stripe.checkout.Session, "retrieve", lambda sid: paid_session())
    monkeypatch.setattr(ledger, "grant", lambda *a: 45)
    assert client.post("/confirm-checkout?session_id=cs_1").json() == {"credits": 45}


def test_checkout_uses_server_side_pack_and_safe_redirect(client, monkeypatch):
    sign_in("user-1")
    captured = {}

    class FakeSession:
        url = "https://stripe.test/pay"

    monkeypatch.setattr(payments.stripe.checkout.Session, "create", lambda **kw: captured.update(kw) or FakeSession())
    response = client.post("/create-checkout-session", json={"pack_id": "standard", "redirect_url": "https://evil.example.com"})
    assert response.json()["checkout_url"] == "https://stripe.test/pay"
    assert captured["line_items"][0]["price_data"]["unit_amount"] == 1000
    assert captured["client_reference_id"] == "user-1"
    assert captured["metadata"] == {"user_id": "user-1", "pack_id": "standard"}
    assert captured["success_url"].startswith("https://www.linkedingenai.com")
    assert client.post("/create-checkout-session", json={"pack_id": "free-money"}).status_code == 400


def test_checkout_requires_sign_in(client):
    assert client.post("/create-checkout-session", json={"pack_id": "starter"}).status_code == 401


def test_redirect_allowlist():
    assert is_allowed_redirect("https://www.linkedingenai.com/?x=1")
    assert is_allowed_redirect("http://localhost:7860/")
    assert is_allowed_redirect("https://someone-app.hf.space/")
    assert not is_allowed_redirect("https://linkedingenai.com.evil.com/")
    assert not is_allowed_redirect("javascript:alert(1)")
    assert not is_allowed_redirect("")


# --- ledger fallback ---------------------------------------------------------

def test_ledger_spend_returns_rpc_balance(monkeypatch):
    class Rpc:
        def __init__(self, data):
            self.data = data

        def execute(self):
            return self

    monkeypatch.setattr(ledger, "get_service_client", lambda: type("C", (), {"rpc": staticmethod(lambda name, params: Rpc(12))})())
    assert ledger.spend("u", 1, "k") == 12
    monkeypatch.setattr(ledger, "get_service_client", lambda: type("C", (), {"rpc": staticmethod(lambda name, params: Rpc(-1))})())
    assert ledger.spend("u", 1, "k") == ledger.INSUFFICIENT


# --- security helpers ---------------------------------------------------------

def test_normalize_email_collapses_aliases():
    assert normalize_email("John.Doe+promo@Gmail.com") == "johndoe@gmail.com"
    assert normalize_email("a.b@work.com") == "a.b@work.com"
    assert normalize_email("X+1@work.com") == "x@work.com"


def test_disposable_email_detection(monkeypatch):
    assert is_disposable("x@mailinator.com") and not is_disposable("x@gmail.com")
    monkeypatch.setenv("DISPOSABLE_EMAIL_DOMAINS", "spam.test")
    assert is_disposable("x@SPAM.test")


def test_signup_blocks_disposable_email(client):
    response = client.post("/auth/signup", json={"username": "u", "email": "a@mailinator.com", "password": "secret1"})
    assert response.status_code == 400


def make_request(headers, host="10.0.0.9"):
    from starlette.requests import Request

    scope = {
        "type": "http", "headers": [(k.lower().encode(), v.encode()) for k, v in headers.items()],
        "client": (host, 1234),
    }
    return Request(scope)


def test_client_ip_ignores_forged_left_side_of_forwarded_for(monkeypatch):
    monkeypatch.setattr(limits, "TRUSTED_PROXY_HOPS", 1)
    request = make_request({"x-forwarded-for": "6.6.6.6, 1.2.3.4"})
    assert limits.client_ip(request) == "1.2.3.4"
    assert limits.client_ip(make_request({})) == "10.0.0.9"
    monkeypatch.setattr(limits, "TRUSTED_PROXY_HOPS", 0)
    assert limits.client_ip(request) == "10.0.0.9"


def test_user_hourly_limit(monkeypatch):
    monkeypatch.setattr(limits, "USER_HOURLY_LIMIT", 2)
    limits.check_user_limit("u")
    limits.check_user_limit("u")
    with pytest.raises(Exception) as error:
        limits.check_user_limit("u")
    assert error.value.status_code == 429
    limits.check_user_limit("other")


def test_ledger_fails_closed_when_sql_functions_missing(monkeypatch):
    class Boom:
        def execute(self):
            raise RuntimeError("PGRST202 Could not find the function public.grant_credits")

    monkeypatch.setattr(ledger, "get_service_client", lambda: type("C", (), {"rpc": staticmethod(lambda name, params: Boom())})())
    with pytest.raises(ledger.LedgerNotInstalled):
        ledger.grant("u", 5, "k", "purchase")
    with pytest.raises(ledger.LedgerNotInstalled):
        ledger.refund("u", 1, "k")
    with pytest.raises(ledger.LedgerNotInstalled):
        ledger.claim_free_grant("u", "a@b.com", 20)
    with pytest.raises(ledger.LedgerNotInstalled):
        ledger.spend("u", 1, "k")


def test_webhook_returns_500_not_double_credit_when_ledger_missing(client, monkeypatch):
    event = {"id": "evt_1", "type": "checkout.session.completed", "data": {"object": paid_session()}}
    monkeypatch.setattr(payments.stripe.Webhook, "construct_event", lambda *a: event)

    class Boom:
        def execute(self):
            raise RuntimeError("PGRST202 Could not find the function")

    monkeypatch.setattr(ledger, "get_service_client", lambda: type("C", (), {"rpc": staticmethod(lambda name, params: Boom())})())
    assert client.post("/webhook", content=b"{}", headers={"stripe-signature": "x"}).status_code == 500


def test_disconnect_after_receiving_text_is_not_refunded(monkeypatch):
    refunds = []
    monkeypatch.setattr(ledger, "refund", lambda *a: refunds.append(a) or 0)

    def chunks(request):
        yield {"event": "chunk", "data": "paid draft text"}
        yield {"event": "chunk", "data": "more"}

    monkeypatch.setattr(jobs, "stream_refine_job_description", chunks)
    stream = jobs._refine_event_stream(None, "user-1", "key", 3)
    next(stream)
    stream.close()
    assert refunds == []


def test_disconnect_before_any_text_is_refunded(monkeypatch):
    refunds = []
    monkeypatch.setattr(ledger, "refund", lambda *a: refunds.append(a) or 0)

    def slow(request):
        yield {"event": "status"}
        yield {"event": "chunk", "data": "x"}

    monkeypatch.setattr(jobs, "stream_refine_job_description", slow)
    stream = jobs._refine_event_stream(None, "user-1", "key", 3)
    next(stream)
    stream.close()
    assert len(refunds) == 1


def test_ledger_fails_closed_without_service_key(monkeypatch):
    monkeypatch.delenv("SUPABASE_SERVICE_ROLE_KEY", raising=False)
    monkeypatch.setattr("src.database.supabase_client._service_client", None)
    with pytest.raises(RuntimeError):
        ledger.grant("u", 5, "k", "purchase")
