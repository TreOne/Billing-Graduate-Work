from http.client import CONFLICT

from auth_api.api.v1.schemas.role import RoleSchema
from auth_api.database import session
from auth_api.models.user import Role
from auth_api.services.exceptions import ServiceException


class RoleServiceException(ServiceException):
    pass


class RoleService:

    def get_role(self, role_uuid: str):
        schema = RoleSchema()
        role = session.query(Role).get(role_uuid)
        return schema.dump(role)

    def update_role(self, role_uuid: str, new_name: str):
        schema = RoleSchema()
        role = session.query(Role).get(role_uuid)
        role.name = new_name

        session.commit()
        return schema.dump(role)

    def delete_role(self, role_uuid: str):
        role = session.query(Role).get(role_uuid)
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

        return schema.dump(role)
