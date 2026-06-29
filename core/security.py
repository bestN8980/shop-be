from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import hashlib

from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# bcrypt context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _prehash(password: str) -> str:
    """
    Convert password -> sha256 hash (always <= 64 chars)
    Fix bcrypt 72-byte limit
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def hash_password(password: str) -> str:
    hashed = _prehash(password)
    return pwd_context.hash(hashed)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    hashed = _prehash(plain_password)
    return pwd_context.verify(hashed, hashed_password)
# JWT

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None