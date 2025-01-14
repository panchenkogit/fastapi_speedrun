import random
from faker import Faker
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from app.entities.books.model import Book

# Создаем подключение к БД
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/library"  # Замените на вашу строку подключения
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем экземпляр Faker
fake = Faker()

# Функция для добавления случайных книг в БД с проверкой уникальности
def add_random_books_to_db(num_books=100):
    session = SessionLocal()
    
    try:
        for _ in range(num_books):
            title = fake.sentence(nb_words=random.randint(3, 6))  # Генерация случайного названия
            author = fake.name()  # Генерация случайного имени автора
            description = fake.text(max_nb_chars=random.randint(100, 300))  # Генерация случайного описания
            year = random.randint(1800, 2025)  # Генерация случайного года

            # Проверка, существует ли книга с таким названием и автором
            existing_book = session.execute(
                select(Book).filter(Book.title == title, Book.author == author)
            ).scalar_one_or_none()

            if existing_book:
                continue  # Если книга уже есть в базе, пропускаем её

            # Создаем новый объект книги
            new_book = Book(
                title=title,
                author=author,
                description=description,
                year=year,
            )
            
            # Добавляем книгу в сессию
            session.add(new_book)

        # Коммитим изменения в БД
        session.commit()
        print(f"{num_books} books added successfully.")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()

# Добавляем 100 случайных книг
add_random_books_to_db(100)
