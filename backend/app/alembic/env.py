import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import (
    create_async_engine
)
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

from app.config.setting import settings
config.set_main_option("sqlalchemy.url", settings.DB_URI)


# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from app.api.v1.models.system.user_model import *
from app.api.v1.models.system.dept_model import *
from app.api.v1.models.system.role_model import *
from app.api.v1.models.system.menu_model import *
from app.api.v1.models.system.position_model import *
from app.api.v1.models.system.operation_log_model import *
from app.api.v1.models.system.notice_model import *
from app.api.v1.models.system.config_model import *
from app.api.v1.models.system.dict_model import *
from app.api.v1.models.system.job_model import *
from app.core.base_model import ModelBase
target_metadata = ModelBase.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_async_engine(config.get_main_option("sqlalchemy.url"), poolclass=pool.NullPool)
    
    async def run_async_migrations():
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)

    def do_run_migrations(connection):
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
