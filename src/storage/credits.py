import json
from pathlib import Path
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path

DB_FILE = Path ("data/credits.json")

def _load_db():
    if not DB_FILE.exists():
        DB_FILE.parent.mkdir (parents = True, exist_ok=True)
        DB_FILE.write_text("{}")
    return json.loads (DB_FILE.read_text())

def _save_db(data: dict):
    DB_FILE.write_text(json.dumps (data, indent = 2))

#get the time of us
def get_current_us_month():
    us_time = datetime.now (ZoneInfo("America/New_York"))
    return us_time.strftime("%Y-%m")

#return the user user account from the database
def get_user_account (user_id: str):
    db = _load_db()
    current_month = get_current_us_month()

    account = db.get(user_id, {
        "free_credits": 10,
        "purchased_credits": 0,
        "last_reset_month": current_month,
    })

    #Check if 1 month has passed to reset the free credits
    if account.get ("last_reset_month") != current_month:
        account["free_credits"] = 10
        account["last_reset_month"] = current_month
        db[user_id] = account
        _save_db(db)

    return account


def deduct_user_credit (user_id: str):
    db = _load_db()
    account = get_user_account(user_id)

    if account['free_credits'] > 0:
        account['free_credits'] -= 1
    elif account['purchased_credits'] > 0:
        account['purchased_credits'] -= 1
    else:
        return False #out of credits

    #Update number of credits to database.
    db[user_id] = account
    _save_db(db)
    return True

#This function is to return the user's credtis
def get_user_credits (user_id: str):
    account = get_user_account(user_id)
    return account.get("free_credits", 0) + account.get("purchased_credits", 0)

#This function is to add the free and purchased credits
def add_user_credits (user_id: str, amount: int):
    db = _load_db()
    account = get_user_account(user_id)
    account["purchased_credits"] = account.get("purchased_credits", 0) + amount
    db[user_id] = account
    _save_db(db)
