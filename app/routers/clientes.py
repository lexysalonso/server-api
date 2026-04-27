from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional
from datetime import datetime
from app.models.schemas import ClienteCreate, ClienteUpdate, ClienteListadoRequest
from app.services.innovasoft import innovasoft_service
from app.services.database import get_sesiones_collection, get_operaciones_collection

router = APIRouter(tags=["Clientes"])


def get_token_from_header(authorization: Optional[str] = Header(None)) -> Optional[str]:
    if authorization and authorization.startswith("Bearer "):
        return authorization[7:]
    return authorization


async def get_current_session(authorization: Optional[str] = Depends(get_token_from_header)):
    if not authorization:
        raise HTTPException(status_code=401, detail="No autorizado")
    
    sesiones = get_sesiones_collection()
    session = sesiones.find_one({"token": authorization})
    
    if not session:
        raise HTTPException(status_code=401, detail="Sesión inválida o expirada")
    
    return session


def registrar_operacion(accion: str, username: str, cliente_id: str, resultado: int):
    operaciones = get_operaciones_collection()
    operaciones.insert_one({
        "accion": accion,
        "usuario": username,
        "cliente_id": cliente_id,
        "timestamp": datetime.utcnow().isoformat(),
        "resultado": resultado,
    })


@router.post("/Listado")
async def listado_clientes(
    request: ClienteListadoRequest,
    session: dict = Depends(get_current_session)
):
    try:
        token = session.get("token")
        userid = session.get("userid")
        
        identificacion = request.identificacion if request.identificacion else ""
        nombre = request.nombre if request.nombre else ""
        usuarioId = request.usuarioId if request.usuarioId else userid
        
        clientes = await innovasoft_service.list_clientes(
            identificacion,
            nombre,
            usuarioId,
            token,
        )
        return clientes if isinstance(clientes, list) else []
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al listar clientes: {str(e)}")


@router.get("/Obtener/{cliente_id}")
async def get_cliente(cliente_id: str, session: dict = Depends(get_current_session)):
    try:
        token = session.get("token")
        username = session.get("username")
        cliente = await innovasoft_service.get_cliente(cliente_id, token)
        registrar_operacion("CONSULTAR", username, cliente_id, 200)
        return cliente
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/Crear")
async def create_cliente(cliente: ClienteCreate, session: dict = Depends(get_current_session)):
    try:
        token = session.get("token")
        username = session.get("username")
        result = await innovasoft_service.create_cliente(cliente.model_dump(exclude_none=True), token)
        cliente_id = result.get("id") or result.get("_id", "") or result.get("Id", "unknown")
        registrar_operacion("CREAR", username, cliente_id, 201)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/Actualizar")
async def update_cliente(
    request: ClienteUpdate,
    session: dict = Depends(get_current_session)
):
    try:
        cliente_id = request.id
        if not cliente_id:
            raise HTTPException(status_code=400, detail="ID de cliente requerido")
        
        token = session.get("token")
        username = session.get("username")
        
        payload = request.model_dump(exclude_none=True)
        payload["id"] = cliente_id
        
        result = await innovasoft_service.update_cliente(cliente_id, payload, token)
        
        registrar_operacion("ACTUALIZAR", username, cliente_id, 200)
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al actualizar: {str(e)}")


@router.delete("/Eliminar/{cliente_id}")
async def delete_cliente(
    cliente_id: str, 
    session: dict = Depends(get_current_session)
):
    try:
        token = session.get("token")
        username = session.get("username")
        await innovasoft_service.delete_cliente(cliente_id, token)
        registrar_operacion("ELIMINAR", username, cliente_id, 200)
        return {"message": "Cliente eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))