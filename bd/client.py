from pymongo import MongoClient
#Base de datos local
#db_client = MongoClient().local

#Base de datos remota

db_client = MongoClient("mongodb+srv://stevendevprz:holamundo123@cluster0.ci5jdhj.mongodb.net/?retryWrites=true&w=majority").test