from http.client import BAD_REQUEST

from flask import Blueprint
from flask import current_app as app
from flask import jsonify, request
from marshmallow import ValidationError

from auth_api.commons.jwt_utils import create_tokens
from auth_api.exceptions import OAuthServiceException
from auth_api.extensions import apispec
from auth_api.services.auth_service import AuthService
from auth_api.services.oauth_service import OAuthService

blueprint = Blueprint('oauth', __name__, url_prefix='/oauth/v1')
auth_service = AuthService()
oauth_service = OAuthService()


@blueprint.route('/providers', methods=['GET'])
def get_providers_list():
    """Получение списка поддерживаемых провайдеров для OAuth авторизации.

    ---
    get:
      tags:
        - oauth
      summary: Список поддерживаемых OAuth-провайдеров.
      description: Получение списка поддерживаемых провайдеров и их данных для OAuth авторизации.
      responses:
        200:
          description: Список провайдеров успешно получен.
          content:
            application/json:
              schema:
                type: object
                properties:
                  providers:
                    type: array
                    items:
                      type: string
                      example: yandex
        429:
          $ref: '#/components/responses/TooManyRequests'
      security: []
    """
    providers_data = oauth_service.get_providers_list_oauth()
    return jsonify({'providers': providers_data})


@blueprint.route('/login/<string:provider>', methods=['POST'])
def oauth_login(provider):
    """Аутентификация с помощью токена полученного от OAuth-провайдера.

    ---
    post:
      tags:
        - oauth
      summary: OAuth аутентификация.
      description: Аутентификация с помощью токена полученного от OAuth-провайдера.
      parameters:
        - in: path
          name: provider
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                access_token:
                  type: string
                  example: AAAAAAA00000000000-AAAAAA00000000000000
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
        404:
          $ref: '#/components/responses/NotFound'
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

    try:
        social_id, email = oauth_service.get_user_info_from_oauth(provider)
        user_uuid = oauth_service.login_user_oauth(social_id, email)
        access_token, refresh_token = create_tokens(user_uuid)
        user_agent = request.user_agent.string
        ip_address = request.remote_addr
        auth_service.add_to_history(user_uuid, user_agent, ip_address)
        return jsonify({'access_token': access_token, 'refresh_token': refresh_token})
    except OAuthServiceException as e:
        return {'msg': str(e)}, e.http_code


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Возвращает json-ошибку при ошибках валидации marshmallow.

    Это позволит избежать необходимости оборачивать в try/catch ошибки ValidationErrors во всех ендпоинтах, возвращая
    корректный json-ответ со статусом 400 (Bad Request).
    """
    return jsonify(e.messages), BAD_REQUEST


@blueprint.before_app_first_request
def register_views():
    apispec.spec.path(view=get_providers_list, app=app)
    apispec.spec.path(view=oauth_login, app=app)
