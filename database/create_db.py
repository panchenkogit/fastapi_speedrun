from app.entities.books import model
from database.connect import Base, engine

async def create_database():
    async with engine.begin() as conn:
        print("Начало создания базы данных...")
        await conn.run_sync(Base.metadata.create_all)
        print("Таблицы успешно созданы!")