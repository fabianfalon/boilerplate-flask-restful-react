# -*- coding: utf-8 -*-
import logging

from flask import url_for, request, g, make_response, jsonify
from flask.ext.restful import reqparse, abort
import traceback, sys
from api.models import *
from api.core import db
from api.utils import *
from api.resources import Resource
import json


class Resource(Resource):
    pass

    def __init__(self):
        self.logger = logging.getLogger('users.' + __name__)
        super(Resource, self).__init__()


class UserCollection(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        super(UserCollection, self).__init__()

    def get(self):
        response = dict(data=[])
        if not is_user_admin(g.user_id):
            response['message'] = 'You do not have permissions'
            response['status_code'] = 401
            response['error'] = True
            return response
        query = db.session.query(
            User.active,
            User.created_at,
            User.email,
            User.first_name,
            User.id,
            User.last_name,
            User.role_id,
            Role.description.label('role_description')
        ).select_from(
            User
        ).outerjoin(
            Role, User.role_id == Role.id
        )
        response['data'] = query.all()
        return response

    def post(self):
        # Crear un nuvo usuario
        data = request.json
        response = dict(data=[])

        if is_user_admin(g.user_id) is False:
            response['message'] = 'You do not have permission to add new users'
            response['status_code'] = 401
            response['error'] = True
            logging.warning("""Se intento crear un usuario sin tener permisos de administrador""")
            return response
        email = data['email'].lower() if 'email' in data else None
        password = data['password'] if 'password' in data else None

        if email is None or password is None:
            response['message'] = 'Missing argument email or password'
            response['status_code'] = 400
            response['error'] = True
            logging.warning("""Se intento crear un nuevo usuario sin email o password""")
            return response
        exists = User.query.filter_by(email=email).first()
        if exists is not None:
            # existing user
            response = dict(data=[])
            response['message'] = 'User already exists'
            response['status_code'] = 400
            response['error'] = True
            logging.warning("""Se intento crear un usuario que ya existe""")
            return response
        user = User()
        user.email = email
        user.first_name = data['first_name'] if 'first_name' in data else None
        user.last_name = data['last_name'] if 'last_name' in data else None
        user.password = get_hmac(password)
        user.active = data['active'] if 'active' in data else False
        user.role_id = data['role_id'] if 'role_id' in data else 2
        try:
            user.save()
            response['message'] = 'The user was created successfully'
            response['status_code'] = 201
            logging.warning("""user: {}, created successfully""".format(
                email))
        except Exception as error:
            err, detail, tb = sys.exc_info()
            print(traceback.format_exc(tb))
            response['message'] = error.message
            response['status_code'] = 400
            response['error'] = True
            logging.warning("""Error al crear nuevo usuario: {},""".format(
                error.message))
        return response


class UserResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        super(UserResource, self).__init__()

    def get(self, user_id):
        response = dict(data=[])
        user = User.query.filter_by(id=user_id)
        if user:
            response['data'] = user.first()
            return response
        else:
            response['message'] = 'User does\'t exists'
            response['status_code'] = 400
            response['error'] = True
            return response

    def delete(self, user_id):
        # Eliminar un usuario existente
        response = dict(data=[])

        if is_user_admin(g.user_id) is False:
            response['message'] = 'You do not have permission to delete users'
            response['status_code'] = 401
            response['error'] = True
            logging.warning(
                """El usuario con id: {} intento eliminar un usuario sin tener permisos de admin""".format(
                    g.user_id, user_id))
            return response
        user = User.query.filter_by(id=user_id).first()
        if user:
            # obtenemos los registros para el user
            user_site_exists = UserSite.query.filter_by(
                user_id=user.id).all()
            if user_site_exists:
                # borramos los registros del usuario
                for old_user_site in user_site_exists:
                    old_user_site.delete()
            # Audit
            a = Audit(before=json.dumps(user.to_json()), after=None,
                      user_id=g.user_id,
                      action='d', object_type='user',
                      object_id=user.id)
            db.session.add(a)
            db.session.commit()
            user.delete()
            response['message'] = 'The user was deleted successfully'
            response['status_code'] = 200
            logging.warning("""El usuario con id: {} elimino el usuario: {}""".format(
                g.user_id, user_id))
            return response
        else:
            response['message'] = 'User does\'t exists'
            response['status_code'] = 400
            response['error'] = True
            return response

    def put(self, user_id):

        if is_user_admin(g.user_id) is False:
            response['message'] = 'You do not have permission to update users'
            response['status_code'] = 401
            response['error'] = True
            logging.warning(
                """El usuario con id: {} intento actualizar un usuario sin tener permisos de admin""".format(
                    user_info(request.headers.get('Authorization')),
                    user_id))
            return response
        user = User.query.get(user_id)
        before = json.dumps(user.to_json())
        data = request.json['data']['data']
        user.active = data['active']
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        if 'role_id' in data:
            user.role_id = data['role_id']
        if 'new_password' in data:
            user.password = get_hmac(data['new_password'])
        db.session.add(user)
        db.session.commit()
        after = json.dumps(user.to_json())
        response = make_response(
            jsonify({'message': 'User has been successfully modified'}))
        response.status_code = 200
        logging.warning("""Se mofico el usuario: {},""".format(
            user_id))
        # Audit
        a = Audit(before=before, after=after,
                  user_id=g.user_id,
                  action='u', object_type='user',
                  object_id=user.id)
        db.session.add(a)
        db.session.commit()
        return response

    def post(self):
        print request.json


class MeResource(Resource):

    def get(self):
        user = User.query.get(g.user_id)
        if user:
            return user
        else:
            return abort(400, **{'message': 'user does\'t exists', 'status': 400})


class RoleCollection(Resource):

    def get(self):
        roles = Role.query
        return roles.all()


from flask_restful import Resource
class UserPingCollection(Resource):
    def get(self):
        response = dict()
        response['message'] = 'pong'
        response['status_code'] = 200
        return response
