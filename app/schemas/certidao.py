from uuid import UUID
from datetime import date
from typing import Optional
from sqlmodel import SQLModel

class CertidaoCreate(SQLModel):
    tipo: str
    data_emissao: date
    status: Optional[str] = "PENDENTE"
    arquivo_url: Optional[str] = None

class CertidaoUpdate(SQLModel):
    tipo: Optional[str] = None
    data_emissao: Optional[date] = None
    status: Optional[str] = None
    arquivo_url: Optional[str] = None

class CertidaoRead(SQLModel):
    id: UUID
    tipo: str
    data_emissao: date
    status: str
    arquivo_url: Optional[str] = None
    imovel_id: UUID