from auth_api.services.role_service import RoleService, RoleServiceException

role_service = RoleService()


def add_role_to_user(body):
    role_uuid = body.item_uuid
    user_uuid = body.user_uuid
    try:
        roles = role_service.add_role_to_user(user_uuid, role_uuid, 31)
        print(f'Add role {body.type} to user. User roles: {roles}.')
    except RoleServiceException as e:
        return {'msg': str(e)}, e.http_code


def delete_user_role(body):
    role_uuid = body.item_uuid
    user_uuid = body.user_uuid
    roles = role_service.delete_user_role(user_uuid, role_uuid)
    print(f'Delete user role - {body.type}. User roles: {roles}.')
