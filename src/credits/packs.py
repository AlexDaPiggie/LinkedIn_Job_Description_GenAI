"""Credit packs sold through Stripe Checkout and pricing constants."""

from pydantic import BaseModel

FREE_SIGNUP_CREDITS = 20
REFINE_COST = 1


class CreditPack(BaseModel):
    """A purchasable bundle of credits.

    Attributes:
        pack_id: Stable id sent by the front end.
        price_cents: Price in US cents.
        credits: Credits granted on payment.
    """

    pack_id: str
    price_cents: int
    credits: int


# 4 credits per dollar. $1 packs are not sold: Stripe takes about 33% of them.
CREDIT_PACKS = [
    CreditPack(pack_id="starter", price_cents=500, credits=20),
    CreditPack(pack_id="standard", price_cents=1000, credits=40),
    CreditPack(pack_id="pro", price_cents=2000, credits=80),
]

_BY_ID = {pack.pack_id: pack for pack in CREDIT_PACKS}


def get_pack(pack_id: str) -> CreditPack | None:
    """Returns the pack with the given id, or None."""
    return _BY_ID.get(pack_id)
