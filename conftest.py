import pytest
import requests

from api.api_manager import ApiManager
from utils.data_generator import DataGenerator


@pytest.fixture(scope="session")
def api_manager():
    session_object = requests.Session()
    api_mgr = ApiManager(session=session_object)
    yield api_mgr
    session_object.close()


@pytest.fixture(scope="session")
def unauthorized_api_manager():
    """
    Фикстура для неавторизованного API менеджера с новой сессией.
    Используется для негативных тестов на неавторизованные запросы.
    """
    session_object = requests.Session()
    api_mgr = ApiManager(session=session_object)
    yield api_mgr
    session_object.close()

@pytest.fixture(scope="session")
def test_user():
    """
    Генерация случайного пользователя для тестов.
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }


@pytest.fixture
def registered_user(api_manager, test_user):
    """
    Фикстура для зарегистрированного пользователя.
    """
    response = api_manager.auth_api.register_user(test_user)
    return test_user


@pytest.fixture
def authenticated_api_manager(api_manager, registered_user):
    """
    Фикстура для авторизованного API менеджера.
    """
    api_manager.auth_api.authenticate([registered_user["email"], registered_user["password"]])
    return api_manager


@pytest.fixture
def super_admin_api_manager(api_manager):
    """
    Фикстура для авторизованного супер-админа.
    """
    SUPER_ADMIN_CREDS = ["api1@gmail.com", "asdqwe123Q"]
    api_manager.auth_api.authenticate(SUPER_ADMIN_CREDS)
    return api_manager


@pytest.fixture
def movie_data():
    """
    Фикстура для генерации данных фильма.
    """
    return DataGenerator.generate_movie_data()


@pytest.fixture
def movie_filters():
    """
    Фикстура для генерации параметров фильтрации.
    """
    return DataGenerator.generate_movie_filters()


@pytest.fixture
def created_movie(super_admin_api_manager, movie_data):
    """
    Фикстура для создания фильма и получения его ID.
    """
    response = super_admin_api_manager.movies_api.post_movie(data=movie_data)
    movie_id = response.json().get("id")
    yield movie_id
    # Cleanup: удаляем фильм после теста
    try:
        super_admin_api_manager.movies_api.delete_movie(movie_id, expected_status=[200, 204])
    except Exception:
        pass  # Игнорируем ошибки при удалении