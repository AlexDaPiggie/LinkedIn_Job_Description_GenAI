from sqlalchemy.orm import Session
from src.database.models import User
from src.storage.credits import get_current_us_month

# This function is to update the credits to the databasae
def deduct_user_db_credit (
    db: Session, user_id: int
): 
    user = db.query (User).filter(User.id == user_id).first()
    if not user:
        return False

    current_month = get_current_us_month()

    # Check to update the credits each month
    if user.last_reset_month != current_month:
        user.free_credits = 20
        user.last_reset_month = current_month
        db.commit()

    # Deduct priority is free credit first, then purchased
    if  user.free_credits > 0:
        user.free_credits -= 1
    elif user.purchased_credits > 0:
        user.purchased_credits -= 1
    else: 
        return False #Insufficient credits

    db.commit()
    return True