from jose import jwt, JWTError
from datetime import datetime, timedelta

# FOR JWT TOKEN
SECRECT_KEY = "fastAPI_secret"
ALGORITHM = "HS256"
EXPIRY_TIME = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRY_TIME)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRECT_KEY, algorithm=ALGORITHM)
    return encoded_jwt
