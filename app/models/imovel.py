from typing import List, Optional
from uuid import UUID, uuid4
from sqlmodel import Field, Relationship, SQLModel

if False:  # 
    from app.models.certidao import Certidao

class Imovel(SQLModel, table=True):

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    endereco: str = Field(index=True)
    cidade: str = Field(index=True)
    estado: str
    cep: str
    proprietario_id: UUID = Field(index=True)
    certidoes: List["Certidao"] = Relationship(
        back_populates="imovel",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    class Config:
        pass