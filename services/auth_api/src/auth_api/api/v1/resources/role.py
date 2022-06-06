from http.client import CREATED

from flask import request
from flask_restful import Resource

from auth_api.commons.jwt_utils import user_has_role
from auth_api.services.role_service import RoleService, RoleServiceException

role_service = RoleService()


class RoleResource(Resource):
    """Ресурс представляющий роль пользователя.

    ---
    get:
      tags:
        - api/roles
      summary: Получить данные о роли.
      description: Возвращает данные о роли по ее UUID.
      parameters:
        - in: path
          name: role_uuid
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
                  role: RoleSchema
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
        - api/roles
      summary: Обновить данные роли.
      description: Обновляет данные роли по ее UUID.
      parameters:
        - in: path
          name: role_uuid
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              RoleSchema
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
                    example: Role updated.
                  role: RoleSchema
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
        - api/roles
      summary: Удалить роль.
      description: Удаляет роль по ее UUID.
      parameters:
        - in: path
          name: role_uuid
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
                    example: Role deleted.
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
    """

    @user_has_role('administrator', 'editor')
    def get(self, role_uuid):
        role = role_service.get_role(role_uuid)
        return {'role': role}

    @user_has_role('administrator')
    def put(self, role_uuid):
        new_name = request.json.get("name")
        role = role_service.update_role(role_uuid, new_name)

        return {'msg': 'Role updated.', 'role': role}

    @user_has_role('administrator')
    def delete(self, role_uuid):
        role_service.delete_role(role_uuid)

        return {'msg': 'Role deleted.'}


class RoleList(Resource):
    """Ресурс создания и получения списка всех ролей.

    ---
    get:
      tags:
        - api/roles
      summary: Получить список ролей.
      description: Возвращает список всех ролей из базы.
      responses:
        200:
          description: Успех
          content:
            application/json:
              schema:
                type: object
                properties:
                  results:
                    type: array
                    items:
                      $ref: '#/components/schemas/RoleSchema'
        401:
          $ref: '#/components/responses/Unauthorized'
        403:
          $ref: '#/components/responses/AccessDenied'
        429:
          $ref: '#/components/responses/TooManyRequests'
    post:
      tags:
        - api/roles
      summary: Создать новую роль.
      description: Создает новую роль.
      requestBody:
        content:
          application/json:
            schema:
              RoleSchema
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
                    example: Role created.
                  role: RoleSchema
        400:
          $ref: '#/components/responses/BadRequest'
        401:
          $ref: '#/components/responses/Unauthorized'
        403:
          $ref: '#/components/responses/AccessDenied'
        409:
          description: Роль уже существует.
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: Role already exist!
        429:
          $ref: '#/components/responses/TooManyRequests'
    """

    @user_has_role('administrator', 'editor')
    def get(self):
        roles = role_service.get_roles()
        # roles = role_service.roll()

        return {'roles': roles}

    @user_has_role('administrator')
    def post(self):
        name = request.json.get("name")
        try:
            role = role_service.create_role(name)
            return {'msg': 'Role created.', 'role': role}, CREATED
        except RoleServiceException as e:
            return {'msg': str(e)}, e.http_code
