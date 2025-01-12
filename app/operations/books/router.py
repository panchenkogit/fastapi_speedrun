from typing import List
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession


from app.entities.books.model import Book as BookDB
from app.entities.books.chema import Book, BookCreate, BookUpdate
 

from database.connect import get_db


router = APIRouter(prefix="/book",
                   tags=['Books'])


@router.get('/all')
async def get_all_books(session: AsyncSession = Depends(get_db)) -> List[Book]:
    query = await session.execute(select(BookDB))
    result = query.scalars().all()
    if not result:
        raise HTTPException(status_code=404,
        detail="Книги не найдены.")

    return result


@router.get('/books/find/{parametr}')
async def search_book(parametr: int | str, session: AsyncSession = Depends(get_db)):
    book = await find_book(parametr, session)
    return book


async def find_book(parametr: int | str,
                    session: AsyncSession):

    if isinstance(parametr, int):
        query = await session.execute(select(BookDB).where(BookDB.id == parametr))
        result = query.scalar_one_or_none()

        if not result:
            raise HTTPException(status_code=404, detail="Книга не найдена.")
        
        return result
    
    if isinstance(parametr, str):
        query = await session.execute(select(BookDB).where(BookDB.title.ilike(f"%{parametr}%")))
        results = query.scalars().all()

        if not results:
            raise HTTPException(status_code=404, detail="Книга не найдена.")
        
        if len(results) > 1:
            book_titles = [{"id": book.id, "Название": book.title, "Автор": book.author} for book in results[:5]]
            raise HTTPException(status_code=400,
                                detail={
                                    "message": "Найдено несколько книг. Уточните запрос.",
                                    "titles": book_titles
                                })
        
        return results[0]




@router.post("/add")
async def add_book(book: BookCreate,
                   session: AsyncSession = Depends(get_db)) -> Book:
    
    query = await session.execute(select(exists(BookDB).where(BookDB.author == book.author,
                                                              BookDB.title == book.title)))
    result = query.scalar()

    if result:
        raise HTTPException(status_code=403,
                            detail="Такая книга уже существует.")
    
    new_book = BookDB(
        title=book.title,
        author=book.author,
        description=book.description,
        year=book.year
    )

    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)

    return new_book


@router.delete("/delete/{id}")
async def delete_by_id(id: int,
                       session: AsyncSession = Depends(get_db)):
    query = await session.execute(select(BookDB).where(BookDB.id == id))
    result = query.scalar_one_or_none()

    if result is None:
       raise HTTPException(status_code=404,
        detail="Книга не найдена.")

    await session.delete(result)
    await session.commit()
    raise HTTPException(status_code=201,
        detail="Книга удалена.")



@router.delete("/delete_by_title/{title}")
async def delete_by_title(title: str, 
                          session: AsyncSession = Depends(get_db)):

    query = await session.execute(select(BookDB).where(BookDB.title.ilike(f"%{title}%")))
    result = query.scalars().all()

    if not result:
        raise HTTPException(status_code=404, detail="Книга не найдена.")

    if len(result) > 1:
        book_titles = [{"Название" : book.title, "Автор": book.author} for book in result]
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Найдено несколько книг. Уточните запрос.",
                "titles": book_titles
            })

    book_to_delete = result[0]
    await session.delete(book_to_delete)
    await session.commit()

    return {"detail": f"Книга '{book_to_delete.title}' удалена."}

@router.patch('/books/{book_id}')
async def update_book(book_id: int,
                      book: BookUpdate,
                      session: AsyncSession = Depends(get_db)):
    
    query = await session.execute(select(BookDB).where(BookDB.id == book_id))
    result = query.scalar_one_or_none()

    if not result:
        raise HTTPException(status_code=404, detail="Книга не найдена.")
    
    book_data = book.model_dump(exclude_unset=True)
    for key, value in book_data.items():
        setattr(result, key, value)

    await session.commit()
    return result


# Не самая лучшая практика
# @router.patch('/update_book/{parametr}')
# async def update_book(parametr: int | str,
#                       book: BookUpdate,
#                       session: AsyncSession = Depends(get_db)):


#     if isinstance(parametr, int):
#         query = await session.execute(select(BookDB).where(BookDB.id == parametr))
#         result = query.scalar_one_or_none()
#         if result is None:
#             raise HTTPException(status_code=404, detail="Книга не найдена.")
        

#     elif isinstance(parametr, str):
#         query = await session.execute(select(BookDB).where(BookDB.title.ilike(f"%{parametr}%")))
#         results = query.scalars().all()

#         if not results:
#             raise HTTPException(status_code=404, detail="Книга не найдена.")
        
#         if len(results) > 1:
#             book_titles = [{"id": book.id, "Название": book.title, "Автор": book.author} for book in results[:5]]
#             raise HTTPException(
#                 status_code=400,
#                 detail={
#                     "message": "Найдено несколько книг. Уточните запрос.",
#                     "titles": book_titles
#                 })
        
#         result = results[0]

#     # Автоматическое обновление атрибутов
#     book_data = book.model_dump(exclude_unset=True)
#     for key, value in book_data.items():
#         if hasattr(result, key):
#             setattr(result, key, value)

#     await session.commit()
#     return result 