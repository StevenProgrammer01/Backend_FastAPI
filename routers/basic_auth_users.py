from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

#OAuth2PasswordBearer: Se va a encargar de gestionar la autenticación (user,password)
#OAuth2PasswordRequestForm: Método por donde enviaremos los datos de autenticación desde el cliente
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
router = APIRouter(prefix = "/login",tags=["Basic_auth"])

#Instaciamos la primer clase, y le pasamos de parámetro el nombre de la url que se va encargar de la authenticación
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
        "password":"holamundo123"
    },
    "stevendev2":{
        "username":"stevendev2",
        "fullname":"Steven Pérez 2",
        "email":"steven.dev.prz2@gmail.com",
        "disable":True,
        "password":"020905spa"
    }

}
#Función para verificar usuario
def search_user_db(username:str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username:str):
    if username in users_db:
        return User(**users_db[username])
    

#criterio de dependencia
#Depende de oauth
async def current_user(token:str=Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=401,detail="No Authorized access",headers={
            "WWW-Authenticate":"Bearer"
        })
    if user.disable:
         raise HTTPException(status_code=400,detail="Disabled User")
    return user

#Función para revisar si el usuario se encuentra en base de datos
@router.post("/")
async def login(form:OAuth2PasswordRequestForm = Depends()):#Depends() depende de la función misma de OAuth2PRF 
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=400, 
            detail="The username is not correct"
        )
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=400, detail = "The password is not correct")
    else:
        return{
            "access_token":user.username,
            "token_type":"bearer"
        }

#Función que devuelve información del usuario y depende de la función current_user
@router.get("/users/me")
async def me(user:User=Depends(current_user)):
    return user
