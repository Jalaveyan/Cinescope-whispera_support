from typing import Optional, List, Any

from constants.constants import REGISTER_ENDPOINT, LOGIN_ENDPOINT
from custom_requester.custom_requester import CustomRequester
from pydantic import BaseModel, ConfigDict, Field


class AuthAPI(CustomRequester, BaseModel):
    """
          Класс для работы с аутентификацией.
          """
    model_config = ConfigDict(arbitrary_types_allowed=True, extra='allow')
    email: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    passwordRepeat: Optional[str] = None
    roles: List[str] = Field(default_factory=list)

    session: Any = None

    def __init__(self, session):
        BaseModel.__init__(self)
        super().__init__(session=session, base_url="https://auth.dev-cinescope.coconutqa.ru/")

    def register_user(self, user_data, expected_status=None):
        """
        Регистрация нового пользователя.
        :param user_data: Данные пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        if expected_status is None:
            expected_status = [201, 200]

        return self.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data=user_data,
            expected_status=expected_status
        )

    def login_user(self, login_data, expected_status=200):
        """
        Авторизация пользователя.
        :param login_data: Данные для логина.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status
        )

    def authenticate(self, creds):
        login_data = {
            "email": creds[0],
            "password": creds[1]
        }

        response = self.login_user(login_data).json()
        if "accessToken" not in response:
            raise KeyError("token is missing")

        token = response["accessToken"]
        self._update_session_headers(**{"Authorization": f"Bearer {token}"})