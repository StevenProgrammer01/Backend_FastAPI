from fastapi import APIRouter, HTTPException

#responses es un parámetro para gestionar el response en caso de errores
router = APIRouter(prefix="/products", responses={404:{"message":"Not Found"}}, tags = ["products"])

products_list = ["Product 1","Product 2","Product 3","Product 4","Product 5"]
@router.get("/")
async def products():
    try:
        return products_list
    except:
        raise HTTPException(404, detail="Not Found")
@router.get("/{id}")
async def products(id:int):
    try:
        return products_list[id]
    except:
        raise HTTPException(404, detail="Not Found")