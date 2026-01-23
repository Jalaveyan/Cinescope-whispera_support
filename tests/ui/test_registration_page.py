import allure
import pytest
from playwright.sync_api import expect

from pages.registration_page import CinescopRegisterPage
from utils.data_generator import DataGenerator


@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Register")
@pytest.mark.ui
class TestRegisterPage:
    
    @allure.title("Проведение успешной регистрации")
    def test_register_by_ui(self, page):
        """
        Регистрация пользователя через UI.
        """
        # Генерируем данные для регистрации
        email = DataGenerator.generate_random_email()
        password = DataGenerator.generate_random_password()
        full_name = DataGenerator.generate_random_name()
        
        register_page = CinescopRegisterPage(page)
        register_page.open()
        register_page.register(full_name, email, password, password)

        expect(page).to_have_url(f"{register_page.home_url}login", timeout=30000)
        
        alert_locator = register_page.get_notification_locator("Подтвердите свою почту")
        expect(alert_locator).to_be_visible(timeout=10000)

        register_page.make_screenshot_and_attach_to_allure()