from api.api_manager import ApiManager


class TestPatchMovies:

    def test_patch_movie_positive(self, api_manager: ApiManager, created_movie, movie_data, super_admin_api_manager):
        """Позитивный тест обновления фильма."""
        updated_data = movie_data.copy()
        updated_data["name"] = f"Updated {movie_data['name']}"
        updated_data["price"] = movie_data["price"] + 100

        response = super_admin_api_manager.api.movies_api.patch_movie(created_movie, data=updated_data)
        response_data = response.json()
        
        # Проверка обязательных полей
        assert "id" in response_data, "В ответе отсутствует ключ 'id'."
        assert response_data["id"] == created_movie, "ID фильма не совпадает"
        
        # Проверка всех обновленных полей
        assert response_data["name"] == updated_data["name"], "Название фильма не обновлено"
        assert response_data["price"] == updated_data["price"], "Цена фильма не обновлена"
        assert response_data["description"] == updated_data["description"], "Описание фильма не совпадает"
        assert response_data["location"] == updated_data["location"], "Локация фильма не совпадает"
        assert response_data["published"] == updated_data["published"], "Статус публикации не совпадает"
        assert response_data["genreId"] == updated_data["genreId"], "ID жанра не совпадает"

    def test_patch_movie_negative_unauthorized(self, unauthorized_api_manager: ApiManager, created_movie, movie_data):
        """Негативный тест обновления фильма без авторизации."""
        response = unauthorized_api_manager.movies_api.patch_movie(
            created_movie, data=movie_data, expected_status=401
        )
        assert response is not None, "Response должен существовать"

    def test_patch_movie_negative_not_found(self, api_manager: ApiManager, movie_data, super_admin_api_manager):
        """Негативный тест обновления несуществующего фильма."""
        non_existent_id = 999999
        response = super_admin_api_manager.api.movies_api.patch_movie(
            non_existent_id, data=movie_data, expected_status=404
        )
        assert response is not None, "Response должен существовать"

    def test_patch_movie_negative_invalid_data(self, api_manager: ApiManager, created_movie, super_admin_api_manager):
        """Негативный тест обновления фильма с невалидными данными."""
        invalid_data = {
            "name": "",  # Пустое имя
            "price": -100  # Отрицательная цена
        }
        response = super_admin_api_manager.api.movies_api.patch_movie(
            created_movie, data=invalid_data, expected_status=[400, 422]
        )
        assert response is not None, "Response должен существовать"