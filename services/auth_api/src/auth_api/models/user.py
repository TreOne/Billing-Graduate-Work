import datetime
import uuid as uuid_

from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.ext.hybrid import hybrid_property

from auth_api.database import Base
from auth_api.extensions import pwd_context
from auth_api.models.custom_field_types import GUID
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship




class Role(Base):
    __tablename__ = 'roles'

    uuid = Column(GUID(), primary_key=True, default=uuid_.uuid4)
    name = Column(String(80), unique=True)

    def __repr__(self):
        return '<Role %s>' % self.name

class UsersRoles(Base):
    __tablename__ = 'links_users_roles'

    uuid = Column(GUID(), primary_key=True, default=uuid_.uuid4)
    users_uuid = Column(GUID(), ForeignKey('users.uuid'))
    roles_uuid = Column(GUID(), ForeignKey('roles.uuid'))
    date_expiration = Column(DateTime, default=None)


class User(Base):
    """Basic user model"""

    __tablename__ = 'users'

    uuid = Column(GUID(), primary_key=True, default=uuid_.uuid4)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(80), unique=True)
    _password = Column('password', String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    roles = relationship('Role', secondary='links_users_roles',
                         secondaryjoin=f"and_(UsersRoles.roles_uuid==Role.uuid, or_(UsersRoles.date_expiration==None, "
                                       f"UsersRoles.date_expiration>'{datetime.datetime.utcnow()}'))")
    is_totp_enabled = Column(Boolean, default=False, nullable=False)
    two_factor_secret = Column(String(255))
    social_id = Column(String(255))

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value: str):
        self._password = pwd_context.hash(value)

    def __repr__(self):
        return '<User %s>' % self.username


# class Role(Base):
#     __tablename__ = 'roles'
#
#     uuid = Column(GUID(), primary_key=True, default=uuid_.uuid4)
#     name = Column(String(80), unique=True)
#     data_expiration = Column(DateTime)
#
#     def __repr__(self):
#         return '<Role %s>' % self.name

#
# class UsersRoles(Base):
#     __tablename__ = 'links_users_roles'
#
#     uuid = Column(GUID(), primary_key=True, default=uuid_.uuid4)
#     users_uuid = Column(GUID(), ForeignKey('users.uuid'))
#     roles_uuid = Column(GUID(), ForeignKey('roles.uuid'))


def create_auth_partition(target, connection, **kw) -> None:
    connection.execute(
        """CREATE TABLE IF NOT EXISTS auth_history_desktop PARTITION OF auth_history FOR VALUES IN ('desktop');""",
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS auth_history_tablet PARTITION OF auth_history FOR VALUES IN ('tablet');""",
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS auth_history_mobile PARTITION OF auth_history FOR VALUES IN ('mobile');""",
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS auth_history_other PARTITION OF auth_history FOR VALUES IN ('other');""",
    )


class AuthHistory(Base):
    __tablename__ = 'auth_history'
    __table_args__ = (
        PrimaryKeyConstraint('uuid', 'device'),
        {
            'postgresql_partition_by': 'LIST (device)',
            'listeners': [('after_create', create_auth_partition)],
        },
    )

    uuid = Column(GUID(), default=uuid_.uuid4)
    user_uuid = Column(GUID(), ForeignKey('users.uuid'))
    user_agent = Column(String(200), nullable=False)
    device = Column(String(40), nullable=False)
    ip_address = Column(String(40), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)


# class UserSubscriptions(Model):
#     __tablename__ = 'subscriptions'
#
#     uuid = Column(GUID(), primary_key=True, default=uuid_.uuid4)
#     user_uuid = Column(GUID(), ForeignKey('users.uuid'))
#     name = Column(String(80))
#     data_expiration = Column(DateTime)
#
#
#     def __repr__(self):
#         return '<Subscription %s>' % self.name