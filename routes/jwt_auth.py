from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext
from jwt.exceptions import InvalidTokenError



ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
SECRET_KEY = "kmbftgdvnkJhgbnjkhGghH85564564456dfgv45fgvhKNBJbtbftfybugbuy8546"



router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")
crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")



class User(BaseModel):
    username: str
    name: str
    email: str
    disable: bool
    
class UserDB(User):
    password: str

users_db = {
    "pablo": {
        "username" : "pablo",
        "name": "pablo",
        "email": "pablo@pablo.com",
        "disable": False,
        "password": "$2a$12$1zx.X7IfA6DMuD.nngXRhOwQX9gIEWB8bYoSm0bBgqBICZk6RO6Aq"
    },

    "admin": {
        "username" : "admin",
        "name": "admin",
        "email": "admin@admin.com",
        "disable": True,
        "password": "$2a$12$lI93Y6KoMEgG3EwRF6tOPeuvUYHKmKt5bJIAQRSainWGugRfuW47m"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
async def auth_user(token: str = Depends(oauth2)):
    
    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación inválidas",
            headers={"WWW-Authenticate": "Bearer"})
    
    try:
        username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
        
    except InvalidTokenError:
        raise exception
    
    return search_user(username)
    
    
    


async def current_user(user: User = Depends(auth_user)):
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")
        
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")

    user = search_user_db(form.username)
    
    
    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
        
            
    
    access_token = {
        "sub": user.username, 
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)}


    return {"access_token": jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM), "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user