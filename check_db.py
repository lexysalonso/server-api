import certifi
from pymongo import MongoClient

uri = "mongodb+srv://admin:L3xy5931026@innovasofpythonpruebate.mnxjcdo.mongodb.net/?retryWrites=true&w=majority&appName=innovasofpythonpruebatecnica"
client = MongoClient(uri, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=5000)

db = client["innovasofpythonpruebatecnica"]

print("=== COLECCIONES EN MONGODB ATLAS ===")
for col in db.list_collection_names():
    print(f"- {col}")

print("\n=== SESIONES ===")
sesiones = list(db["sesiones"].find().limit(3))
for s in sesiones:
    print(f"Usuario: {s.get('username')}")
    print(f"UserID: {s.get('userid')}")
    print(f"Login: {s.get('login_timestamp')}")
    print("---")

print("\n=== OPERACIONES ===")
operaciones = list(db["operaciones"].find().limit(5))
for o in operaciones:
    print(f"Acción: {o.get('accion')}")
    print(f"Usuario: {o.get('usuario')}")
    print(f"Cliente ID: {o.get('cliente_id')}")
    print(f"Resultado: {o.get('resultado')}")
    print(f"Timestamp: {o.get('timestamp')}")
    print("---")

print("\n=== TOTAL ===")
print(f"Sesiones: {db['sesiones'].count_documents({})}")
print(f"Operaciones: {db['operaciones'].count_documents({})}")