__all__ = ('BaseRepository',)


class BaseRepository:

    MODEL_CLASS = None

    @classmethod
    def get_all(cls):
        return cls.MODEL_CLASS.objects.all()

    @classmethod
    def get_by_id(cls, item_id: int):
        return cls.MODEL_CLASS.objects.get(pk=item_id)
