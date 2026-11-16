"""Pay-transparency rules by jurisdiction.

Summary for a UI hint only. This is NOT legal advice: laws change, have
employer-size thresholds and exceptions. Verify with counsel.
Sources: state and provincial labour agencies, law-firm summaries, and the
EU Pay Transparency Directive (2023/970, transposition deadline 7 June 2026;
many member states are late, so national rules vary).
"""

from pydantic import BaseModel


class Jurisdiction(BaseModel):
    """A pay-transparency jurisdiction.

    Attributes:
        code: Stable id used in requests.
        label: Name shown to users.
        pay_required: Whether a pay range is generally required in the ad.
        note: Short explanation shown beside the field.
    """

    code: str
    label: str
    pay_required: bool
    note: str


JURISDICTIONS = [
    Jurisdiction(code="none", label="Other / not listed", pay_required=False,
                 note="No known pay-range rule. Adding pay still gets more applicants."),
    Jurisdiction(code="US-CA", label="California, US", pay_required=True,
                 note="Employers with 15+ staff must include the pay scale."),
    Jurisdiction(code="US-CO", label="Colorado, US", pay_required=True,
                 note="Pay range and benefits notice required in the posting."),
    Jurisdiction(code="US-WA", label="Washington, US", pay_required=True,
                 note="Employers with 15+ staff must list wage scale and benefits."),
    Jurisdiction(code="US-NY", label="New York State, US", pay_required=True,
                 note="Employers with 4+ staff must include the pay range."),
    Jurisdiction(code="US-NYC", label="New York City, US", pay_required=True,
                 note="Minimum and maximum pay required in the posting."),
    Jurisdiction(code="US-VA", label="Virginia, US", pay_required=True,
                 note="Pay range requirement in effect from 1 July 2026."),
    Jurisdiction(code="CA-ON", label="Ontario, Canada", pay_required=True,
                 note="Expected pay or range required in public postings (from 2026)."),
    Jurisdiction(code="CA-BC", label="British Columbia, Canada", pay_required=True,
                 note="Expected pay or range required in every posting."),
    Jurisdiction(code="EU", label="European Union", pay_required=True,
                 note="Directive 2023/970: pay or range in the ad or before the interview. National rules vary."),
]

_BY_CODE = {item.code: item for item in JURISDICTIONS}


def get_jurisdiction(code: str) -> Jurisdiction:
    """Returns the jurisdiction for a code, or the "none" entry if unknown."""
    return _BY_CODE.get(code, _BY_CODE["none"])


def pay_required_for(code: str) -> bool:
    """Whether the jurisdiction generally requires a pay range."""
    return get_jurisdiction(code).pay_required
