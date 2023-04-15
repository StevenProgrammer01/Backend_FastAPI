from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

#OAuth2PasswordBearer: Se va a encargar de gestionar la autenticación (user,password)
#OAuth2PasswordRequestForm: Método por donde enviaremos los datos de autenticación desde el cliente
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1 
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
#Contexto de encriptación: Que algoritmo vamos a usar 
crypt = CryptContext(schemes=["bcrypt"]) 


router = APIRouter(tags=["JWT_auth"])
oauth2 = OAuth2PasswordBearer(tokenUrl="login") 
class User(BaseModel):
    username:str
    fullname:str
    email:str
    disable:bool

#Clase heredada de User
class UserDB(User):
    password:str

users_db = {
    "stevendev":{
        "username":"stevendev",
        "fullname":"Steven Pérez",
        "email":"steven.dev.prz@gmail.com",
        "disable":False,
        "password":"$2a$12$eaYi0rJzqpkN4yhNCZgmtO.R4iUFo9P4FKZoDcWL0KA5/DIwiLeGy"
    },
    "stevendev2":{
        "username":"stevendev2",
        "fullname":"Steven Pérez 2",
        "email":"steven.dev.prz2@gmail.com",
        "disable":True,
        "password":"$2a$12$nFpYH75MM96tb8K5.V5W8.YmPMEn1pizNj/qjFkMMdExgGAu6pgdi"
    }

}
def search_user_db(username:str):
    if username in users_db:
        return UserDB(**users_db[username])
def search_user(username:str):
    if username in users_db:
        return User(**users_db[username])
    
#Función para buscar usuario autenticado
async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(status_code=401,detail="No Authorized access",headers={
            "WWW-Authenticate":"Bearer"
        })
    #Decodear token
    try:
        username = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM).get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception
    
    return search_user(username)
        
async def current_user(user:User=Depends(auth_user)):
    if user.disable:
         raise HTTPException(status_code=400,detail="Disabled User")
    return user

@router.post("/login")
async def login(form:OAuth2PasswordRequestForm = Depends()):#Depends() depende de la función misma de OAuth2PRF 
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=400, 
            detail="The username is not correct"
        )
    user = search_user_db(form.username)

    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_DURATION)
    access_token = {
        "sub":user.username,
        "exp":expire,

    }
    #Verificar si la contraseña está encriptada
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail = "The password is not correct")
    else:
        return{
            #Generar token con jwt le pasamos el token que queremos, SECRET(opcional), y el algoritmo a utilizar
            "access_token":jwt.encode(access_token,SECRET_KEY,algorithm=ALGORITHM),
            "token_type":"bearer"
        }
@router.get("/users/me")
async def me(user:User=Depends(current_user)):
    print(user)
    return user
