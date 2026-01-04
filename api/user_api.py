from typing import Optional, List, Any

from pydantic import BaseModel, ConfigDict, Field
from custom_requester.custom_requester import CustomRequester

class UserAPI(CustomRequester, BaseModel):
    """
    Класс для работы с API пользователей.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, extra='allow')

    email: Optional[str] = None
    password: Optional[str] = None
    roles: List[str] = Field(default_factory=list)

    session: Any = None

    def __init__(self, session):
        BaseModel.__init__(self)
        super().__init__(session=session,base_url="https://auth.dev-cinescope.coconutqa.ru/")
        self.session = session

    def get_user_info(self, user_id, expected_status=200):
        """
        Получение информации о пользователе.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """

        return self.send_request(
            method="GET",
            endpoint=f"user/{user_id}",
            expected_status=expected_status
        )

    def delete_user(self, user_id, expected_status=204):
        """
        Удаление пользователя.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="DELETE",
            endpoint=f"user/{user_id}",
            expected_status=expected_status
        )

    def get_user(self, user_locator, expected_status=200):
        return self.send_request(
            method="GET",
            endpoint=f"user/{user_locator}",
            expected_status=expected_status
        )

    def create_user(self, user_data, expected_status=201):
        return self.send_request(
            method="POST",
            endpoint=f"user",
            data=user_data,
            expected_status=expected_status
        )
