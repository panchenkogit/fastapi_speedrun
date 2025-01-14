from locust import HttpUser, task, between
import random

from faker import Faker

fake = Faker()

class BookstoreUser(HttpUser):
    wait_time = between(1, 2.5)  # Время ожидания между запросами (в секундах)

    # @task
    # def get_all_books(self):
    #     self.client.get("/book/all")  # Эндпоинт для получения всех книг

    # @task
    # def search_books(self):
    #     id = random.randint(1, 500)
    #     self.client.get(f"/book/find/{id}")  # Поиск книги по ID

    @task
    def add_book(self):
        self.client.post("/book/add", json={
            "title": fake.sentence(nb_words=random.randint(3, 6)),
            "author": fake.name(),
            "description": fake.text(max_nb_chars=random.randint(100, 300)),
            "year": random.randint(1400, 2025)
        })
