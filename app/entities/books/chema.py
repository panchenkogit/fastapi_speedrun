from pydantic import BaseModel, Field, model_validator


class BaseBook(BaseModel):
    title: str = Field(...,max_length=100, description="Название", examples=["Преступление и наказание"])
    author: str = Field(...,max_length=100, description="Автор", examples=["Ф.М.Достоевский"])
    description: str | None = Field(None, max_length=1000, description="Описание", examples=["Тут будет описание"])
    year: int = Field(..., gt=0, lt=2025, description="Год издания", examples=["1864"])


class BookCreate(BaseBook):
    pass


class Book(BaseBook):
    id: int = Field(...,gt=0, description="Уникальный идентификатор", examples=[1, "преступление"])
    
    class Config:
        from_attributes = True


class BookUpdate(BaseModel):
    title: str | None = Field(None, max_length=100, description="Название", examples=["Преступление и наказание"])
    author: str | None = Field(None, max_length=100, description="Автор", examples=["Ф.М.Достоевский"])
    description: str | None = Field(None, max_length=1000, description="Описание", examples=["Тут будет описание"])
    year: int | None = Field(None, gt=0, lt=2025, description="Год издания", examples=["1864"])

    
    @model_validator(mode="before")
    def validate_input(cls, values: dict) -> dict:
        """
        Валидатор исключает значения по умолчанию, которые создаются Swagger (например, "string").
        """
        for key, value in values.items():
            if isinstance(value, str) and value.strip().lower() == "string":
                values[key] = None  # Игнорируем это поле
        return values