from http.client import CONFLICT

from auth_api.api.v1.schemas.role import RoleSchema
from auth_api.extensions import db
from auth_api.models.user import Role, User


class RoleServiceException(Exception):
    def __init__(self, message, http_code=None):
        super().__init__(message)
        self.http_code = http_code


class RoleService:

    def get_role(self, name):
        schema = RoleSchema()
        role = Role.query.filter_by(name=name).first()
        return {'role': schema.dump(role)}

    def update_role(self, name):
        schema = RoleSchema(partial=True)
        role = Role.query.filter_by(name=name).first()
        role = schema.load(name, instance=role)

        db.session.commit()
        return schema.dump(role)

    def delete_role(self, name):
        role = Role.query.filter_by(name=name).first()
        db.session.delete(role)
        db.session.commit()

    def get_roles(self):
        schema = RoleSchema(many=True)
        roles = Role.query.all()
        return schema.dump(roles)

    def create_role(self, new_role):
        schema = RoleSchema()
        role = schema.load(new_role)

        existing_role = Role.query.filter_by(name=role.name).first()
        if existing_role:
            raise RoleServiceException('Role already exist!', http_code=CONFLICT)

        db.session.add(role)
        db.session.commit()

        return {'msg': 'Role created.', 'role': schema.dump(role)},

    def add_role_to_user(self, user_uuid: str, role_uuid: str):
        user = User.query.get_or_404(user_uuid)
        role = Role.query.get_or_404(role_uuid)
        user.roles.append(role)

        db.session.add(user)
        db.session.commit()

        return user.roles

    def remove_user_role(self, user_uuid: str, role_uuid: str):
        user = User.query.get_or_404(user_uuid)
        role = Role.query.get_or_404(role_uuid)

        if role in user.roles:
            user.roles.remove(role)
        else:
            raise RoleServiceException('The user does not have this role.', http_code=CONFLICT)

        db.session.add(user)
        db.session.commit()

        return user.roles

    def get_user_roles(self, user_uuid: str):
        user = User.query.get_or_404(user_uuid)
        return user.roles
