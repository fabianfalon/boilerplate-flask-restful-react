# -*- coding: utf-8 -*-
import datetime
import logging
from flask import request, jsonify, make_response
from flask_restful import Resource

from api.models import *
from api.settings import SECRET_KEY
import jwt


def create_token(user):
    payload = {
        'sub': user.id,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'scope': user.roles
    }
    token = jwt.encode(payload, SECRET_KEY)
    return token.decode('unicode_escape')


class AuthResource(Resource):

    def post(self):
        data = request.get_json(force=True)
        email = data['email']
        password = data['password']
        user = User.query.filter_by(email=email).first()

        if not user:
            response = make_response(
                jsonify({"email": "email does not exists"}))
            response.status_code = 401
            return response
        if user.active is False:
            response = make_response(
                jsonify({"password": "Your user is not active"}))
            response.status_code = 401
            logging.warning("user: {}, invalid password".format(
                data['email']))
            return response
        if user.check_password(password):
            token = create_token(user)
            logging.info("user: {}".format(data['email']))
            user.registration_token = token
            user.save()
            return {'token': token}
        else:
            response = make_response(jsonify({"password": "invalid password"}))
            response.status_code = 401
            logging.warning("user: {}, invalid password".format(data['email']))
            return response
