import os
from datetime import date
from uuid import UUID, uuid4
from sqlmodel import Session

from app.core.database import get_session
from app.models.imovel import Imovel
from app.schemas.imovel import ImovelCreate, ImovelUpdate
from app.schemas.certidao import CertidaoCreate, CertidaoUpdate
from app.crud.imovel import create_imovel, get_imovel_by_id, update_imovel, delete_imovel, get_imoveis
from app.crud.certidao import create_certidao, get_certidoes_by_imovel, get_certidao_by_id, update_certidao, delete_certidao

def run_tests():
    """
    Função principal para executar os testes manuais da camada CRUD.
    """
    print("Iniciando testes manuais da camada CRUD...")

    with next(get_session()) as session:
        try:
            # =========================
            # 1. TESTE: CRIAÇÃO DE IMÓVEL
            # =========================
            print("\n--- Testando a criação de um Imóvel ---")
            proprietario_id = uuid4()
            imovel_data = ImovelCreate(
                endereco="Rua Teste, 123",
                cidade="São Paulo",
                estado="SP",
                cep="01000-000",
                proprietario_id=proprietario_id,
            )
            novo_imovel = create_imovel(session=session, imovel=imovel_data)
            print(f"Imóvel criado com sucesso! ID: {novo_imovel.id}")
            assert novo_imovel.endereco == "Rua Teste, 123"
            assert novo_imovel.proprietario_id == proprietario_id

            imovel_id = novo_imovel.id

            # =========================
            # 2. TESTE: CRIAÇÃO DE CERTIDÃO PARA O IMÓVEL
            # =========================
            print("\n--- Testando a criação de uma Certidão ---")
            certidao_data = CertidaoCreate(
                tipo="Matrícula",
                data_emissao=date.today(),
                status="EMITIDA",
                arquivo_url="https://s3.amazonaws.com/pipeimob/certidoes/abc.pdf"
            )
            nova_certidao = create_certidao(session=session, imovel_id=imovel_id, certidao=certidao_data)
            print(f"Certidão criada com sucesso! ID: {nova_certidao.id}")
            assert nova_certidao.imovel_id == imovel_id
            assert nova_certidao.status == "EMITIDA"

            certidao_id = nova_certidao.id

            # =========================
            # 3. TESTE: LEITURA (GET) DE IMÓVEIS
            # =========================
            print("\n--- Testando a leitura de Imóveis com filtros ---")
            imoveis_sp = get_imoveis(session=session, estado="SP")
            print(f"Encontrados {len(imoveis_sp)} imóveis no estado de SP.")
            assert len(imoveis_sp) >= 1
            assert imoveis_sp[0].cidade == "São Paulo"

            # =========================
            # 4. TESTE: LEITURA (GET) DE CERTIDÕES
            # =========================
            print("\n--- Testando a leitura de Certidões de um Imóvel ---")
            certidoes_imovel = get_certidoes_by_imovel(session=session, imovel_id=imovel_id)
            print(f"Encontradas {len(certidoes_imovel)} certidões para o imóvel ID: {imovel_id}")
            assert len(certidoes_imovel) == 1
            assert certidoes_imovel[0].tipo == "Matrícula"

            # =========================
            # 5. TESTE: ATUALIZAÇÃO DE IMÓVEL
            # =========================
            print("\n--- Testando a atualização de um Imóvel ---")
            imovel_update_data = ImovelUpdate(endereco="Avenida Brasil, 456")
            imovel_atualizado = update_imovel(session=session, db_imovel=novo_imovel, imovel_update=imovel_update_data)
            print(f"Imóvel atualizado com sucesso! Novo endereço: {imovel_atualizado.endereco}")
            assert imovel_atualizado.endereco == "Avenida Brasil, 456"

            # =========================
            # 6. TESTE: ATUALIZAÇÃO DE CERTIDÃO
            # =========================
            print("\n--- Testando a atualização de uma Certidão ---")
            certidao_update_data = CertidaoUpdate(status="VENCIDA")
            certidao_atualizada = update_certidao(session=session, db_certidao=nova_certidao, certidao_update=certidao_update_data)
            print(f"Certidão atualizada com sucesso! Novo status: {certidao_atualizada.status}")
            assert certidao_atualizada.status == "VENCIDA"

            # =========================
            # 7. TESTE: DELEÇÃO DE CERTIDÃO
            # =========================
            print("\n--- Testando a deleção de uma Certidão ---")
            certidao_deletada = delete_certidao(session=session, db_certidao=certidao_atualizada)
            certidao_existente = get_certidao_by_id(session=session, certidao_id=certidao_id)
            assert certidao_deletada is True
            assert certidao_existente is None
            print(f"Certidão com ID {certidao_id} deletada com sucesso.")

            # =========================
            # 8. TESTE: DELEÇÃO DE IMÓVEL (com cascade)
            # =========================
            print("\n--- Testando a deleção de um Imóvel ---")
            imovel_deletado = delete_imovel(session=session, db_imovel=imovel_atualizado)
            imovel_existente = get_imovel_by_id(session=session, imovel_id=imovel_id)
            assert imovel_deletado is True
            assert imovel_existente is None
            print(f"Imóvel com ID {imovel_id} deletado com sucesso.")

        except Exception as e:
            print(f"\nErro durante os testes: {e}")
            session.rollback()
            raise
        finally:
            print("\nTestes concluídos.")
        

if __name__ == "__main__":
    os.environ['PYTHONPATH'] = os.path.dirname(os.path.abspath(__file__))
    run_tests()