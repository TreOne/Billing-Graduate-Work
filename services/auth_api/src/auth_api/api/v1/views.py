from http.client import BAD_REQUEST, METHOD_NOT_ALLOWED

from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required
from flask_restful import Api
from marshmallow import ValidationError

from auth_api.api.v1.resources.role import RoleList, RoleResource
from auth_api.api.v1.resources.user import MeResource, UserList, UserResource
from auth_api.api.v1.schemas.auth_history import AuthHistorySchema
from auth_api.api.v1.schemas.role import RoleSchema
from auth_api.api.v1.schemas.totp_request import TOTPRequestSchema
from auth_api.api.v1.schemas.user import UserSchema
from auth_api.commons.jwt_utils import get_user_uuid_from_token, user_has_role
from auth_api.commons.pagination import paginate
from auth_api.exeptions import UserServiceException
from auth_api.extensions import apispec
from auth_api.services.user_service import UserService

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)
user_service = UserService()

api.add_resource(MeResource, '/users/me', endpoint='current_user')
api.add_resource(UserResource, '/users/<uuid:user_uuid>', endpoint='user_by_uuid')
api.add_resource(UserList, '/users', endpoint='users')

api.add_resource(RoleResource, '/roles/<uuid:role_uuid>', endpoint='role_by_uuid')
api.add_resource(RoleList, '/roles', endpoint='roles')


@blueprint.route('/users/me/history', methods=['GET'])
@jwt_required()
def get_self_history():
    """Получение истории своих логинов.

    ---
    get:
      tags:
        - api/users/me
      summary: Получение истории своих логинов.
      description: Возвращает список всех своих логинов.
      responses:
        200:
          description: История логинов получена успешно.
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/PaginatedResult'
                  - type: object
                    properties:
                      results:
                        type: array
                        items: AuthHistorySchema
        401:
          $ref: '#/components/responses/Unauthorized'
    """
    token = get_jwt()
    user_uuid = token['user_uuid']
    auth_history = user_service.get_auth_history(user_uuid)

    schema = AuthHistorySchema(many=True)

    return paginate(auth_history, schema)


@blueprint.route('/users/me/totp/link', methods=['GET'])
@jwt_required()
def get_totp_link():
    """Получение totp ссылки.

    ---
    get:
      tags:
        - api/users/me/totp
      summary: Получение totp ссылки.
      description: Возвращает totp_link.
      responses:
        200:
          description: totp_link получена успешно.
          content:
            application/json:
              schema:
                type: object
                properties:
                  totp_link:
                    type: string
                    example: otpauth://totp/PractixMovie:admin?secret=33HCRQNTDON7YD...
        401:
          $ref: '#/components/responses/Unauthorized'
        429:
          $ref: '#/components/responses/TooManyRequests'
    """
    token = get_jwt()
    user_uuid = get_user_uuid_from_token(token)

    provisioning_url = user_service.get_user_totp_link(user_uuid)

    return {'totp_link': provisioning_url}


@blueprint.route('/users/me/totp/change_status', methods=['PUT'])
@jwt_required()
def change_totp_status():
    """Изменение статуса двухфакторной аутентификации.

    ---
    put:
      tags:
        - api/users/me/totp
      summary: Активация, деактивация totp.
      description: Позволяет включить или выключить двухфакторную аутентификацию.
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                totp_code:
                  type: string
                  example: '123456'
                totp_status:
                  type: boolean
      responses:
        200:
          description: totp_status изменён успешно.
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: Totp status changed.
        400:
          $ref: '#/components/responses/BadRequest'
        401:
          $ref: '#/components/responses/Unauthorized'
        409:
          description: Данный статус уже установлен.
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: This status has already been established.
        429:
          $ref: '#/components/responses/TooManyRequests'
    """
    token = get_jwt()
    user_uuid = get_user_uuid_from_token(token)
    schema = TOTPRequestSchema()
    totp_request = schema.load(request.json)

    try:
        totp_status = user_service.change_user_totp_status(user_uuid, totp_request)
        return {'msg': f'Totp status changed to: {totp_status}'}
    except UserServiceException as e:
        return {'msg': str(e)}, e.http_code


@blueprint.route('/users/<uuid:user_uuid>/history', methods=['GET'])
@user_has_role('administrator', 'editor')
def get_user_history(user_uuid):
    """Получение истории логинов пользователя.

    ---
    get:
      tags:
        - api/users
      summary: Получение истории логинов пользователя.
      description: Возвращает список всех логинов конкретного пользователя заданного по `uuid`.
      parameters:
        - in: path
          name: user_uuid
          schema:
            type: string
      responses:
        200:
          description: История логинов получена успешно.
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/PaginatedResult'
                  - type: object
                    properties:
                      results:
                        type: array
                        items: AuthHistorySchema
        400:
          $ref: '#/components/responses/BadRequest'
        401:
          $ref: '#/components/responses/Unauthorized'
        403:
          $ref: '#/components/responses/AccessDenied'
        429:
          $ref: '#/components/responses/TooManyRequests'
    """
    auth_history = user_service.get_auth_history(user_uuid)
    schema = AuthHistorySchema(many=True)

    return paginate(auth_history, schema)


