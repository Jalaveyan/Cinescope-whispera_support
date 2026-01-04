import pytest
import requests

from api.api_manager import ApiManager
from constants.roles import Roles
from utils.data_generator import DataGenerator

@pytest.fixture(scope="session")
def api_manager():
    session_object = requests.Session()
    api_mgr = ApiManager(session=session_object)
    yield api_mgr
    session_object.close()

@pytest.fixture(scope="session")
def registration_user_data():
    random_password = DataGenerator.generate_random_password()

    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": [Roles.USER.value]
    }
