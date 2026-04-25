import certifi
from pymongo import MongoClient

uri = "mongodb+srv://admin:L3xy5931026@innovasofpythonpruebate.mnxjcdo.mongodb.net/?retryWrites=true&w=majority&appName=innovasofpythonpruebatecnica"
client = MongoClient(uri, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=5000)

db = client["innovasofpythonpruebatecnica"]

print("Colecciones en la BD:")
for col in db.list_collection_names():
    print(f"  - {col}")

print("\n--- Sesiones ---")
sesiones = db["sesiones"].find()
for s in sesiones:
    print(f"  Usuario: {s.get('username')}, Login: {s.get('login_timestamp')}")

print("\n--- Operaciones ---")
operaciones = db["operaciones"].find()
for o in operaciones:
    print(f"  Accion: {o.get('accion')}, Usuario: {o.get('usuario')}, Cliente: {o.get('cliente_id')}")