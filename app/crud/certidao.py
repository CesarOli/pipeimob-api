from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from app.models.certidao import Certidao
from app.schemas.certidao import CertidaoCreate, CertidaoUpdate

def create_certidao(session: Session, imovel_id: UUID, certidao: CertidaoCreate) -> Certidao:
    db_certidao = Certidao.model_validate(certidao, update={"imovel_id": imovel_id})
    session.add(db_certidao)
    session.commit()
    session.refresh(db_certidao)
    return db_certidao

def get_certidoes_by_imovel(session: Session, imovel_id: UUID, skip: int = 0, limit: int = 100) -> List[Certidao]:
    certidoes = session.exec(
        select(Certidao).where(Certidao.imovel_id == imovel_id).offset(skip).limit(limit)
    ).all()
    return certidoes

def get_certidao_by_id(session: Session, certidao_id: UUID) -> Optional[Certidao]:
    return session.get(Certidao, certidao_id)

def update_certidao(session: Session, db_certidao: Certidao, certidao_update: CertidaoUpdate) -> Certidao:
    certidao_data = certidao_update.model_dump(exclude_unset=True)
    for key, value in certidao_data.items():
        setattr(db_certidao, key, value)
    session.add(db_certidao)
    session.commit()
    session.refresh(db_certidao)
    return db_certidao

def delete_certidao(session: Session, db_certidao: Certidao) -> bool:
    session.delete(db_certidao)
    session.commit()
    return True