import pytest

from api.api_manager import ApiManager
from constants.roles import Roles


class TestDeleteMovies:

    @pytest.mark.parametrize("movie_data", [
        {
            "name": "Joseph King2",
            "price": 1488,
            "description": "История о том, как IT ментор будучи в походе, придумывает идеальную стратегию для развития своего бизнеса.",
            "imageUrl": "https://alpindustria.ru/i/info/big/6888_1686583057.jpg",
            "location": "SPB",
            "published": True,
            "rating": 0,
            "genreId": 3,
            "createdAt": "2024-07-14T09:35:58.548Z"
        }
    ])

    @pytest.mark.flaky(reruns = 2, reruns_delay = 1)
    def test_delete_movie_positive(self, api_manager : ApiManager, movie_data, super_admin_api_manager):
        """Позитивный тест удаления фильма."""
        # Создаем фильм для удаления
        roles = getattr(super_admin_api_manager, "roles", [])

        create_response = super_admin_api_manager.api.movies_api.post_movie(data=movie_data)
        movie_id = create_response.json()["id"]

        if Roles.SUPER_ADMIN.value in roles:
            super_admin_api_manager.api.movies_api.delete_movie(movie_id, expected_status=[200, 204])
            super_admin_api_manager.api.movies_api.get_movie_by_id(movie_id, expected_status=404)
        elif Roles.USER.value in roles and Roles.ADMIN.value in roles:
            pytest.skip("Проверка отказа в доступе: используйте фикстуру `common_user` и ожидайте 403")
        else:
            pytest.skip(f"Требуется роль SUPER_ADMIN или ADMIN; текущие роли: {roles}")


    def test_delete_movie_negative_unauthorized(self, unauthorized_api_manager: ApiManager, created_movie):
        """Негативный тест удаления фильма без авторизации."""
        response = unauthorized_api_manager.movies_api.delete_movie(created_movie, expected_status=401)
        assert response is not None, "Response должен существовать"

    def test_delete_movie_negative_not_found(self, api_manager: ApiManager, super_admin_api_manager):
        """Негативный тест удаления несуществующего фильма."""
        non_existent_id = 999999
        response = super_admin_api_manager.api.movies_api.delete_movie(non_existent_id, expected_status=404)
        assert response is not None, "Response должен существовать"

    def test_delete_movie_negative_invalid_id(self, api_manager: ApiManager, super_admin_api_manager):
        """Негативный тест удаления фильма с невалидным ID."""

        invalid_id = -1
        response = super_admin_api_manager.api.movies_api.delete_movie(invalid_id, expected_status=[400, 404])
        assert response is not None, "Response должен существовать"