"""Email rules used to stop free-credit farming."""

import os

# Common throwaway providers. Extend with the DISPOSABLE_EMAIL_DOMAINS env var
# (comma separated).
DISPOSABLE_DOMAINS = {
    "mailinator.com", "guerrillamail.com", "guerrillamail.net", "10minutemail.com",
    "10minutemail.net", "tempmail.com", "temp-mail.org", "temp-mail.io", "throwawaymail.com",
    "yopmail.com", "yopmail.net", "trashmail.com", "getnada.com", "nada.email",
    "sharklasers.com", "grr.la", "guerrillamailblock.com", "maildrop.cc", "dispostable.com",
    "fakeinbox.com", "mintemail.com", "mohmal.com", "mytemp.email", "tempail.com",
    "tempinbox.com", "emailondeck.com", "spamgourmet.com", "mailnesia.com", "moakt.com",
    "burnermail.io", "discard.email", "inboxkitten.com", "tmpmail.org", "tmpmail.net",
    "mail.tm", "1secmail.com", "1secmail.net", "1secmail.org", "dropmail.me",
    "emltmp.com", "luxusmail.org", "mailcatch.com", "anonbox.net", "spambox.us",
    "trbvm.com", "linshiyouxiang.net", "tempr.email", "harakirimail.com", "mailforspam.com",
}

# Providers that ignore dots in the local part.
DOT_INSENSITIVE_DOMAINS = {"gmail.com", "googlemail.com"}


def _extra_blocked() -> set[str]:
    """Reads extra blocked domains from the environment."""
    raw = os.getenv("DISPOSABLE_EMAIL_DOMAINS", "")
    return {item.strip().lower() for item in raw.split(",") if item.strip()}


def normalize_email(email: str) -> str:
    """Reduces an address to one canonical form per real mailbox.

    Lower-cases, removes `+tag` suffixes, and removes dots for Gmail.

    Args:
        email: Address as typed by the user.

    Returns:
        The canonical address, e.g. `John.Doe+x@gmail.com` -> `johndoe@gmail.com`.
    """
    clean = email.strip().lower()
    if "@" not in clean:
        return clean
    local, domain = clean.rsplit("@", 1)
    local = local.split("+", 1)[0]
    if domain in DOT_INSENSITIVE_DOMAINS:
        local = local.replace(".", "")
        domain = "gmail.com"
    return f"{local}@{domain}"


def is_disposable(email: str) -> bool:
    """Whether the address uses a known throwaway email provider."""
    clean = email.strip().lower()
    if "@" not in clean:
        return False
    domain = clean.rsplit("@", 1)[1]
    return domain in DISPOSABLE_DOMAINS or domain in _extra_blocked()
