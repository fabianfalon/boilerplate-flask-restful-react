# -*- coding: utf-8 -*-

from flask import url_for, request, g, make_response, jsonify

from flask.ext import restful
from flask.ext.restful import reqparse, abort

from api.models import *
from api.core import db
from flask.ext.httpauth import HTTPBasicAuth

from api.resources import Resource


class StatusResource(Resource):

    def get(self):
        response = make_response(
            jsonify({"message": "valid session"}))
        response.status_code = 200
        return response
