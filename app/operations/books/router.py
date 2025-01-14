from typing import List

from fastapi import APIRouter, Depends
from app.exeptions.base_exeptions import (
    NotFoundError,
    DublicateContentError,
    MultipleBooksFoundError,
)
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.books.model import Book as BookDB
from app.entities.books.chema import Book, BookCreate, BookUpdate

from database.connect import get_db

router = APIRouter(prefix="/book", tags=["Books"])


@router.get('/all', description="Получение всех книг по 10 шутк на странице")
async def get_all_books(limit: int = 10,
                        offset: int = 0,
                        session: AsyncSession = Depends(get_db)) -> List[Book]:
    query = await session.execute(select(BookDB).limit(limit).offset(offset))
    result = query.scalars().all()
    if not result:
        raise NotFoundError()
    return result


@router.get('/find/{parametr}', description="Поиск книги по ID,полному названию или его части")
async def search_book(parametr: int | str,
                      session: AsyncSession = Depends(get_db)):
    try: 
        book_id = int(parametr)
        book = await find_book(book_id, session)
    except ValueError:
        book = await find_book(parametr, session)
    return book


async def find_book(parametr: int | str,
                    session: AsyncSession) -> Book:
    if isinstance(parametr, int):
        query = await session.execute(select(BookDB).where(BookDB.id == parametr))
        result = query.scalar_one_or_none()

        if not result:
            raise NotFoundError()

        return result

    if isinstance(parametr, str):
        query = await session.execute(select(BookDB).where(BookDB.title.ilike(f"%{parametr}%")))
        results = query.scalars().all()

        if not results:
            raise NotFoundError()

        if len(results) > 1:
            book_titles = [
                {"id": book.id, "Название": book.title, "Автор": book.author}
                for book in results[:5]
            ]
            raise MultipleBooksFoundError(titles=book_titles)

        return results[0]


@router.post("/add", description="Добавление новой книги")
async def add_book(book: BookCreate,
                   session: AsyncSession = Depends(get_db)) -> Book:
    query = await session.execute(select(exists(BookDB).where(BookDB.author == book.author, BookDB.title == book.title)))
    result = query.scalar()

    if result:
        raise DublicateContentError()

    new_book = BookDB(
        title=book.title,
        author=book.author,
        description=book.description,
        year=book.year,
    )

    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)

    return new_book


@router.delete("/{id}", description="Удаление книги по ID. Получить ID можно по пути /find/{parametr}")
async def delete_book(id: int,
                      session: AsyncSession = Depends(get_db)):
    query = await session.execute(select(BookDB).where(BookDB.id == id))
    result = query.scalar_one_or_none()

    if not result:
        raise NotFoundError()

    await session.delete(result)
    await session.commit()
    return {"detail": f"Книга с ID {id} удалена."}


@router.patch('/{book_id}', description="Поиск книги по ID. Получить ID можно по пути /find/{parametr}")
async def update_book(book_id: int,
                      book: BookUpdate,
                      session: AsyncSession = Depends(get_db)):
    query = await session.execute(select(BookDB).where(BookDB.id == book_id))
    result = query.scalar_one_or_none()

    if not result:
        raise NotFoundError()

    book_data = book.model_dump(exclude_unset=True)
    if not book_data:
        raise NotFoundError()

    for key, value in book_data.items():
        setattr(result, key, value)

    await session.commit()
    return {"detail": f"Книга с ID {book_id} обновлена.", "data": book_data}
