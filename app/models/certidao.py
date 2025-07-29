from typing import Optional
from uuid import UUID, uuid4
from datetime import date
from sqlmodel import Field, Relationship, SQLModel

from app.models.imovel import Imovel

class Certidao(SQLModel, table=True):

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    tipo: str = Field(index=True)
    data_emissao: date
    status: str = Field(default="PENDENTE", index=True)
    arquivo_url: Optional[str] = None

    imovel_id: UUID = Field(foreign_key="imovel.id", index=True)

    imovel: Optional[Imovel] = Relationship(back_populates="certidoes")

    class Config:
        pass