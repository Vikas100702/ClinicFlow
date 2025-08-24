from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)

    return encode_jwt


def decode_access_token(token: str) -> str:
    """JWT verify + Decode"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm = [ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token Expires")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid Token")