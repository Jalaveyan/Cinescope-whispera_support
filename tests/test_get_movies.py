from api.api_manager import ApiManager


class TestGetMovies:

    def test_get_movies_positive(self, api_manager: ApiManager):
        """Позитивный тест получения списка фильмов."""
        response = api_manager.movies_api.get_movies()
        response_data = response.json()
        assert "movies" in response_data, "В ответе отсутствует ключ 'movies'."
        assert "count" in response_data, "В ответе отсутствует ключ 'count'."
        assert "page" in response_data, "В ответе отсутствует ключ 'page'."
        assert isinstance(response_data["movies"], list), "Поле 'movies' не является списком."

    def test_get_movies_with_filters(self, api_manager: ApiManager, super_admin_api_manager, movie_filters):
        """Тест получения списка фильмов с применением фильтров."""
        response = api_manager.movies_api.get_movies(params=movie_filters)
        response_data = response.json()

        assert "movies" in response_data, "В ответе отсутствует ключ 'movies'."
        assert "count" in response_data, "В ответе отсутствует ключ 'count'."
        assert "page" in response_data, "В ответе отсутствует ключ 'page'."
        assert isinstance(response_data["movies"], list), "Поле 'movies' не является списком."

        # Проверяем, что фильтры применены
        if response_data["movies"]:
            for movie in response_data["movies"]:
                # Проверка фильтра по цене
                if "price" in movie and "minPrice" in movie_filters and "maxPrice" in movie_filters:
                    assert movie["price"] >= movie_filters["minPrice"], \
                        f"Фильтр minPrice не применен: {movie['price']} < {movie_filters['minPrice']}"
                    assert movie["price"] <= movie_filters["maxPrice"], \
                        f"Фильтр maxPrice не применен: {movie['price']} > {movie_filters['maxPrice']}"

                # Проверка фильтра по локации
                if "location" in movie and "locations" in movie_filters:
                    assert movie["location"] in movie_filters["locations"], \
                        f"Фильтр locations не применен: {movie['location']} не в {movie_filters['locations']}"

                # Проверка фильтра по статусу публикации
                if "published" in movie and "published" in movie_filters:
                    assert movie["published"] == movie_filters["published"], \
                        f"Фильтр published не применен: {movie['published']} != {movie_filters['published']}"

                # Проверка фильтра по жанру
                if "genreId" in movie and "genreId" in movie_filters:
                    assert movie["genreId"] == movie_filters["genreId"], \
                        f"Фильтр genreId не применен: {movie['genreId']} != {movie_filters['genreId']}"

    def test_get_movie_by_id_positive(self, api_manager: ApiManager, created_movie):
        """Позитивный тест получения фильма по ID."""
        response = api_manager.movies_api.get_movie_by_id(created_movie)
        response_data = response.json()

        assert "id" in response_data, "В ответе отсутствует ключ 'id'."
        assert "name" in response_data, "В ответе отсутствует ключ 'name'."
        assert "description" in response_data, "В ответе отсутствует ключ 'description'."
        assert "reviews" in response_data, "В ответе отсутствует ключ 'reviews'."
        assert response_data["id"] == created_movie, f"Получен фильм с ID {response_data['id']}, ожидался ID {created_movie}"
        assert isinstance(response_data["id"], int), "ID фильма должен быть числом."

    def test_get_movie_by_id_negative_not_found(self, api_manager: ApiManager):
        """Негативный тест получения несуществующего фильма."""
        non_existent_id = 999999
        response = api_manager.movies_api.get_movie_by_id(non_existent_id, expected_status=404)
        assert response is not None, "Response должен существовать"

    def test_get_movie_by_id_negative_invalid_id(self, api_manager: ApiManager):
        """Негативный тест получения фильма с невалидным ID."""
        invalid_id = -1
        response = api_manager.movies_api.get_movie_by_id(invalid_id, expected_status=[400, 404])
        assert response is not None, "Response должен существовать"