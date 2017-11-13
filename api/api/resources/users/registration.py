# -*- coding: utf-8 -*-
import logging
import base64
import datetime

from flask import url_for, request, g
from flask.ext import restful
from flask.ext.restful import reqparse, abort

from api.models import *
from api.core import db
from flask.ext.httpauth import HTTPBasicAuth

from api.resources import Resource


class Resource(Resource):
    pass

    def __init__(self):
        self.logger = logging.getLogger('users.' + __name__)
        super(Resource, self).__init__()


class RegistrationResource(Resource):

    def get(self, token):
        try:
            token = base64.b64decode(token)
            token = UserRegistrationToken.query.filter_by(registration_token=token).first()
            return dict(data=token)
        except Exception as error:
            err, detail, tb = sys.exc_info()
            print(traceback.format_exc(tb))
            raise


class ValidateRegistrationVerb(Resource):

    def get(self, token):
        try:
            token = base64.b64decode(token)
            token = UserRegistrationToken.query.filter_by(registration_token=token).first()
            return dict(data=token)
        except Exception as error:
            err, detail, tb = sys.exc_info()
            print(traceback.format_exc(tb))
            raise


class PreRegistrationValidationResource(Resource):

    def put(self, token):
        try:
            post = request.json
            token = base64.b64decode(token)
            token = UserRegistrationToken.query.filter_by(registration_token=token).first()

            first_name = post.get('first_name')
            last_name = post.get('last_name')
            role = post.get('role')
            password = post.get('password')
            email = post.get('email')
            id_number = post.get('id_number')
            birthday = post.get('birthday')
            print post
            assert all((email,
                        first_name, last_name,
                        password, role, token,
                        id_number, birthday))

            # Constraints del token
            assert token.expiration_date > datetime.datetime.now()
            assert token.registration_token

            # Constraints del usuario
            user = User.query.filter_by(email=email).first()

            # assert user.active != True, "El usuario ya está activado"
            profile = user.get_profile(role)
            assert profile, "El profile del usuario %s (%s) no existe" % \
                (user.user_id, user.email)
            # assert profile.active != True, "El perfil del usuario ya está activado"

            now = datetime.datetime.now()
            password = get_hmac(password)

            user.first_name = first_name
            user.last_name = last_name
            user.password = password
            user.id_number = id_number
            user.birthday = birthday
            user.last_updated_at = now
            user.validated = True
            user.validated_at = now
            user.active = True
            user.save()

            profile.updated_by = profile.id
            profile.is_active = True
            profile.save()

            return dict(message=u"El usuario ha sido registrado con éxito")
        except Exception as error:
            err, detail, tb = sys.exc_info()
            print(traceback.format_exc(tb))
            return dict(error=error.message), 403

