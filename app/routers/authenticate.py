from fastapi import APIRouter, HTTPException, Header, Depends
from typing import Optional
from datetime import datetime
from app.models.schemas import LoginRequest, LoginResponse, RegisterRequest, RegistroResponse
from app.services.innovasoft import innovasoft_service
from app.services.database import get_sesiones_collection

router = APIRouter(tags=["Autenticacion"])


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


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"Login attempt: {request.username}")
        response = await innovasoft_service.login(request.username, request.password)
        logger.info(f"Innovasoft response: {response}")
        
        token = response.get("token")
        userid = response.get("userid")
        username = response.get("username") or response.get("userName")
        logger.info(f"Parsed - token: {token}, userid: {userid}, username: {username}")
        
        if not token or not userid:
            logger.warning("Invalid credentials - no token or userid")
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        
        sesiones = get_sesiones_collection()
        sesiones.insert_one({
            "token": token,
            "userid": userid,
            "username": username,
            "login_timestamp": datetime.utcnow().isoformat(),
        })
        logger.info("Session saved to MongoDB")
        
        return LoginResponse(token=token, userid=userid, username=username)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=401, detail="Credenciales inválidas")


@router.post("/register", response_model=RegistroResponse)
async def register(request: RegisterRequest):
    try:
        response = await innovasoft_service.register(
            request.username, request.email, request.password
        )
        
        return RegistroResponse(
            status=response.get("status", "Success"),
            message=response.get("message", "Usuario registrado exitosamente")
        )
    
    except Exception as e:
        error_msg = str(e).lower()
        if "500" in error_msg or "internal" in error_msg:
            return RegistroResponse(
                status="Error",
                message="El usuario o correo ya existe. Intenta con otros datos."
            )
        if "password" in error_msg or "weak" in error_msg or "required" in error_msg or "invalid" in error_msg:
            return RegistroResponse(
                status="Error",
                message="La contraseña no cumple los requisitos."
            )
        return RegistroResponse(
            status="Error",
            message="Error al registrar. Verifica los datos."
        )


@router.post("/logout")
async def logout(authorization: Optional[str] = Header(None)):
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:]
        sesiones = get_sesiones_collection()
        result = sesiones.delete_many({"token": token})
        return {"message": "Sesión cerrada exitosamente"}
    
    return {"message": "No había sesión activa"}