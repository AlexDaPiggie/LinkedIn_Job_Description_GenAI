import bcrypt 

#This function is to hash the password
def hash_password(password: str):
    password_bytes = password.encode ('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode ('utf-8')

#This function is to verify if the input pass matching any encoded pass in the db
def verify_password(
    plain_password: str,
    hashed_password: str,
):
    password_bytes = plain_password.encode ('utf-8')
    hashed_bytes = hashed_password.encode ('utf-8')
    try: 
        return bcrypt.checkpw (password_bytes, hashed_bytes)
    except Exception:
        return False