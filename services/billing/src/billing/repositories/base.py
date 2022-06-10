from rest_framework.generics import get_object_or_404

__all__ = ("BaseRepository",)


class BaseRepository:
    """Основной репозиторий."""

    MODEL_CLASS = None

    @classmethod
    def get_all(cls):
        return cls.MODEL_CLASS.objects.all()

    @classmethod
    def get_by_id(cls, item_uuid: str):
        return get_object_or_404(cls.MODEL_CLASS, id=item_uuid)
