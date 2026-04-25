from fastapi import APIRouter, Header, Depends, HTTPException
from typing import Optional, List, Dict, Any
from app.services.database import get_sesiones_collection


router = APIRouter(prefix="/api/Intereses", tags=["Intereses"])


async def get_session(authorization: Optional[str] = Header(None)):
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:]
        from app.services.database import get_sesiones_collection
        sesiones = get_sesiones_collection()
        session = sesiones.find_one({"token": token})
        if session:
            return session
    raise HTTPException(status_code=401, detail="No autorizado")


@router.get("/Listado", response_model=List[Dict[str, Any]])
async def list_intereses(session: dict = Depends(get_session)):
    from app.services.innovasoft import innovasoft_service
    try:
        token = session.get("token")
        client = await innovasoft_service._get_client()
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get("/api/Intereses/Listado", headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return []