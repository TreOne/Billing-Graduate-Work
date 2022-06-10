import http
import logging
from typing import Optional

from rest_framework.exceptions import NotFound

from billing.models.enums import BillType
from utils import constants

logger = logging.getLogger('billing')

__all__ = ('RoleRepository',)


class RoleRepository:
    """Репозиторий по работе с Подписками."""

    MODEL_CLASS = constants.SYSTEM_ROLES

    @classmethod
    def get_by_id(cls, item_uuid: str) -> Optional[dict]:
        try:
            role: dict = [role for role in cls.MODEL_CLASS if role.get('uuid') == item_uuid][0]
            return role
        except Exception as e:
            logger.error(e, exc_info=True, extra={
                'item_uuid': item_uuid,
                'bill_type': BillType.subscription,
                'http_code': http.HTTPStatus.NOT_FOUND,
                'message': 'Такого подписки нет'
            })
            raise NotFound
