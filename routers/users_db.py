#Importamos librerías
'''
APIRouter: método de fastapi que nos proporciona la capacidad de routear desde main a las otras APIs

HTTPException: Método de fastapi que nos permite generar excepciones para el servidor

pydantic: Librería para poder generar BaseModel, y crear objetos JSON a partir de una clase y usarlos en el código

'''
from fastapi import APIRouter, HTTPException 
from bd.models.user import User,User2
from bd.client import db_client
from bd.schemas.user import user_schema, users_schema
from bson import ObjectId
#El tag nos sirve para en la documentación: URL/docs nos genere una división con sus accesos
router = APIRouter(prefix = "/userdb",tags=["UsersDB"])


#Lista de users, (simula base de datos)
users_list = []

@router.get("/", response_model=list)
async def users():
    return users_schema(db_client.users.find())

@router.get("/{id}",response_model=User2)

async def user(id:str):
    user = search_user("_id",ObjectId(id))
    if type(user) == User2:
        return user
    else:
        raise HTTPException(status_code=400, detail="That user is not exist")


@router.post("/",status_code=201, response_model=User2) 
async def add_user(user: User):
    if type(search_user("email",user.email))==User:
        raise HTTPException(404,"That user is already exists")
    
    user_dict = dict(user)
    
    #Insertar un registro en mongo db
    id = db_client.users.insert_one(user_dict).inserted_id #Este a su vez lo crea y devuelve su id
    #Buscamos un registro por su id

    #User_schema es una función en la que podremos manipular los campos del registro que nos devuelve mongodb
    n_user = user_schema(db_client.users.find_one({"_id":id}))
    return User2(**n_user)  
    
@router.put("/",response_model=User2,status_code=202)
async def update_user(user:User2):
    user_dict = dict(user)
    del user_dict["id"]
    try:
        db_client.users.find_one_and_replace({"_id":ObjectId(user.id)}, user_dict)
    except:
        raise HTTPException(status_code=400, detail="Thath user is not exist")
    return search_user("_id",ObjectId(user.id))
@router.delete("/{id}",status_code=204)
async def delete_user(id:str):
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        raise HTTPException(status_code=204)

#Importante mencionar, que para que el servidor devuelva una excepción o error utilizamos "raise" en ves de "return"
            
#Función para buscar usuario existe por campo y valor
def search_user(key:str, value):
    try:
       user = user_schema(db_client.users.find_one({key:value}))
       return User2(**user)
    except:
        #raise HTTPException(status_code=404,detail="That user is not exist")
        return None



