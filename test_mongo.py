import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def probar_conexion():
    uri = "mongodb+srv://admin:L3xy5931026@innovasofpythonpruebate.mnxjcdo.mongodb.net/?retryWrites=true&w=majority&appName=innovasofpythonpruebatecnica"
    
    client = AsyncIOMotorClient(uri, tlsAllowInvalidCertificates=True)
    try:
        info = await client.server_info()
        print("Conexion exitosa a MongoDB Atlas!")
        print(f"Version: {info.get('version')}")
    except Exception as e:
        print(f"Error: {e}")
        print("Verifica que el clusterNO este pausado en Atlas")

if __name__ == "__main__":
    asyncio.run(probar_conexion())