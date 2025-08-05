from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from app.models.imovel import Imovel
from app.schemas.imovel import ImovelCreate, ImovelUpdate

def create_imovel(session: Session, imovel: ImovelCreate) -> Imovel:
    db_imovel = Imovel.model_validate(imovel)
    session.add(db_imovel)
    session.commit()
    session.refresh(db_imovel)
    return db_imovel

def get_imoveis(
    session: Session,
    skip: int = 0,
    limit: int = 100,
    cidade: Optional[str] = None,
    estado: Optional[str] = None
) -> List[Imovel]:
    query = select(Imovel)
    if cidade:
        query = query.where(Imovel.cidade == cidade)
    if estado:
        query = query.where(Imovel.estado == estado)
    imoveis = session.exec(query.offset(skip).limit(limit)).all()
    return imoveis

def get_imovel_by_id(session: Session, imovel_id: UUID) -> Optional[Imovel]:
    return session.get(Imovel, imovel_id)

def update_imovel(session: Session, db_imovel: Imovel, imovel_update: ImovelUpdate) -> Imovel:
    imovel_data = imovel_update.model_dump(exclude_unset=True)
    for key, value in imovel_data.items():
        setattr(db_imovel, key, value)
    session.add(db_imovel)
    session.commit()
    session.refresh(db_imovel)
    return db_imovel

def delete_imovel(session: Session, db_imovel: Imovel) -> bool:
    session.delete(db_imovel)
    session.commit()
    return True