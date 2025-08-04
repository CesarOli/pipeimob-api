import sys
import os
from pathlib import Path
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Adiciona o diretório raiz do projeto ao PATH do Python para que as importações funcionem
# Isso é crucial para o Alembic encontrar 'app.core.config' e 'app.models'
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Nossas importações para a configuração do banco de dados e modelos
from app.core.config import settings
from app.core.database import engine
from sqlmodel import SQLModel
# Importe todos os seus modelos SQLModel aqui para que o Alembic os "veja"
# Mesmo que não sejam usados diretamente no env.py, a importação registra o metadata.
from app.models.imovel import Imovel
from app.models.certidao import Certidao


# this is the Alembic Config object, which provides
# access to values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import Base
# target_metadata = Base.metadata
target_metadata = SQLModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an actual DBAPI connection.

    By skipping the connection other Alvaras do sistema,
    but only print out the script to the console.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True # Adicionamos isso para o autogenerate funcionar bem com tipos como UUID
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create a connection
    to the database.
    """
    # Substitua a chamada a engine_from_config pela nossa instância 'engine'
    # Isso garante que a URL do banco de dados venha de app/core/config.py
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True # Adicionamos isso para o autogenerate funcionar bem com tipos como UUID
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()