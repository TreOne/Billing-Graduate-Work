import bisect
from typing import Tuple

import requests
from django.conf import settings


class MovieRepository:
    @classmethod
    def get_by_id(cls, item_uuid: str) -> Tuple[str, float]:
        """Запрашивает информацию о фильме из сервиса контента."""
        data = cls._get_movie_info(item_uuid=item_uuid)
        movie_title: str = data.get("title")
        imdb_rating: float = data.get("imdb_rating")
        movie_cost: float = cls._determine_movie_cost(rating=imdb_rating)
        return movie_title, movie_cost

    @classmethod
    def _get_movie_info(cls, item_uuid: str) -> dict:
        url: str = f"{settings.MOVIE_SERVICE_URL}{settings.MOVIE_SERVICE_GET_MOVIE}/{item_uuid}"
        response = requests.get(url=url)
        return response.json()

    @classmethod
    def _determine_movie_cost(cls, rating: float) -> float:
        costs: list[float] = [50.00, 60.00, 70.00, 80.00, 90.00, 100.00]
        breakpoints: list[int] = [5, 6, 7, 8, 9]
        index = bisect.bisect(breakpoints, rating)
        return costs[index]
