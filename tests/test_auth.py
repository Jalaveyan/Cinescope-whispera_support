from api.api_manager import ApiManager
from utils.data_generator import DataGenerator


class TestAuthAPI:

    def test_register_user_positive(self, api_manager: ApiManager, test_user):
        """Позитивный тест регистрации пользователя."""
        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()

        # Проверка основных полей
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert isinstance(response_data["id"], int), "ID должен быть числом"
        assert response_data["email"] == test_user["email"], "Email не совпадает"
        
        # Проверка имени пользователя
        assert "fullName" in response_data, "fullName отсутствует в ответе"
        assert response_data["fullName"] == test_user["fullName"], "fullName не совпадает"
        
        # Проверка ролей
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
        assert isinstance(response_data["roles"], list), "Роли должны быть списком"
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"

    def test_register_user_negative_duplicate_email(self, api_manager: ApiManager, registered_user):
        """Негативный тест регистрации с уже существующим email."""
        duplicate_user = {
            "email": registered_user["email"],
            "fullName": DataGenerator.generate_random_name(),
            "password": DataGenerator.generate_random_password(),
            "passwordRepeat": DataGenerator.generate_random_password(),
            "roles": ["USER"]
        }
        response = api_manager.auth_api.register_user(duplicate_user, expected_status=[400, 409, 422])
        assert response is not None, "Response должен существовать"

    def test_register_user_negative_invalid_data(self, api_manager: ApiManager):
        """Негативный тест регистрации с невалидными данными."""
        invalid_user = {
            "email": "invalid-email",  # Невалидный email
            "fullName": "",
            "password": "123",  # Слишком короткий пароль
            "passwordRepeat": "456"  # Пароли не совпадают
        }
        response = api_manager.auth_api.register_user(invalid_user, expected_status=[400, 422])
        assert response is not None, "Response должен существовать"

    def test_login_user_positive(self, api_manager: ApiManager, registered_user):
        """Позитивный тест авторизации пользователя."""
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"],
        }

        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()

        # Проверка токена
        assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
        assert isinstance(response_data["accessToken"], str), "Токен должен быть строкой"
        assert len(response_data["accessToken"]) > 0, "Токен не должен быть пустым"
        
        # Проверка данных пользователя
        assert "user" in response_data, "Данные пользователя отсутствуют в ответе"
        assert "email" in response_data["user"], "Email пользователя отсутствует"
        assert response_data["user"]["email"] == registered_user["email"], "Email не совпадает"
        assert "id" in response_data["user"], "ID пользователя отсутствует"
        assert "roles" in response_data["user"], "Роли пользователя отсутствуют"

    def test_login_user_negative_wrong_password(self, api_manager: ApiManager, registered_user):
        """Негативный тест авторизации с неверным паролем."""
        login_data = {
            "email": registered_user["email"],
            "password": "wrong_password_123",
        }

        response = api_manager.auth_api.login_user(login_data, expected_status=401)
        assert response is not None, "Response должен существовать"

    def test_login_user_negative_nonexistent_user(self, api_manager: ApiManager):
        """Негативный тест авторизации несуществующего пользователя."""
        login_data = {
            "email": f"nonexistent_{DataGenerator.generate_random_email()}",
            "password": DataGenerator.generate_random_password(),
        }

        response = api_manager.auth_api.login_user(login_data, expected_status=401)
        assert response is not None, "Response должен существовать"