import random
import time
from typing import Any, Generator

import allure
import pytest
import requests


from api.api_manager import ApiManager
from constants.roles import Roles
from db_requester.db_client import get_db_session
from db_requester.db_helpers import DBHelper
from entities.user import User
from tools.tools import Tools
from utils.data_generator import DataGenerator

DEFAULT_UI_TIMEOUT = 30000


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

@pytest.fixture(scope="function")
def test_user():

    random_password = DataGenerator.generate_random_password()

    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": [Roles.USER.value]
    }


@pytest.fixture(scope="session")
def ui_test_user():
    """
    Фиксированные данные для UI тестов регистрации и логина.
    Scope="session" чтобы данные были одинаковы для всей сессии тестов.
    """
    random_password = DataGenerator.generate_random_password()
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    
    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": [Roles.USER.value]
    }


@pytest.fixture(scope="session")
def verified_ui_user(super_admin_api_manager, ui_test_user):
    """
    Создаёт верифицированного пользователя через admin API для UI теста логина.
    """
    user_data = ui_test_user.copy()
    user_data["verified"] = True
    user_data["banned"] = False
    
    super_admin_api_manager.api.user_api.create_user(user_data)
    return ui_test_user

@pytest.fixture(scope="function")
def registered_user(super_admin_api_manager, test_user):
    """
    Фикстура для зарегистрированного и верифицированного пользователя.
    Использует admin API для создания пользователя с verified=True.
    """
    user_data = test_user.copy()
    user_data["verified"] = True
    user_data["banned"] = False
    
    # Создаём пользователя через admin API (уже верифицированный)
    super_admin_api_manager.api.user_api.create_user(user_data)
    return test_user  # Возвращаем оригинальные данные с паролем



@pytest.fixture(scope="session")
def authenticated_api_manager(api_manager, registered_user):
    """
    Фикстура для авторизованного API менеджера.
    """
    api_manager.auth_api.authenticate([registered_user["email"], registered_user["password"]])
    return api_manager


@pytest.fixture(scope="session")
def super_admin_api_manager(user_session):
    new_session = user_session()
    """
    Фикстура для авторизованного супер-админа.
    """
    super_admin = User(
        User.SUPER_ADMIN_USERNAME,
        User.SUPER_ADMIN_PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)

    return super_admin


@pytest.fixture(scope="session")
def movie_data():
    """
    Фикстура для генерации данных фильма.
    """
    return DataGenerator.generate_movie_data()


@pytest.fixture(scope="session")
def movie_filters():
    """
    Фикстура для генерации параметров фильтрации.
    """
    return DataGenerator.generate_movie_filters()


@pytest.fixture(scope="session")
def created_movie(super_admin_api_manager, movie_data):
    """
    Фикстура для создания фильма и получения его ID.
    """
    response = super_admin_api_manager.api.movies_api.post_movie(data=movie_data)
    movie_id = response.json().get("id")
    yield movie_id
    # Cleanup: удаляем фильм после теста
    try:
        super_admin_api_manager.api.movies_api.delete_movie(movie_id, expected_status=[200, 204])
    except Exception:
        pass  # Игнорируем ошибки при удалении

@pytest.fixture
def common_user(user_session, super_admin_api_manager, creation_user_data):
    new_session = user_session()

    user_data = creation_user_data.copy()
    user_data["roles"] = [Roles.USER.value]

    common_user = User(
        user_data["email"],
        user_data["password"],
        user_data["roles"],
        new_session)

    super_admin_api_manager.api.user_api.create_user(user_data)
    common_user.api.auth_api.authenticate(common_user.creds)

    return common_user


@pytest.fixture
def common_admin(user_session, super_admin_api_manager, creation_user_data):
    new_session = user_session()

    admin_data = creation_user_data.copy()
    admin_data["roles"] = [Roles.ADMIN.value]

    common_admin = User(
        admin_data["email"],
        admin_data["password"],
        admin_data["roles"],
        new_session)

    super_admin_api_manager.api.user_api.create_user(admin_data)
    common_admin.api.auth_api.authenticate(common_admin.creds)

    return common_admin

@pytest.fixture(scope="function")
def creation_user_data(test_user):
    updated_data = test_user.copy()
    # Ensure unique email per test to avoid conflicts with already registered users
    updated_data["email"] = DataGenerator.generate_random_email()
    updated_data.update({
        "verified" : True,
        "banned" : False
    })

    return updated_data

@pytest.fixture(scope="session")
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()

@pytest.fixture(scope="module")
def db_session() -> Generator[Any, Any, None]:
    db_session = get_db_session()
    yield db_session
    db_session.close()

@pytest.fixture(scope="function")
def db_helper(db_session) -> DBHelper:
    """
    Фикстура для экземпляра хелпера
    """
    db_helper = DBHelper(db_session)
    return db_helper


@pytest.fixture(scope="function")
def created_test_user(db_helper):
    """
    Фикстура, которая создает тестового пользователя в БД
    и удаляет его после завершения теста
    """
    user = db_helper.create_test_user(DataGenerator.generate_user_data())
    yield user
    # Cleanup после теста
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)

@pytest.fixture
def delay_between_retries():
    time.sleep(2)
    yield
