from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class Sexo(str, Enum):
    pass


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=1)


class LoginResponse(BaseModel):
    token: str
    userid: str
    username: str


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)


class RegistroResponse(BaseModel):
    status: str
    message: Optional[str] = None


class ClienteBase(BaseModel):
    
    nombre: str = Field(..., min_length=1, max_length=100)
    apellidos: str = Field(..., min_length=1, max_length=150)
    identificacion: str = Field(..., min_length=5, max_length=20)
    celular: Optional[str] = Field(None, max_length=20)
    telefono_otros: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    fecha_afiliacion: Optional[str] = None
    sexo: Optional[str] = None
    resena_personal: Optional[str] = None
    intereses: Optional[List[str]] = None


class ClienteCreate(BaseModel):
    nombre: str


class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    apellidos: Optional[str] = Field(None, min_length=1, max_length=150)
    identificacion: Optional[str] = Field(None, min_length=5, max_length=20)
    celular: Optional[str] = Field(None, max_length=20)
    telefono_otros: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    fecha_afiliacion: Optional[str] = None
    sexo: Optional[str] = None
    resena_personal: Optional[str] = None
    intereses: Optional[List[str]] = None


class ClienteResponse(ClienteBase):
    id: Optional[str] = None
    imagen: Optional[str] = None
    fecha_afiliacion: Optional[str] = None
    
    class Config:
        from_attributes = True


class ClienteListadoRequest(BaseModel):
    identificacion: str = ""
    nombre: str = ""
    usuarioId: str