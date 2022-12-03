from passlib.context import CryptContext


psw_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
	return psw_context.hash(password)

def decode_password(password, hashed_password):
	return psw_context.verify(password, hashed_password)

