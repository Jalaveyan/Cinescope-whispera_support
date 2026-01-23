import allure
import pytest
from playwright.sync_api import expect

from pages.login_page import CinescopLoginPage


@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Login")
@pytest.mark.ui
class TestloginPage:
    
    @allure.title("Проведение успешного входа в систему")
    def test_login_by_ui(self, verified_ui_user, page):
        """
        Логин пользователя через UI.
        Использует верифицированного пользователя, созданного через Admin API.
        """
        login_page = CinescopLoginPage(page)

        login_page.open()
        login_page.login(verified_ui_user["email"], verified_ui_user["password"])
            
        expect(page).to_have_url(login_page.home_url, timeout=30000)
        
        alert_locator = login_page.get_notification_locator("Вы вошли в аккаунт")
        expect(alert_locator).to_be_visible(timeout=10000)

        login_page.make_screenshot_and_attach_to_allure()