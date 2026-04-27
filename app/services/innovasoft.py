import httpx
from typing import Optional, Dict, Any
from app.config import get_innovasoft_url, get_innovasoft_timeout
from app.models.schemas import (
    LoginRequest,
    RegisterRequest,
    ClienteCreate,
    ClienteUpdate,
    ClienteListadoRequest,
)
import logging

logger = logging.getLogger(__name__)

_client: Optional[httpx.AsyncClient] = None


async def get_http_client() -> httpx.AsyncClient:
    global _client
    if _client is None:
        _client = httpx.AsyncClient(
            base_url=get_innovasoft_url(),
            timeout=get_innovasoft_timeout(),
            follow_redirects=True,
        )
    return _client


async def get_client() -> httpx.AsyncClient:
    return await get_http_client()


async def close_http_client():
    global _client
    if _client:
        await _client.aclose()
        _client = None


class InnovasoftService:
    def __init__(self):
        self.base_url = get_innovasoft_url()
    
    async def _get_client(self):
        return await get_http_client()
    
    async def login(self, username: str, password: str) -> Dict[str, Any]:
        client = await get_http_client()
        payload = {"username": username, "password": password}
        response = await client.post("/api/Authenticate/login", json=payload)
        response.raise_for_status()
        return response.json()
    
    async def register(self, username: str, email: str, password: str) -> Dict[str, Any]:
        client = await get_http_client()
        payload = {"username": username, "email": email, "password": password}
        response = await client.post("/api/Authenticate/register", json=payload)
        response.raise_for_status()
        return response.json()
    
    async def get_cliente(self, cliente_id: str, token: str) -> Dict[str, Any]:
        client = await get_http_client()
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get(f"/api/Cliente/Obtener/{cliente_id}", headers=headers)
        response.raise_for_status()
        return response.json()
    
    async def list_clientes(
        self, identificacion: str, nombre: str, usuario_id: str, token: str
    ) -> Dict[str, Any]:
        client = await get_http_client()
        headers = {"Authorization": f"Bearer {token}"}
        payload = {
            "identificacion": identificacion,
            "nombre": nombre,
            "usuarioId": usuario_id,
        }
        response = await client.post("/api/Cliente/Listado", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    
    async def create_cliente(self, cliente: dict, token: str) -> Dict[str, Any]:
        client = await get_http_client()
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.post("/api/Cliente/Crear", json=cliente, headers=headers)
        if response.status_code == 204 or not response.text:
            return {"success": True, "message": "Cliente creado exitosamente"}
        response.raise_for_status()
        return response.json()
    
    async def update_cliente(self, cliente_id: str, cliente: dict, token: str) -> Dict[str, Any]:
        client = await get_http_client()
        headers = {"Authorization": f"Bearer {token}"}
        payload = {**cliente, "id": cliente_id}
        
        try:
            response = await client.post("/api/Cliente/Actualizar", json=payload, headers=headers)
        except Exception:
            response = await client.put(f"/api/Cliente/Actualizar/{cliente_id}", json=cliente, headers=headers)
        
        if response.status_code in [204, 200] or not response.text:
            return {"success": True, "message": "Cliente actualizado exitosamente"}
        try:
            return response.json()
        except:
            return {"success": True}
    
    async def delete_cliente(self, cliente_id: str, token: str) -> Dict[str, Any]:
        client = await get_http_client()
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"id": cliente_id}
        
        try:
            response = await client.post("/api/Cliente/Eliminar", json=payload, headers=headers)
            response.raise_for_status()
        except Exception:
            response = await client.delete(f"/api/Cliente/Eliminar/{cliente_id}", headers=headers)
            response.raise_for_status()
        
        if response.status_code in [204, 200] or not response.text:
            return {"success": True, "message": "Cliente eliminado exitosamente"}
        try:
            return response.json()
        except:
            return {"success": True}


innovasoft_service = InnovasoftService()