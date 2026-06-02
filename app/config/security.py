# from datetime import datetime, timedelta, timezone
# import hashlib
# from jose import jwt
# from passlib.context import CryptContext

# from app.config.settings import settings

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def hash_password(password: str):
#     password = password[:72]
#     return pwd_context.hash(password)


# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)


# def create_access_token(data: dict) -> str:
#     to_encode = data.copy()
#     expire = datetime.now(timezone.utc) + timedelta(
#         minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
#     )
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# def token_fingerprint(token: str) -> str:
#     return hashlib.sha256(token.encode()).hexdigest()


from datetime import datetime, timedelta, timezone
import hashlib

from jose import jwt
from passlib.context import CryptContext

from app.config.settings import settings


# Password hashing context
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# Hash password
def hash_password(password: str) -> str:
    """
    Hash password using bcrypt.
    bcrypt supports maximum 72 bytes.
    """
    # Truncate to 72 bytes to satisfy bcrypt limits while preserving UTF-8
    pw_bytes = password.encode("utf-8")
    if len(pw_bytes) > 72:
        pw_bytes = pw_bytes[:72]
        password = pw_bytes.decode("utf-8", errors="ignore")

    return pwd_context.hash(password)


# Verify password
def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Verify hashed password.
    """
    # Apply the same byte-wise truncation as when hashing
    pw_bytes = plain_password.encode("utf-8")
    if len(pw_bytes) > 72:
        pw_bytes = pw_bytes[:72]
        plain_password = pw_bytes.decode("utf-8", errors="ignore")

    return pwd_context.verify(plain_password, hashed_password)


# Create JWT access token
def create_access_token(data: dict) -> str:
    """
    Generate JWT token.
    """
    to_encode = data.copy()

    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


# Generate token fingerprint
def token_fingerprint(token: str) -> str:
    """
    Generate SHA256 fingerprint for token.
    """
    return hashlib.sha256(
        token.encode()
    ).hexdigest()