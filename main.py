from fastapi import FastAPI

from routers import products, users,basic_auth_users,jwt_auth_users, users_db
app = FastAPI()

#Routers
app.include_router(products.router)
app.include_router(users.router)
#app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)

#app.get() indica desde donde accederemos al api
@app.get("/")
#async: asíncrono
async def root():
    return "Hola Mundo FASTAPI!!!"

# Si a nuestra url le agregamos /doct podremos ver nuestra documentación a tiempo real
# Tambien si usamos /redoc