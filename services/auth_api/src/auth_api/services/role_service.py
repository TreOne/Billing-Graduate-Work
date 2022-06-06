from http.client import CONFLICT, NOT_FOUND

from auth_api.api.v1.schemas.role import RoleSchema
from auth_api.database import session
from auth_api.models.user import Role, User, UsersRoles


class RoleServiceException(Exception):
    def __init__(self, message, http_code=None):
        super().__init__(message)
        self.http_code = http_code


class RoleService:

    def get_role(self, role_uuid: str):
        schema = RoleSchema()
        role = session.query(Role).filter_by(uuid=role_uuid).first()
        return schema.dump(role)

    def update_role(self, role_uuid: str, new_name: str):
        schema = RoleSchema(partial=True)
        role = session.query(Role).filter_by(uuid=role_uuid).first()
        role.name = new_name

        session.commit()
        return schema.dump(role)

    def delete_role(self, role_uuid: str):
        role = session.query(Role).filter_by(uuid=role_uuid).first()
        session.delete(role)
        session.commit()

    def get_roles(self):
        schema = RoleSchema(many=True)
        roles = session.query(Role).all()
        return schema.dump(roles)

    def create_role(self, name: str):
        schema = RoleSchema()
        role = Role(name=name)

        existing_role = session.query(Role).filter_by(name=name).first()
        if existing_role:
            raise RoleServiceException('Role already exist!', http_code=CONFLICT)

        session.add(role)
        session.commit()

        return {'msg': 'Role created.', 'role': schema.dump(role)},

    def add_role_to_user(self, user_uuid: str, role_uuid: str):
        user = session.query(User).get(user_uuid)
        if not user:
            raise RoleServiceException('User not found.', http_code=NOT_FOUND)
        role = session.query(Role).get(role_uuid)
        if not role:
            raise RoleServiceException('Role not found.', http_code=NOT_FOUND)
        user.roles.append(role)

        session.add(user)
        session.commit()

        return user.roles

    def delete_user_role(self, user_uuid: str, role_uuid: str):
        user = session.query(User).get(user_uuid)
        if not user:
            raise RoleServiceException('User not found.', http_code=NOT_FOUND)
        role = session.query(Role).get(role_uuid)
        if not role:
            raise RoleServiceException('Role not found.', http_code=NOT_FOUND)

        if role in user.roles:
            user.roles.remove(role)
        else:
            raise RoleServiceException('The user does not have this role.', http_code=CONFLICT)

        session.add(user)
        session.commit()

        return user.roles

    def get_user_roles(self, user_uuid: str):
        user = session.query(User).get(user_uuid)
        if not user:
            raise RoleServiceException('User not found.', http_code=NOT_FOUND)
        return user.roles
