from http.client import CREATED, BAD_REQUEST

from flask import request
from flask_jwt_extended import get_jwt, jwt_required
from flask_restful import Resource

from auth_api.commons.jwt_utils import (
    user_has_role,
)
from auth_api.services.user_service import UserService, UserServiceException

user_service = UserService()


class MeResource(Resource):
    """Ресурс представляющий текущего пользователя (на основе access-токена).

    ---
    get:
      tags:
        - api/users/me
      summary: Получить данные о себе.
      description: Возвращает данные о текущем пользователе на основе access-токена.
      responses:
        200:
          description: Успех
          content:
            application/json:
              schema:
                  type: object
                  properties:
                    user: UserSchema
        401:
          $ref: '#/components/responses/Unauthorized'
        429:
          $ref: '#/components/responses/TooManyRequests'
    put:
      tags:
        - api/users/me
      summary: Обновить свои данные (username, password, email).
      description: Обновляет данные текущего пользователя на основе access-токена.
      requestBody:
        content:
          application/json:
            schema:
              UserSchema
      responses:
        200:
          description: Успех
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: Update is successful. Please use new access_token.
                  user: UserSchema
                  access_token:
                    type: string
                    example: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1...
        400:
          $ref: '#/components/responses/BadRequest'
        401:
          $ref: '#/components/responses/Unauthorized'
        429:
          $ref: '#/components/responses/TooManyRequests'
    delete:
      tags:
        - api/users/me
      summary: Удалить (заблокировать) свой аккаунт.
      description: Удаляет (блокирует) аккаунт на основе access-токена.
      responses:
        200:
          description: Успех
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: Your account has been blocked.
        400:
          $ref: '#/components/responses/BadRequest'
        401:
          $ref: '#/components/responses/Unauthorized'
        429:
          $ref: '#/components/responses/TooManyRequests'
    """

    method_decorators = [jwt_required()]

    def get(self):
        access_token = get_jwt()
        user_data = {
            'uuid': access_token['user_uuid'],
            'username': access_token['username'],
            'email': access_token['email'],
            'is_superuser': access_token['is_superuser'],
            'created_at': access_token['created_at'],
            'roles': access_token['roles'],
        }
        return {'user': user_data}

    def put(self):
        access_token = get_jwt()

        email = request.json.get('email')
        username = request.json.get('username')
        password = request.json.get('password')
        if not any([email, username, password]):
            return {'msg': 'At least one field - email, username or password must be filled.'}, BAD_REQUEST
        try:
            user, new_access_token = user_service.update_current_user(access_token, email, username, password)
            return {
                'msg': 'Update is successful. Please use new access_token.',
                'user': user,
                'access_token': new_access_token,
            }
        except UserServiceException as e:
            return {'msg': str(e)}, e.http_code

    def delete(self):
        access_token = get_jwt()
        user_service.delete_current_user(access_token)
        return {'msg': 'Your account has been blocked.'}


class UserResource(Resource):
    """Ресурс представляющий единичного пользователя.

    ---
    get:
      tags:
        - api/users
      summary: Получить данные о пользователе.
      description: Возвращает данные о пользователе по его UUID.
      parameters:
        - in: path
          name: user_uuid
          schema:
            type: string
      responses:
        200:
          description: Успех
          content:
            application/json:
              schema:
                type: object
                properties:
                  user: UserSchema
        400:
          $ref: '#/components/responses/BadRequest'
        401:
          $ref: '#/components/responses/Unauthorized'
        403:
          $ref: '#/components/responses/AccessDenied'
        404:
          $ref: '#/components/responses/NotFound'
        429:
          $ref: '#/components/responses/TooManyRequests'
    put:
      tags:
        - api/users
      summary: Обновить данные пользователя (username, password, email).
      description: Обновляет данные пользователя по его UUID.
      parameters:
        - in: path
          name: user_uuid
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              UserSchema
      responses:
        200:
          description: Успех
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: user updated
                  user: UserSchema
        400:
          $ref: '#/components/responses/BadRequest'
        401:
          $ref: '#/components/responses/Unauthorized'
        403:
          $ref: '#/components/responses/AccessDenied'
        404:
          $ref: '#/components/responses/NotFound'
        429:
          $ref: '#/components/responses/TooManyRequests'
    delete:
      tags:
        - api/users
      summary: Удалить (заблокировать) пользователя.
      description: Удаляет (блокирует) аккаунт по его UUID.
      parameters:
        - in: path
          name: user_uuid
          schema:
            type: string
      responses:
        200:
          description: Успех
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: User has been blocked.
        400:
          $ref: '#/components/responses/BadRequest'
        401:
          $ref: '#/components/responses/Unauthorized'
        403:
          $ref: '#/components/responses/AccessDenied'
        404:
          $ref: '#/components/responses/NotFound'
        409:
          description: Пользователь уже удален (заблокирован).
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: The user is already blocked.
        429:
          $ref: '#/components/responses/TooManyRequests'
    """

    @user_has_role('administrator', 'editor')
    def get(self, user_uuid):
        try:
            user = user_service.get_user(user_uuid)
            return {'user': user}
        except UserServiceException as e:
            return {'msg': str(e)}, e.http_code

    @user_has_role('administrator')
    def put(self, user_uuid):
        email = request.json.get('email')
        username = request.json.get('username')
        password = request.json.get('password')
        if not any([email, username, password]):
            return {'msg': 'At least one field - email, username or password must be filled.'}, BAD_REQUEST
        try:
            user = user_service.update_user(user_uuid, email, username, password)
            return {'msg': 'Update is successful.', 'user': user}
        except UserServiceException as e:
            return {'msg': str(e)}, e.http_code

    @user_has_role('administrator')
    def delete(self, user_uuid):
        try:
            user_service.delete_user(user_uuid)
            return {'msg': 'User has been blocked.'}
        except UserServiceException as e:
            return {'msg': str(e)}, e.http_code


class UserList(Resource):
    """Ресурс создания и получения списка всех пользователей.

    ---
    get:
      tags:
        - api/users
      summary: Получить список пользователей.
      description: Возвращает список всех активных пользователей из базы.
      responses:
        200:
          description: Успех
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/PaginatedResult'
                  - type: object
                    properties:
                      results:
                        type: array
                        items:
                          $ref: '#/components/schemas/UserSchema'
        401:
          $ref: '#/components/responses/Unauthorized'
        403:
          $ref: '#/components/responses/AccessDenied'
        429:
          $ref: '#/components/responses/TooManyRequests'
    post:
      tags:
        - api/users
      summary: Создать нового пользователя.
      description: Создает нового пользователя на основе переданных данных.
      requestBody:
        content:
          application/json:
            schema:
              UserSchema
      responses:
        201:
          description: Объект создан
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
        401:
          $ref: '#/components/responses/Unauthorized'
        403:
          $ref: '#/components/responses/AccessDenied'
        409:
          description: Пользователь уже существует.
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: Username or email is already taken!
        429:
          $ref: '#/components/responses/TooManyRequests'
    """

    @user_has_role('administrator', 'editor')
    def get(self):
        users_list = user_service.get_users_list()
        return users_list

    @user_has_role('administrator')
    def post(self):
        email = request.json.get('email')
        username = request.json.get('username')
        password = request.json.get('password')
        if not any([email, username, password]):
            return {'msg': 'Email, username and password must be filled.'}, BAD_REQUEST
        try:
            user = user_service.create_user(email, username, password)
            return {'msg': 'User created.', 'user': user}, CREATED
        except UserServiceException as e:
            return {'msg': str(e)}, e.http_code
