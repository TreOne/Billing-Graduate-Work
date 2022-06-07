from auth_api.consumer.models import BillMessageBody
from auth_api.services.role_service import RoleService, RoleServiceException
from auth_api.services.user_service import UserService, UserServiceException

role_service = RoleService()


def add_role_to_user(body: BillMessageBody):
    role_uuid = body.item_uuid
    user_uuid = body.user_uuid
    try:
        if role_service.user_has_role(user_uuid, role_uuid):
            roles = role_service.update_role_exp_date(user_uuid, role_uuid, expiration_months=1)
            print(f'Update role exp time {role_uuid} to user. User roles: {roles}.')
        else:
            roles = role_service.add_role_to_user(user_uuid, role_uuid, expiration_months=1)
            print(f'Add role {role_uuid} to user. User roles: {roles}.')
    except (RoleServiceException, UserServiceException) as e:
        return {'msg': str(e)}, e.http_code


def delete_user_role(body: BillMessageBody):
    role_uuid = body.item_uuid
    user_uuid = body.user_uuid
    roles = role_service.delete_user_role(user_uuid, role_uuid)
    print(f'Delete user role - {body.type}. User roles: {roles}.')
