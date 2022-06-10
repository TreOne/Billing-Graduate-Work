import pytest

from billing.repositories.role import RoleRepository


@pytest.mark.parametrize(
    "item_uuid, expected_result",
    [
        (
            "1e320df7-cd4b-43e4-8d9c-bdf1f8b5a7e4",
            {
                "uuid": "1e320df7-cd4b-43e4-8d9c-bdf1f8b5a7e4",
                "code": "guest",
                "price": 100,
                "title_ru": "Гость",
            },
        ),
        (
            "169f17d7-63a9-4f52-a49a-20e201a6a29a",
            {
                "uuid": "169f17d7-63a9-4f52-a49a-20e201a6a29a",
                "code": "registered",
                "price": 200,
                "title_ru": "Пользователь",
            },
        ),
        (
            "c45ea0ef-f9b4-4569-af09-9ee7b0a9c16c",
            {
                "uuid": "c45ea0ef-f9b4-4569-af09-9ee7b0a9c16c",
                "code": "administrator",
                "price": 300,
                "title_ru": "Администратор",
            },
        ),
        (
            "065ad9e0-bb75-4127-94a6-6022e3e0a666",
            {
                "uuid": "065ad9e0-bb75-4127-94a6-6022e3e0a666",
                "code": "sub_practix_basic",
                "price": 400,
                "title_ru": "Practix.Стандарт",
            },
        ),
        (
            "6014c570-7ee8-4636-9bca-0415442ca7b6",
            {
                "uuid": "6014c570-7ee8-4636-9bca-0415442ca7b6",
                "code": "sub_practix_plus",
                "price": 500,
                "title_ru": "Practix.Плюс",
            },
        ),
        (
            "2c6fb321-f240-46f8-a73a-335fe69e67ed",
            {
                "uuid": "2c6fb321-f240-46f8-a73a-335fe69e67ed",
                "code": "sub_practix_max",
                "price": 600,
                "title_ru": "Practix.Макс",
            },
        ),
    ],
)
def test_get_role(item_uuid: str, expected_result: dict):
    role = RoleRepository.get_by_id(item_uuid=item_uuid)
    assert role == expected_result
