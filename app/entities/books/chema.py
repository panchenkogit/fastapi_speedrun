from pydantic import BaseModel, Field


class BaseBook(BaseModel):
    title: str = Field(...,max_length=30, description="Название")
    author: str = Field(...,max_length=30, description="Автор")
    description: str | None = Field(None, max_length=100, description="Описание") 
    year: int = Field(..., gt=0, lt=2025, description="Год издания")

class BookCreate(BaseBook):
    pass

class Book(BaseBook):
    id: int = Field(...,gt=0, description="Уникальный идентификатор")
    pass
    class Config:
        from_attributes = True

class BookUpdate(BaseModel):
    title: str | None = Field(None, max_length=30, description="Название")
    author: str | None = Field(None, max_length=15, description="Автор")
    description: str | None = Field(None, max_length=100, description="Описание")
    year: int | None = Field(None, gt=0, lt=2025, description="Год издания")