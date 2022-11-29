from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
from starlette.config import Config

settingenv = Config(".env")
DATABASE_NAME: str = settingenv("DATABASE_NAME", cast=str)
POSTGRES_HOST: str = settingenv("POSTGRES_HOST", default="localhost", cast=str)
DATABASE_USERNAME: str = settingenv("DATABASE_USERNAME", cast=str)
POSTGRES_PORT: int = settingenv("POSTGRES_PORT", cast=str)
DATABASE_PASSWORD: str = settingenv("DATABASE_PASSWORD", cast=str)

config = context.config
section = config.config_ini_section

config.set_section_option(section, "DATABASE_USERNAME", DATABASE_USERNAME)
config.set_section_option(section, "DATABASE_PASSWORD", DATABASE_PASSWORD)
config.set_section_option(section, "POSTGRES_HOST", POSTGRES_HOST)
config.set_section_option(section, "POSTGRES_PORT", POSTGRES_PORT)
config.set_section_option(section, "DATABASE_NAME", DATABASE_NAME)
# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
# target_metadata = None
from servicedb.service.models import metadata, user_data

# from service.config.db_settings import
target_metadata = metadata
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
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
