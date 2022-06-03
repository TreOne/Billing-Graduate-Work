# from auth_api.services.user_service import UserService

# user_service = UserService()

def send_notification_to_user(body):
    print(f'Sending PAID message to user: {body}.')


def send_notification_to_admin(body):
    print(f'Sending CANCELED message to admin: {body}.')


def print_congratulations(body):
    print(f'Congratulations!')

def check_role_user(body):
    user_uuid = body.user_uuid
    roles = user_service.get_user_roles(user_uuid)

def add_role_to_user(body):
    role_uuid = ""
    user_uuid = body.user_uuid
    roles = user_service.add_role_to_user(user_uuid, role_uuid)
    print(f'{roles}.')


def extend_role(body):
    role_uuid = ""
    user_uuid = body.user_uuid
    roles = user_service.add_role_to_user(user_uuid, role_uuid)
    print(f'{roles}.')
