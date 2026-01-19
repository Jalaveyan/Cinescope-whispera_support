"""
Фикстуры для UI тестов (Playwright).
"""
import pytest
import requests

from api.api_manager import ApiManager
from constants.roles import Roles
from entities.user import User
from utils.data_generator import DataGenerator


@pytest.fixture(scope="session")
def ui_api_session():
    """
    Отдельная сессия API для UI тестов.
    """
    session = requests.Session()
    api_manager = ApiManager(session=session)
    yield api_manager
    session.close()


@pytest.fixture(scope="session")
def ui_super_admin(ui_api_session):
    """
    Super Admin для создания пользователей в UI тестах.
    """
    ui_api_session.auth_api.authenticate([
        User.SUPER_ADMIN_USERNAME,
        User.SUPER_ADMIN_PASSWORD
    ])
    return ui_api_session


@pytest.fixture(scope="session")
def ui_test_user():
    """
    Генерирует данные для тестового пользователя.
    Scope="session" чтобы данные были одинаковы для всех тестов сессии.
    """
    password = DataGenerator.generate_random_password()
    
    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": password,
        "passwordRepeat": password,
        "roles": [Roles.USER.value]
    }


@pytest.fixture(scope="session")
def verified_ui_user(ui_super_admin, ui_test_user):
    """
    Создаёт верифицированного пользователя через Admin API.
    Возвращает данные пользователя для использования в тестах логина.
    """
    user_data = ui_test_user.copy()
    user_data["verified"] = True
    user_data["banned"] = False
    
    # Создаём пользователя через Admin API
    ui_super_admin.user_api.create_user(user_data)
    
    return ui_test_user
