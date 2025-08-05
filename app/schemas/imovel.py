from uuid import UUID
from typing import Optional, List
from sqlmodel import SQLModel

if False:
    from app.schemas.certidao import CertidaoRead


class ImovelCreate(SQLModel):
    endereco: str
    cidade: str
    estado: str
    cep: str
    proprietario_id: UUID

class ImovelUpdate(SQLModel):
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    proprietario_id: Optional[UUID] = None

class ImovelRead(SQLModel):
    id: UUID
    endereco: str
    cidade: str
    estado: str
    cep: str
    proprietario_id: UUID

class ImovelReadWithCertidoes(ImovelRead):
    certidoes: List["CertidaoRead"] = []