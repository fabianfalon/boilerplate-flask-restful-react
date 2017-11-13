# Token Auth functions
import jwt
from jwt import DecodeError, ExpiredSignature
from datetime import datetime, timedelta
from functools import wraps
from flask import g, Blueprint, jsonify, make_response, request
from flask_restful import Resource
import flask_restful
from api.settings import SECRET_KEY, PASSWORD_RESET_EMAIL
# from app.users.models import Users, UsersSchema
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from flask_mail import Mail, Message

from api.models import User
from api import settings


def parse_token(req):
    token = req.headers.get('Authorization').split()[1]
    # token = req.headers.get('Authorization')
    return jwt.decode(token, SECRET_KEY, algorithms='HS256')

# Login decorator function


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.headers.get('Authorization'):
            response = jsonify(message='Missing authorization header')
            response.status_code = 401
            return response

        try:
            payload = parse_token(request)
        except DecodeError:
            response = jsonify(message='Token is invalid')
            response.status_code = 401
            return response
        except ExpiredSignature:
            response = jsonify(message='Token has expired')
            response.status_code = 401
            return response

        g.user_id = payload['sub']

        return f(*args, **kwargs)

    return decorated_function

# JWT AUTh process end

# Login Authentication Class


class Resource(flask_restful.Resource):
    method_decorators = [login_required]
