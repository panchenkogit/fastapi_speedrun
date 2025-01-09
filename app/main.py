from fastapi import FastAPI

from database.create_db import create_database

app = FastAPI(title="FastAPI",
              description="Тут будет описание",
                version="1.0.0")

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