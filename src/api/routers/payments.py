"""Stripe checkout, webhook and credit-balance endpoints."""

import os
import traceback
from urllib.parse import urlparse

import stripe
from fastapi import APIRouter, Depends, Header, HTTPException, Request

from src.api.config import is_allowed_redirect
from src.api.dependencies import get_user_id_from_auth
from src.api.schemas import CheckoutRequest
from src.credits import ledger
from src.credits.packs import get_pack
from src.database.supabase_credits import get_supabase_credits

router = APIRouter()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

DEFAULT_REDIRECT_URL = "https://www.linkedingenai.com"


def _fulfill_session(checkout_session) -> int | None:
    """Grants the credits for a paid Checkout Session, once.

    The pack and user come from metadata the server set when it created the
    session, and the paid amount must match the pack price. The grant key is
    the session id, so the webhook and the success page can both call this
    without double-crediting.

    Args:
        checkout_session: Stripe Checkout Session object or dict.

    Returns:
        The new balance, or None if the session is not a paid credit pack.
    """
    get = checkout_session.get if isinstance(checkout_session, dict) else lambda k, d=None: getattr(checkout_session, k, d)
    if get("payment_status") != "paid":
        return None
    metadata = get("metadata") or {}
    user_id = get("client_reference_id") or metadata.get("user_id")
    pack = get_pack(metadata.get("pack_id", ""))
    if not user_id or pack is None or get("amount_total") != pack.price_cents:
        return None
    return ledger.grant(user_id, pack.credits, f"stripe:{get('id')}", "purchase")


@router.post("/create-checkout-session")
def create_checkout_session(
    payload: CheckoutRequest,
    user_id: str = Depends(get_user_id_from_auth),
):
    """Creates a Stripe Checkout session for a credit pack.

    Args:
        payload: The pack to buy and where to return to afterwards.
        user_id: ID of the signed-in user (from the access token).

    Returns:
        A dict with the `checkout_url` to redirect the user to.

    Raises:
        HTTPException: 400 for an unknown pack or if Stripe fails.
    """
    pack = get_pack(payload.pack_id)
    if pack is None:
        raise HTTPException(status_code=400, detail="Unknown credit pack")

    redirect_url = payload.redirect_url if is_allowed_redirect(payload.redirect_url) else DEFAULT_REDIRECT_URL
    separator = "&" if urlparse(redirect_url).query else "?"
    success_url = f"{redirect_url}{separator}session_id={{CHECKOUT_SESSION_ID}}"

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": f"{pack.credits} refine credits",
                        "description": "Each credit pays for one refine request. Generating a job description is free.",
                    },
                    "unit_amount": pack.price_cents,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=success_url,
            cancel_url=redirect_url,
            client_reference_id=user_id,
            metadata={"user_id": user_id, "pack_id": pack.pack_id},
        )
        return {"checkout_url": checkout_session.url}
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.post("/confirm-checkout")
def confirm_checkout(
    session_id: str,
    user_id: str = Depends(get_user_id_from_auth),
):
    """Grants credits right after payment, without waiting for the webhook.

    Safe to call more than once: crediting is keyed on the session id.

    Args:
        session_id: Checkout Session id from the success URL.
        user_id: ID of the signed-in user.

    Returns:
        `{"credits": balance}`.

    Raises:
        HTTPException: 400 if the session is unknown, unpaid, or belongs
            to another user.
    """
    try:
        checkout_session = stripe.checkout.Session.retrieve(session_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Unknown checkout session")
    if checkout_session.get("client_reference_id") != user_id:
        raise HTTPException(status_code=400, detail="Unknown checkout session")
    balance = _fulfill_session(checkout_session)
    if balance is None:
        raise HTTPException(status_code=400, detail="Payment not completed")
    return {"credits": balance}


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None),
):
    """Receives Stripe events and grants credits for completed payments.

    Stripe delivers events at least once. Crediting is idempotent, and each
    handled event id is recorded for auditing.

    Args:
        request: Incoming request carrying the raw event payload.
        stripe_signature: Signature header used to authenticate the event.

    Returns:
        `{"status": "success"}` once the event is handled.

    Raises:
        HTTPException: 400 on a bad signature, 500 if granting credits fails
            (Stripe then retries).
    """
    payload = await request.body()
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    try:
        event = stripe.Webhook.construct_event(payload, stripe_signature, webhook_secret)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid webhook signature")

    if event["type"] not in ("checkout.session.completed", "checkout.session.async_payment_succeeded"):
        return {"status": "ignored"}

    try:
        # Crediting is keyed on the session id, so repeats never double-credit.
        # The event id is recorded only after crediting succeeded, so a failed
        # attempt is retried by Stripe instead of being skipped as a duplicate.
        _fulfill_session(event["data"]["object"])
        ledger.claim_stripe_event(event["id"])
    except Exception as error:
        print("Error processing webhook credits:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(error))

    return {"status": "success"}


@router.get("/credits")
def check_credits(user_id: str = Depends(get_user_id_from_auth)):
    """Returns the credit balance of the signed-in user."""
    return {"user_id": user_id, "credits": get_supabase_credits(user_id)}
