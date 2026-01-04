import datetime
import random
import string
import uuid
from faker import Faker

faker = Faker()


class DataGenerator:

    @staticmethod
    def generate_random_email():
        random_string = ''.join(
            random.choices(string.ascii_lowercase + string.digits, k=8)
        )
        return f"kek{random_string}@gmail.com"


    @staticmethod
    def generate_random_name():
        return f"{faker.first_name()} {faker.last_name()}"


    @staticmethod
    def generate_random_password():
        """
        Генерация пароля, соответствующего требованиям:
        - Минимум 1 буква.
        - Минимум 1 цифра.
        - Допустимые символы.
        - Длина от 8 до 20 символов.
        """
        # Гарантируем наличие хотя бы одной буквы и одной цифры
        letters = random.choice(string.ascii_letters)  # Одна буква
        digits = random.choice(string.digits)  # Одна цифра

        # Дополняем пароль случайными символами из допустимого набора
        special_chars = "?@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6, 18)  # Остальная длина пароля
        remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))

        # Перемешиваем пароль для рандомизации
        password = list(letters + digits + remaining_chars)
        random.shuffle(password)

        return ''.join(password)

    @staticmethod
    def generate_movie_data():
        """
        Генерация данных для создания фильма.
        """
        unique_id = str(uuid.uuid4())[:8]
        return {
            "name": f"Test Movie {unique_id}",
            "imageUrl": f"https://example.com/movie_{unique_id}.jpg",
            "price": random.randint(50, 1000),
            "description": faker.text(max_nb_chars=200),
            "location": random.choice(["MSK", "SPB"]),
            "published": random.choice([True, False]),
            "genreId": random.randint(1, 10)
        }

    @staticmethod
    def generate_movie_filters():
        """
        Генерация параметров фильтрации для GET /movies.
        """
        return {
            "pageSize": random.randint(5, 20),
            "page": random.randint(1, 5),
            "minPrice": random.randint(1, 500),
            "maxPrice": random.randint(500, 2000),
            "locations": random.sample(["MSK", "SPB"], k=random.randint(1, 2)),
            "published": random.choice([True, False]),
            "genreId": random.randint(1, 10),
            "createdAt": random.choice(["asc", "desc"])
        }

    # data_generator.py
    """
    Добавим метод в DataGenerator который сразу делает рандомные данные
    которые можно сразу передать в метод создания юзера через БД
    """

    @staticmethod
    def generate_user_data() -> dict:
        """Генерирует данные для тестового пользователя"""
        from uuid import uuid4

        return {
            'id': f'{uuid4()}',  # генерируем UUID как строку
            'email': DataGenerator.generate_random_email(),
            'full_name': DataGenerator.generate_random_name(),
            'password': DataGenerator.generate_random_password(),
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
            'verified': False,
            'banned': False,
            'roles': '{USER}'
        }

    @classmethod
    def generate_random_int(cls, param):
        pass
