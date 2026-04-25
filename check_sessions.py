import certifi
from pymongo import MongoClient

uri = "mongodb+srv://admin:L3xy5931026@innovasofpythonpruebate.mnxjcdo.mongodb.net/?retryWrites=true&w=majority&appName=innovasofpythonpruebatecnica"
client = MongoClient(uri, tlsCAFile=certifi.where())

db = client["innovasoft_api"]
sesiones = db["sesiones"].find()
for s in sesiones:
    print(f"Usuario: {s.get('username')}, Token: {s.get('token')[:50]}...")