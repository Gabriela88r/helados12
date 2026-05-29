from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["heladeria"]

productos = db["productos"]
pedidos = db["pedidos"]
contactos = db["contactos"]  
