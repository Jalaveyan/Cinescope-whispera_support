from api.api_manager import ApiManager


class TestDeleteMovies:

    def test_delete_movie_positive(self, super_admin_api_manager: ApiManager, movie_data):
        """Позитивный тест удаления фильма."""
        # Создаем фильм для удаления
        create_response = super_admin_api_manager.movies_api.post_movie(data=movie_data)
        movie_id = create_response.json()["id"]

        # Удаляем фильм
        response = super_admin_api_manager.movies_api.delete_movie(movie_id)
        assert response is not None, "Response должен существовать"

        # Проверяем, что фильм действительно удален
        get_response = super_admin_api_manager.movies_api.get_movie_by_id(movie_id, expected_status=404)
        assert get_response is not None, "Response должен существовать"

    def test_delete_movie_negative_unauthorized(self, unauthorized_api_manager: ApiManager, created_movie):
        """Негативный тест удаления фильма без авторизации."""
        response = unauthorized_api_manager.movies_api.delete_movie(created_movie, expected_status=401)
        assert response is not None, "Response должен существовать"

    def test_delete_movie_negative_not_found(self, super_admin_api_manager: ApiManager):
        """Негативный тест удаления несуществующего фильма."""
        non_existent_id = 999999
        response = super_admin_api_manager.movies_api.delete_movie(non_existent_id, expected_status=404)
        assert response is not None, "Response должен существовать"

    def test_delete_movie_negative_invalid_id(self, super_admin_api_manager: ApiManager):
        """Негативный тест удаления фильма с невалидным ID."""
        invalid_id = -1
        response = super_admin_api_manager.movies_api.delete_movie(invalid_id, expected_status=[400, 404])
        assert response is not None, "Response должен существовать"