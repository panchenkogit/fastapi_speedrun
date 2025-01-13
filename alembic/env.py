import asyncio
from logging.config import fileConfig
from alembic import context

# Импортируйте ваши существующие настройки (движок и сессии)
from database.connect import Base, engine, async_session  # Подключаем уже существующий движок и сессию
from config import SQL_DB

# Это объект конфигурации Alembic, который предоставляет доступ
# к значениям в .ini файле.
config = context.config

# Интерпретирует конфигурационный файл для Python logging.
# Эта строка настраивает логгеры.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Добавьте объект MetaData вашего модуля здесь для поддержки 'autogenerate'
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Запуск миграций в 'offline' режиме.

    Здесь настраивается контекст только с URL-адресом, а не с движком,
    и не требуется DBAPI.
    """
    url = SQL_DB
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Запуск миграций в 'online' режиме.

    В этом случае нужно создать асинхронное подключение.
    """
    # Используем уже существующий асинхронный движок (engine) и сессию (async_session)
    async with engine.begin() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        await context.run_migrations()


async def run_migrations() -> None:
    """Запуск миграций в зависимости от того, онлайн или оффлайн."""
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        await run_migrations_online()


# Запуск асинхронных миграций
if __name__ == "__main__":
    asyncio.run(run_migrations())
