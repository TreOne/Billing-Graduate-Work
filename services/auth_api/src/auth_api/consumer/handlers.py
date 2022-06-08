import logging
from logging import config as logging_config

from auth_api.consumer.logger import LOGGER_SETTINGS
from auth_api.consumer.models import BillMessageBody
from auth_api.services.user_service import UserService, UserServiceException

user_service = UserService()
logging_config.dictConfig(LOGGER_SETTINGS)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def add_role_to_user(body: BillMessageBody):
    if body.type != 'subscription':
        return
    role_uuid = body.item_uuid
    user_uuid = body.user_uuid
    try:
        if user_service.user_has_role(user_uuid, role_uuid):
            roles = user_service.update_role_exp_date(user_uuid, role_uuid, expiration_months=1)
            logger.info(f'Update role exp time {role_uuid} to user. User roles: {roles}.')
        else:
            roles = user_service.add_role_to_user(user_uuid, role_uuid, expiration_months=1)
            logger.info(f'Add role {role_uuid} to user. User roles: {roles}.')
    except UserServiceException as e:
        logger.error(f'{e}')
        return {'msg': str(e)}, e.http_code


def delete_user_role(body: BillMessageBody):
    if body.type != 'subscription':
        return
    role_uuid = body.item_uuid
    user_uuid = body.user_uuid
    roles = user_service.delete_user_role(user_uuid, role_uuid)
    logger.info(f'Delete user role - {role_uuid}. User roles: {roles}.')
