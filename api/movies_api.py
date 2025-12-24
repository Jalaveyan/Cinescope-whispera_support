from custom_requester.custom_requester import CustomRequester


class MoviesApi(CustomRequester):
    """
    Класс для работы с API movies.
    """

    def __init__(self, session):
        super().__init__(
            session=session,
            base_url="https://api.dev-cinescope.coconutqa.ru/"
        )

    def get_movies(self, params=None, expected_status=200):
        """
        Получение списка фильмов.
        :param params: Параметры фильтрации (если None, используются дефолтные значения API сервера).
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            endpoint="/movies",
            params=params,
            expected_status=expected_status
        )

    def get_movie_by_id(self, movie_id: int, expected_status=200):
        """
        Получение фильма по ID.
        :param movie_id: ID фильма.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            endpoint=f"/movies/{movie_id}",
            expected_status=expected_status
        )

    def delete_movie(self, movie_id: int, expected_status=None):
        """
        Удаление фильма.
        :param movie_id: ID фильма для удаления.
        :param expected_status: Ожидаемый статус-код.
        """
        if expected_status is None:
            expected_status = [200, 204]

        return self.send_request(
            method="DELETE",
            endpoint=f"/movies/{movie_id}",
            expected_status=expected_status
        )

    def post_movie(self, data=None, expected_status=201):
        """
        Создание нового фильма.
        :param data: Данные фильма (если None, используются значения по умолчанию).
        :param expected_status: Ожидаемый статус-код.
        """

        return self.send_request(
            method="POST",
            endpoint="/movies",
            expected_status=expected_status,
            data=data
        )

    def patch_movie(self, movie_id: int, data=None, expected_status=200):
        """
        Обновление фильма.
        :param movie_id: ID фильма для обновления.
        :param data: Данные для обновления (если None, генерируются автоматически).
        :param expected_status: Ожидаемый статус-код.
        """

        return self.send_request(
            method="PATCH",
            endpoint=f"/movies/{movie_id}",
            expected_status=expected_status,
            data=data
        )
