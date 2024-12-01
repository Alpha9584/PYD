import bcrypt

def encrypt_password(password: str) -> str:
    """Encrypt a password using bcrypt"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, stored_hash: str) -> bool:
    """Verify a plain password against stored hash"""
    try:
        password_bytes = plain_password.encode('utf-8')
        stored_hash_bytes = stored_hash.encode('utf-8')
        return bcrypt.checkpw(password_bytes, stored_hash_bytes)
    except (ValueError, TypeError):
        return False