@blueprint.route('/users/me/roles', methods=['GET'])
@jwt_required()
def get_self_roles():
    """Получение списка своих ролей.

    ---
    get:
      tags:
        - api/users/me
      summary: Получение списка своих ролей.
      description: Возвращает список всех своих ролей.
      responses:
        200:
          description: Список ролей получен успешно.
          content:
            application/json:
              schema:
                type: object
                properties:
                  roles:
                    type: array
                    items: RoleSchema
        401:
          $ref: '#/components/responses/Unauthorized'
        429:
          $ref: '#/components/responses/TooManyRequests'
    """
    token = get_jwt()
    roles = token['roles']
    return {'roles': roles}


@blueprint.route('/users/<uuid:user_uuid>/roles', methods=['GET'])
@user_has_role('administrator', 'editor')
def get_user_roles(user_uuid):
    """Получение ролей пользователя.

    ---
    get:
      tags:
        - api/users
      summary: Получение ролей пользователя.
      description: Возвращает список ролей конкретного пользователя заданного по `uuid`.
      parameters:
        - in: path
          name: user_uuid
          schema:
            type: string
      responses:
        200:
          description: Список ролей успешно получен.
          content:
            application/json:
              schema:
                type: object
                properties:
                  roles:
                    type: array
                    items: RoleSchema
        400:
          $ref: '#/components/responses/BadRequest'
        401:
          $ref: '#/components/responses/Unauthorized'
        403:
          $ref: '#/components/responses/AccessDenied'
        429:
          $ref: '#/components/responses/TooManyRequests'
    """

    roles = user_service.get_roles(user_uuid)
    schema = RoleSchema(many=True)

    return {'roles': schema.dump(roles)}


@blueprint.route('/users/<uuid:user_uuid>/roles/<uuid:role_uuid>', methods=['PUT', 'DELETE'])
@user_has_role('administrator')
def user_roles(user_uuid, role_uuid):
    """Изменение ролей пользователя.

    ---
    put:
      tags:
        - api/users
      summary: Добавление роли пользователю.
      description: Позволяет добавлять роли пользователю.
      parameters:
        - in: path
          name: user_uuid
          schema:
            type: string
        - in: path
          name: role_uuid
          schema:
            type: string
      responses:
        200:
          description: Добавление роли прошло успешно.
          content:
            application/json:
              schema:
                type: object
                properties:
                  roles:
                    type: array
                    items: RoleSchema
        400:
          $ref: '#/components/responses/BadRequest'
        401:
          $ref: '#/components/responses/Unauthorized'
        403:
          $ref: '#/components/responses/AccessDenied'
        429:
          $ref: '#/components/responses/TooManyRequests'
    delete:
      tags:
        - api/users
      summary: Удаление роли у пользователя.
      description: Позволяет удалить роль у пользователя.
      parameters:
        - in: path
          name: user_uuid
          schema:
            type: string
        - in: path
          name: role_uuid
          schema:
            type: string
      responses:
        200:
          description: Удаление роли прошло успешно.
          content:
            application/json:
              schema:
                type: object
                properties:
                  roles:
                    type: array
                    items: RoleSchema
        400:
          $ref: '#/components/responses/BadRequest'
        401:
          $ref: '#/components/responses/Unauthorized'
        403:
          $ref: '#/components/responses/AccessDenied'
        409:
          description: У данного пользователя нет этой роли.
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: The user does not have this role.
        429:
          $ref: '#/components/responses/TooManyRequests'
    """

    if request.method == 'PUT':
        roles = user_service.add_role(user_uuid, role_uuid)
    elif request.method == 'DELETE':
        roles = user_service.remove_role(user_uuid, role_uuid)
    else:
        return jsonify({'msg': 'Method not allowed.'}), METHOD_NOT_ALLOWED

    schema = RoleSchema(many=True)
    return {'roles': schema.dump(roles)}


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Возвращает json-ошибку при ошибках валидации marshmallow.

    Это позволит избежать необходимости оборачивать в try/catch ошибки ValidationErrors во всех ендпоинтах, возвращая
    корректный json-ответ со статусом 400 (Bad Request).
    """
    return jsonify(e.messages), BAD_REQUEST


@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema('TOTPRequestSchema', schema=TOTPRequestSchema)
    apispec.spec.components.schema('UserSchema', schema=UserSchema)
    apispec.spec.components.schema('RoleSchema', schema=RoleSchema)
    apispec.spec.path(view=MeResource, app=current_app)
    apispec.spec.path(view=UserResource, app=current_app)
    apispec.spec.path(view=UserList, app=current_app)
    apispec.spec.path(view=RoleResource, app=current_app)
    apispec.spec.path(view=RoleList, app=current_app)
    apispec.spec.path(view=get_self_history, app=current_app)
    apispec.spec.path(view=get_self_roles, app=current_app)
    apispec.spec.path(view=get_user_history, app=current_app)
    apispec.spec.path(view=get_user_roles, app=current_app)
    apispec.spec.path(view=get_totp_link, app=current_app)
    apispec.spec.path(view=change_totp_status, app=current_app)
    apispec.spec.path(view=user_roles, app=current_app)
