from api.api_manager import ApiManager


class TestPostMovies:

    def test_add_movie_positive(self, api_manager: ApiManager, movie_data, super_admin_api_manager):
        """Позитивный тест создания фильма."""
        response = super_admin_api_manager.api.movies_api.post_movie(data=movie_data)
        response_data = response.json()
        
        # Проверка обязательных полей
        assert "id" in response_data, "В ответе отсутствует ключ 'id'."
        assert isinstance(response_data["id"], int), "ID должен быть числом"
        
        # Проверка всех переданных данных
        assert response_data["name"] == movie_data["name"], "Название фильма не совпадает"
        assert response_data["price"] == movie_data["price"], "Цена фильма не совпадает"
        assert response_data["description"] == movie_data["description"], "Описание фильма не совпадает"
        assert response_data["location"] == movie_data["location"], "Локация фильма не совпадает"
        assert response_data["published"] == movie_data["published"], "Статус публикации не совпадает"
        assert response_data["genreId"] == movie_data["genreId"], "ID жанра не совпадает"
        assert response_data["imageUrl"] == movie_data["imageUrl"], "URL изображения не совпадает"

        # Cleanup
        movie_id = response_data["id"]
        super_admin_api_manager.api.movies_api.delete_movie(movie_id, expected_status=[200, 204])

    def test_add_movie_negative_unauthorized(self, unauthorized_api_manager: ApiManager, movie_data):
        """Негативный тест создания фильма без авторизации."""
        response = unauthorized_api_manager.movies_api.post_movie(data=movie_data, expected_status=401)
        assert response is not None, "Response должен существовать"

    def test_add_movie_negative_invalid_data(self, api_manager: ApiManager, super_admin_api_manager):
        """Негативный тест создания фильма с невалидными данными."""
        invalid_data = {
            "name": "",
            "price": -100,
            "description": "Test"
        }
        response = super_admin_api_manager.api.movies_api.post_movie(data=invalid_data, expected_status=[400, 422])
        assert response is not None, "Response должен существовать"

    def test_add_movie_negative_missing_required_fields(self, api_manager: ApiManager, super_admin_api_manager):
        """Негативный тест создания фильма без обязательных полей."""
        incomplete_data = {
            "name": "Test Movie"
        }
        response = super_admin_api_manager.api.movies_api.post_movie(data=incomplete_data, expected_status=[400, 422])
        assert response is not None, "Response должен существовать"