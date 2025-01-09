from fastapi import FastAPI


app = FastAPI(title="FastAPI",
              description="Тут будет описание",
                version="1.0.0")

@app.get("/")
async def hello():
    return {"status" : 200,
            "message" : "hello"}