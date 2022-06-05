from auth_api.commons.jwt_utils import deactivate_all_refresh_tokens
from auth_api.services.role_service import RoleService

role_service = RoleService()


def add_role_to_user(body):
    roles = role_service.get_roles()['roles']
    role_uuid = [role['uuid'] for role in roles if role['name'] == 'subscriber']
    user_uuid = body.user_uuid
    roles = role_service.add_role_to_user(user_uuid, role_uuid[0])
    print(f'Add role {body.type} to user. User roles: {roles}.')


# def extend_role(body):
#     role_uuid = ""
#     user_uuid = body.user_uuid
#     roles = user_service.add_role_to_user(user_uuid, role_uuid)
#     print(f'{roles}.')

def delete_user_role(body):
    role_uuid = role_service.get_role(body.type)
    user_uuid = body.user_uuid
    roles = role_service.delete_user_role(user_uuid, role_uuid)
    deactivate_all_refresh_tokens(user_uuid)
    print(f'Delete user role - {body.type}. User roles: {roles}.')
