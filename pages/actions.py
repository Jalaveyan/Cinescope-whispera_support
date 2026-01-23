import allure
from playwright.sync_api import Page, Locator


class PageAction:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Переход на страницу: {url}")
    def open_url(self, url: str):
        self.page.goto(url)

    @allure.step("Ввод текста '{text}' в поле '{locator}'")
    def enter_text_to_element(self, locator: str, text: str):
        self.page.fill(locator, text)

    @allure.step("Клик по элементу '{locator}'")
    def click_element(self, locator: str):
        self.page.click(locator)

    @allure.step("Ожидание загрузки страницы: {url}")
    def wait_for_url(self, url: str):
        self.page.wait_for_url(url)

    @allure.step("Получение текста элемента: {locator}")
    def get_element_text(self, locator: str) -> str:
        return self.page.locator(locator).text_content()

    @allure.step("Ожидание появления или исчезновения элемента: {locator}, state = {state}")
    def wait_for_element(self, locator: str, state: str = "visible"):
        self.page.locator(locator).wait_for(state=state)

    @allure.step("Скриншот текущей страиницы")
    def make_screenshot_and_attach_to_allure(self):
        screenshot_path = "screenshot.png"
        self.page.screenshot(path=screenshot_path, full_page=True)

        with open(screenshot_path, "rb") as file:
            allure.attach(file.read(), name="Screenshot", attachment_type=allure.attachment_type.PNG)

    @allure.step("Получение локатора уведомления с текстом: {text}")
    def get_notification_locator(self, text: str) -> Locator:
        return self.page.get_by_text(text)
