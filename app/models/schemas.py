from pydantic import BaseModel, Field
from typing import Optional, List


class LoginRequest(BaseModel):
    username: str = Field(description="Nombre de usuario")
    password: str = Field(description="Contraseña")


class LoginResponse(BaseModel):
    token: str
    userid: str
    username: str


class RegisterRequest(BaseModel):
    username: str = Field(description="Nombre de usuario")
    email: str = Field(description="Correo electrónico")
    password: str = Field(description="Contraseña")


class RegistroResponse(BaseModel):
    status: str
    message: Optional[str] = None


class ClienteCreate(BaseModel):
    model_config = {"json_schema_extra": {
        "examples": [{
            "nombre": "Juan",
            "apellidos": "Pérez Gómez",
            "identificacion": "12345678901",
            "celular": "88888888",
            "otroTelefono": "99999999",
            "direccion": "San José, Costa Rica",
            "fNacimiento": "1990-01-01T00:00:00.000Z",
            "fAfiliacion": "2024-01-01T00:00:00.000Z",
            "sexo": "M",
            "resennaPersonal": "Cliente preferred",
            "imagen": "https://ejemplo.com/imagen.jpg",
            "interesFK": "47c53f03-87fb-4bc4-8426-d17ef67445e0",
            "usuarioId": "b5fb8aad-6aa6-41d7-b435-a6f011beb2b8"
        }]
    }}
    
    nombre: str = Field(..., description="Nombre del cliente")
    apellidos: str = Field(..., description="Apellidos del cliente")
    identificacion: str = Field(..., description="Número de identificación")
    celular: Optional[str] = Field(None, description="Teléfono celular")
    otroTelefono: Optional[str] = Field(None, description="Otro teléfono")
    direccion: Optional[str] = Field(None, description="Dirección")
    fNacimiento: Optional[str] = Field(None, description="Fecha de nacimiento")
    fAfiliacion: Optional[str] = Field(None, description="Fecha de afiliación")
    sexo: Optional[str] = Field(None, description="Sexo: M/F")
    resennaPersonal: Optional[str] = Field(None, description="Reseña personal")
    imagen: Optional[str] = Field(None, description="URL de imagen")
    interesFK: Optional[str] = Field(None, description="ID del interés")
    usuarioId: str = Field(..., description="ID del usuario")


class ClienteUpdate(BaseModel):
    model_config = {"json_schema_extra": {
        "examples": [{
            "id": "156f22a3-82a9-4c5c-b27f-0466a74390ba",
            "nombre": "Juan Actualizado",
            "apellidos": "Pérez Gómez",
            "identificacion": "12345678901",
            "celular": "88888888",
            "otroTelefono": "99999999",
            "direccion": "San José, Costa Rica",
            "fNacimiento": "1990-01-01T00:00:00.000Z",
            "fAfiliacion": "2024-01-01T00:00:00.000Z",
            "sexo": "M",
            "resennaPersonal": "Cliente preferred",
            "imagen": "https://ejemplo.com/imagen.jpg",
            "interesFK": "47c53f03-87fb-4bc4-8426-d17ef67445e0",
            "usuarioId": "b5fb8aad-6aa6-41d7-b435-a6f011beb2b8"
        }]
    }}
    
    id: Optional[str] = Field(None, description="ID del cliente")
    nombre: Optional[str] = Field(None, description="Nombre del cliente")
    apellidos: Optional[str] = Field(None, description="Apellidos del cliente")
    identificacion: Optional[str] = Field(None, description="Número de identificación")
    celular: Optional[str] = Field(None, description="Teléfono celular")
    otroTelefono: Optional[str] = Field(None, description="Otro teléfono")
    direccion: Optional[str] = Field(None, description="Dirección")
    fNacimiento: Optional[str] = Field(None, description="Fecha de nacimiento")
    fAfiliacion: Optional[str] = Field(None, description="Fecha de afiliación")
    sexo: Optional[str] = Field(None, description="Sexo: M/F")
    resennaPersonal: Optional[str] = Field(None, description="Reseña personal")
    imagen: Optional[str] = Field(None, description="URL de imagen")
    interesFK: Optional[str] = Field(None, description="ID del interés")
    usuarioId: Optional[str] = Field(None, description="ID del usuario")


class ClienteListadoRequest(BaseModel):
    model_config = {"json_schema_extra": {
        "examples": [{
            "identificacion": "",
            "nombre": "",
            "usuarioId": "b5fb8aad-6aa6-41d7-b435-a6f011beb2b8"
        }]
    }}
    
    identificacion: str = Field("", description="Filtrar por identificación")
    nombre: str = Field("", description="Filtrar por nombre")
    usuarioId: str = Field(..., description="ID del usuario")