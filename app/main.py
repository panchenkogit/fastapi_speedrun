from fastapi import FastAPI
from app.operations.books.router import router as books_router

from database.create_db import create_database

app = FastAPI(title="FastAPI",
              description="Короткое API для управления библиотекой.Позволяет добавлять, удалять, находить книги и управлять ими.",
                version="1.2.0",
                contact={
        "name": "Евгений",
        "email": "odosaol@yandex.ru",
    },)

app.include_router(books_router)

@app.get("/")
async def hello():
    return {"status" : 200,
            "message" : "hello"}

@app.on_event("startup")
async def startup():
    await create_database()
    print("База данных создана")

@app.on_event("shutdown")
async def shutdown():
    print("Приложение завершило работу")