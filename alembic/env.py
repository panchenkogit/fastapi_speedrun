from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context

from config import SYNC_SQL_DB   # Используем синхронную строку подключения
from database.connect import Base
from app.entities.books.model import Book


# Это объект конфигурации Alembic, который предоставляет
# доступ к значениям внутри .ini файла
config = context.config

# Интерпретация файла конфигурации для настройки логирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Добавьте объект MetaData ваших моделей для поддержки autogenerate
# Здесь мы указываем метаданные всех ваших моделей
# Например, Product, User и Diary
# target_metadata содержит metadata всех моделей

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Запуск миграций в оффлайн-режиме."""
    context.configure(
        url=SYNC_SQL_DB,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Запуск миграций в онлайн-режиме."""
    # Используем синхронный движок для Alembic
    connectable = create_engine(
        SYNC_SQL_DB,
        poolclass=pool.NullPool,
        future=True,  # Включаем поддержку новой версии SQLAlchemy
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
