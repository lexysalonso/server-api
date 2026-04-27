from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
import logging

from app.routers import authenticate, clientes, intereses
from app.services.database import close_connection
from app.services.innovasoft import close_http_client
from app.config import get_app_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando API...")
    yield
    logger.info("Cerrando API...")
    await close_http_client()
    close_connection()


app = FastAPI(
    title="Innovasoft API Local",
    description="API Local para gestión de clientes - consume API Innovasoft",
    version="1.0.0",
    lifespan=lifespan,
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Innovasoft API Local",
        version="1.0.0",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "description": 'JWT Authorization header using the Bearer scheme. Example: "Bearer {token}"'
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if method in ["get", "post", "put", "delete"]:
                openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authenticate.router, prefix="/api/Authenticate")
app.include_router(clientes.router, prefix="/api/Cliente")
app.include_router(intereses.router, prefix="/api/Intereses")


@app.get("/")
async def root():
    return {"message": "Innovasoft API Local", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    
    config = get_app_config()
    uvicorn.run(
        "main:app",
        host=config.get("host", "0.0.0.0"),
        port=config.get("port", 8000),
        reload=True,
    )