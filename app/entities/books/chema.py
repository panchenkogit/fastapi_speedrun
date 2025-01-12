from pydantic import BaseModel, Field, model_validator


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

    
    @model_validator(mode="before")
    def validate_input(cls, values: dict) -> dict:
        """
        Валидатор исключает значения по умолчанию, которые создаются Swagger (например, "string").
        """
        for key, value in values.items():
            if isinstance(value, str) and value.strip().lower() == "string":
                values[key] = None  # Игнорируем это поле
        return values