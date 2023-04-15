#Importamos librerías
'''
APIRouter: método de fastapi que nos proporciona la capacidad de routear desde main a las otras APIs

HTTPException: Método de fastapi que nos permite generar excepciones para el servidor

pydantic: Librería para poder generar BaseModel, y crear objetos JSON a partir de una clase y usarlos en el código

'''
from fastapi import APIRouter, HTTPException 
from pydantic import BaseModel

#El tag nos sirve para en la documentación: URL/docs nos genere una división con sus accesos
router = APIRouter(tags=["Users"])


# Entidad User
# Pasamos BaseModel como parámetro para que recupere los parametros y los usemos en la clase
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

#Lista de users, (simula base de datos)
users_list = [
    #Parámetros para la clase User y crear nuestro JSON Object
    User(id = 1 , name = "Steven", surname = "Pérez", url = "https://steven.dev", age = 17),
    User(id = 2 ,name = "Maikel", surname = "Arguedas", url = "https://maikel.dev", age = 17),
    User(id = 3, name = "Samantha", surname = "Chacón", url = "https://samantha.ui", age = 18)]

#Url para mostrar todos los usuarios
#response_model: parámetro en el que se específica el tipo de dato a devolver en la ruta
@router.get("/users", response_model=list)
async def users():
    return users_list
#Url para buscar un único usuario
@router.get("/user/{id}",response_model=User)
#Recibe el dato por path
#Tambien podemos crear una que lo reciba por query : user/?id=1 pero no sería de uso obligatorio en la API
async def user(id:int):#Hay que especificar el tipo de dato
    user = search_user(id)
    if type(user) == User:
        return user
    else:
        raise HTTPException(status_code=400, detail="That user is not exist")

#Ruta para agregar un nuevo usuario con POST
#status code específicamos que código enviar al ejecutarse
@router.post("/user/",status_code=201, response_model=User) 
async def add_user(user: User):
    if type(search_user(user.id))!=User:
        users_list.append(user)
        return user
    else:
        raise HTTPException(404,"That user is already exists")
    
# Ruta para actualizar el usuario
@router.put("/user/",response_model=User,status_code=202)
async def update_user(user:User):
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            return users_list[index]

    else:
        raise HTTPException(status_code=400,detail="That user is not exist")
#Ruta para eliminar usuario
@router.delete("/user/{id}",response_model=User,status_code=202)
async def delete_user(id:int):
    for index, user in enumerate(users_list):
        if user.id == id:
            user_dropped = users_list.pop(index)
            return user_dropped
    else:
        raise HTTPException(status_code=400, detail="That user is not exist")
#Importante mencionar, que para que el servidor devuelva una excepción o error utilizamos "raise" en ves de "return"
        

        
    

    

#Función para buscar un usuario
def search_user(id:int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        pass



