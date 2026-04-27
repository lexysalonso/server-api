from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    token: str
    userid: str
    username: str


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class RegistroResponse(BaseModel):
    status: str
    message: Optional[str] = None


class ClienteBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    apellidos: str = Field(..., min_length=1, max_length=150)
    identificacion: str = Field(..., min_length=5, max_length=20)
    celular: Optional[str] = None
    telefono_otros: Optional[str] = None
    direccion: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    fecha_afiliacion: Optional[str] = None
    sexo: Optional[str] = None
    resena_personal: Optional[str] = None
    intereses: Optional[List[str]] = None


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    identificacion: Optional[str] = None
    celular: Optional[str] = None
    telefono_otros: Optional[str] = None
    direccion: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    fecha_afiliacion: Optional[str] = None
    sexo: Optional[str] = None
    resena_personal: Optional[str] = None
    intereses: Optional[List[str]] = None
    id: Optional[str] = None


class ClienteListadoRequest(BaseModel):
    identificacion: str = ""
    nombre: str = ""
    usuarioId: str