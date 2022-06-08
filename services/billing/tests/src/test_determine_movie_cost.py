import pytest

from billing.repositories.movie import MovieRepository


@pytest.mark.parametrize(
    "imdb_rating, expected_result",
    [
        (9.99, 100.0),
        (8.2, 90.0),
        (7.2, 80.0),
        (6.2, 70.0),
        (5.7, 60.0),
        (4.2, 50.0),
        (3.2, 50.0),
    ],
)
def test_determine_movie_const(imdb_rating: float, expected_result: float):
    result = MovieRepository._determine_movie_cost(rating=imdb_rating)
    assert result == expected_result
