import bisect
import http
import logging
from typing import Any, NamedTuple

import requests
from django.conf import settings
from requests import JSONDecodeError
from rest_framework.exceptions import ValidationError

from billing.models.enums import BillType

logger = logging.getLogger('billing')

__all__ = ('MovieRepository',)


class MovieData(NamedTuple):
    """Данные о Фильме."""

    movie_title: str
    movie_cost: float


class MovieRepository:
    """Репозиторий по работе с Фильмами."""

    @classmethod
    def get_by_id(cls, item_uuid: str) -> MovieData:
        """Запрашивает информацию о фильме из сервиса контента."""
        data = cls._get_movie_info(item_uuid=item_uuid)
        movie_title: str = data.get('title')
        imdb_rating: float = data.get('imdb_rating')
        movie_cost: float = cls._determine_movie_cost(rating=imdb_rating)
        return MovieData(movie_title=movie_title, movie_cost=movie_cost)

    @classmethod
    def _get_movie_info(cls, item_uuid: str) -> dict[str, Any]:
        """Запросить информацию о фильме из Сервиса Фильмов."""
        try:
            url: str = f'{settings.MOVIE_SERVICE_URL}{settings.MOVIE_SERVICE_GET_MOVIE}/{item_uuid}'
            response: requests.Response = requests.get(url=url)
            return response.json()
        except (requests.exceptions.HTTPError, JSONDecodeError) as e:
            message: str = 'Movie service unavailable.'
            logger.error(
                e,
                exc_info=True,
                extra={
                    'item_uuid': item_uuid,
                    'bill_type': BillType.movie,
                    'http_code': http.HTTPStatus.BAD_REQUEST,
                    'message': message,
                },
            )
            raise ValidationError({'detail': message})

    @classmethod
    def _determine_movie_cost(cls, rating: float) -> float:
        """Определить цену за фильм."""
        costs: list[float] = [50.00, 60.00, 70.00, 80.00, 90.00, 100.00]
        breakpoints: list[int] = [5, 6, 7, 8, 9]
        index = bisect.bisect(breakpoints, rating)
        return costs[index]
