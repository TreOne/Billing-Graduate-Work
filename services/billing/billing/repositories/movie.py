from dateutil.relativedelta import relativedelta
from django.conf import settings
from datetime import date
import requests


class MovieRepository:

    @classmethod
    def get_by_id(cls, item_uuid: str) -> tuple:
        url: str = f"{settings.MOVIE_SERVICE_URL}{settings.MOVIE_SERVICE_GET_MOVIE}/{item_uuid}"
        response = requests.get(url=url)
        data = response.json()

        half_year_ago = (date.today() - relativedelta(months=6)).year

        movie_title: str = data.get('title')
        amount: int = 300 if data.get('year') > half_year_ago else 150
        return movie_title, amount
