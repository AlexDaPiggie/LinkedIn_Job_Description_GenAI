from passlib.context import CryptContext

pwd_context = CryptContext(
    schemas = ['bcrypt'],
    deprecated = 'auto'
)

# This function is to hash the password from the 'string' version
def hash_password (password: str):
    return pwd_context.hash (password)

# This function is to verify if the password is correct
def verify_password (plain_password: str, hashed_password):
    return pwd_context.verify (
        plain_password,
        hashed_password,
    )