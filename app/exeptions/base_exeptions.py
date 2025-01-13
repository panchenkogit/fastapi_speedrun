from http import HTTPStatus
from fastapi import HTTPException


# Code-404
class NotFoundError(HTTPException):
    def __init__(self, detail = "Запрашиваемый ресурс не найден."):
        super().__init__(HTTPStatus.NOT_FOUND, detail=detail)

# Code-409
class DublicateContentError(HTTPException):
    def __init__(self, detail = "Такой ресурс уже существует.", headers = None):
        super().__init__(HTTPStatus.CONFLICT, detail, headers)

# Code-400
class MultipleBooksFoundError(HTTPException):
    def __init__(self, titles: list[dict], detail: str = "Найдено несколько книг. Уточните запрос."):
        super().__init__(
            HTTPStatus.BAD_REQUEST,
            detail={"message": detail, "titles": titles}
        )