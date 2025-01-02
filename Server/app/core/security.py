from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.core.config import settings
from typing import Union

# Initialize password context and secret key for JWT
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# Function to verify passwords
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Function to create JWT access token
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    to_encode = data.copy()

    # Ajoutez l'ID de l'utilisateur dans les données
    user_id = data.get("id")
    if not user_id:
        raise ValueError("User ID is required for token creation.")
    to_encode.update({"id": user_id})

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=1)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Function to verify JWT token
def verify_token(token: str) -> dict:
    try:
        # Décoder le token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Afficher le payload pour débogage
        print(f"Decoded Payload: {payload}")

        # Vérification de l'expiration (si nécessaire)
        if datetime.utcnow() > datetime.utcfromtimestamp(payload['exp']):
            raise HTTPException(status_code=401, detail="Token has expired")

        return payload
    except JWTError as e:
        print(f"JWT error: {str(e)}")
        raise HTTPException(status_code=401, detail=f"JWT error: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=401, detail=f"Error: {str(e)}")
