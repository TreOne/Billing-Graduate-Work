from http.client import BAD_REQUEST, CREATED

from flask import Blueprint
from flask import current_app as app
from flask import jsonify, request
from flask_jwt_extended import get_jwt, jwt_required
from marshmallow import ValidationError

from auth_api.api.v1.schemas.user import UserSchema
from auth_api.commons.jwt_utils import (
    create_tokens,
    deactivate_access_token,
    deactivate_all_refresh_tokens,
    deactivate_refresh_token,
    deactivate_refresh_token_by_access_token,
    get_user_uuid_from_token,
    is_active_token,
)
from auth_api.extensions import apispec, jwt
from auth_api.services.auth_service import AuthService, AuthServiceException

blueprint = Blueprint('auth', __name__, url_prefix='/auth/v1')
auth_service = AuthService()


@blueprint.route('/signup', methods=['POST'])
def signup():
    """Регистрация пользователя.

    ---
    post:
      tags:
        - auth
      summary: Регистрация пользователя.
      description: Создает пользователя в базе данных.
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                  example: CoolUser
                password:
                  type: string
                  example: Super$ecret!
                email:
                  type: string
                  example: user@example.com
      responses:
        201:
          description: Регистрация прошла успешно.
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: User created.
                  user: UserSchema
        400:
          $ref: '#/components/responses/BadRequest'
        409:
          description: Такое имя пользователя или email уже существуют.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorMessage'
        429:
          $ref: '#/components/responses/TooManyRequests'
      security: []
    """
    if not request.is_json:
        return jsonify({'msg': 'Missing JSON in request.'}), BAD_REQUEST

    schema = UserSchema()
    user = schema.load(request.json)
    username = user.username
    email = user.email
    password = user.password
    try:
        registered_user = auth_service.register_user(username, email, password)
        return {'msg': 'User created.', 'user': schema.dump(registered_user)}, CREATED
    except AuthServiceException as e:
        return {'msg': str(e)}, e.http_code


@blueprint.route('/login', methods=['POST'])
def login():
    """Аутентификация пользователя для получения токенов.

    ---
    post:
      tags:
        - auth
      summary: Аутентификация пользователя.
      description: Проверяет подлинность учетных данных пользователя и возвращает токены.
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                  example: CoolUser
                password:
                  type: string
                  example: Super$ecret!
                totp_code:
                  type: string
                  example: '123456'
              required:
                - username
                - password
      responses:
        200:
          description: Аутентификация прошла успешно.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Tokens'
        400:
          $ref: '#/components/responses/BadRequest'
        403:
          $ref: '#/components/responses/AccessDenied'
        429:
          $ref: '#/components/responses/TooManyRequests'
      security: []
    """
    if not request.is_json:
        return jsonify({'msg': 'Missing JSON in request'}), BAD_REQUEST
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    totp_code = request.json.get('totp_code', '')

    try:
        access_token, refresh_token = auth_service.get_tokens(username, password, totp_code)
        user_uuid = get_user_uuid_from_token(refresh_token)
        user_agent = request.user_agent.string
        ip_address = request.remote_addr
        auth_service.add_to_history(user_uuid, user_agent, ip_address)
        return jsonify({'access_token': access_token, 'refresh_token': refresh_token})
    except AuthServiceException as e:
        return {'msg': str(e)}, e.http_code


@blueprint.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Получение новой пары токенов с помощью refresh-токена.

    ---
    post:
      tags:
        - auth
      summary: Получение новой пары токенов.
      description: Возвращает новую пару токенов с помощью refresh-токена переданного в заголовке `Authorization`.
      responses:
        200:
          description: Обновление токенов прошло успешно.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Tokens'
        400:
          $ref: '#/components/responses/BadRequest'
        401:
          $ref: '#/components/responses/Unauthorized'
        429:
          $ref: '#/components/responses/TooManyRequests'
    """
    refresh_token = get_jwt()
    user_uuid = get_user_uuid_from_token(refresh_token)

    deactivate_refresh_token(refresh_token)

    access_token, refresh_token = create_tokens(user_uuid)
    ret = {'access_token': access_token, 'refresh_token': refresh_token}
    return jsonify(ret)


@blueprint.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Выход из аккаунта.

    ---
    post:
      tags:
        - auth
      summary: Выход из аккаунта.
      description: Отзыв access и refresh токена.
      responses:
        200:
          description: Выход успешно осуществлен.
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: You have been logged out.
        400:
          $ref: '#/components/responses/BadRequest'
        401:
          $ref: '#/components/responses/Unauthorized'
        429:
          $ref: '#/components/responses/TooManyRequests'
    """
    access_token = get_jwt()
    deactivate_access_token(access_token)
    deactivate_refresh_token_by_access_token(access_token)

    return jsonify({'msg': 'You have been logged out.'})


@blueprint.route('/logout_all', methods=['POST'])
@jwt_required()
def logout_all():
    """Выход из всех аккаунтов.

    ---
    post:
      tags:
        - auth
      summary: Выход из всех аккаунтов
      description: Отзыв всех токенов авторизации.
      responses:
        200:
          description: Выход успешно осуществлен.
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: You have been logged out from all devices.
        400:
          $ref: '#/components/responses/BadRequest'
        401:
          $ref: '#/components/responses/Unauthorized'
        429:
          $ref: '#/components/responses/TooManyRequests'
    """
    access_token = get_jwt()
    deactivate_access_token(access_token)
    user_uuid = get_user_uuid_from_token(access_token)
    deactivate_all_refresh_tokens(user_uuid)
    return jsonify({'msg': 'You have been logged out from all devices.'})


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    return not is_active_token(jwt_payload)


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Возвращает json-ошибку при ошибках валидации marshmallow.

    Это позволит избежать необходимости оборачивать в try/catch ошибки ValidationErrors во всех ендпоинтах, возвращая
    корректный json-ответ со статусом 400 (Bad Request).
    """
    return jsonify(e.messages), BAD_REQUEST


@blueprint.before_app_first_request
def register_views():
    apispec.spec.path(view=signup, app=app)
    apispec.spec.path(view=login, app=app)
    apispec.spec.path(view=refresh, app=app)
    apispec.spec.path(view=logout, app=app)
    apispec.spec.path(view=logout_all, app=app)
