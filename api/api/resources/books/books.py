# -*- coding: utf-8 -*-
from flask import url_for, request, g, jsonify, make_response
from flask.ext.restful import reqparse, abort
from sqlalchemy.sql import text
from sqlalchemy import and_, or_, not_, func, CHAR, literal
from api.models import *
from api.core import db
from api.resources import Resource
import math


class BookCollection(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        super(BookCollection, self).__init__()

    def get(self):
        page = 0
        limit_row = 15
        response = dict(data=[])
        self.parser.add_argument('pages', type=str, required=False,
                                 location='args')
        self.parser.add_argument('limit', type=str, required=False,
                                 location='args')
        self.parser.add_argument('sortField', type=str, required=False,
                                 location='args')
        self.parser.add_argument('sortDirection', type=str, required=False,
                                 location='args')

        q = self.parser.parse_args()

        if q.pages:
            page = int(q.pages)

        if q.limit:
            limit_row = int(q.limit)

        query = db.session.query(
            Book.id,
            Book.name,
            Book.description,
            Book.user_id,
            User.email,
        ).outerjoin(
            User, User.id == Book.user_id
        )

        if q.sortField == 'name':
            if q.sortDirection == 'asc':
                query = query.order_by(Book.name.asc())
            else:
                query = query.order_by(Book.name.desc())
        if q.sortField == 'user_id':
            if q.sortDirection == 'asc':
                query = query.order_by(Book.user_id.asc())
            else:
                query = query.order_by(Book.user_id.desc())
        if q.sortField == 'description':
            if q.sortDirection == 'asc':
                query = query.order_by(Book.description.asc())
            else:
                query = query.order_by(Book.description.desc())
        else:
            query = query.order_by(Book.id.asc())

        query = query.limit(limit_row).offset(int(page) * limit_row).all()
        response['data'] = query
        response['total'] = Book.query.count()
        response['pages'] = int(
            math.ceil(Book.query.count() / float(limit_row))
        )
        return response

    def post(self):
        response = dict(data=[])
        data = request.json
        if data:
            book = Book()
            book.name = data['name']
            book.description = data['description']
            book.name = data['name']
            book.user_id = 4
            book.save()
            response['status_code'] = 201
            response['message'] = 'Created ok'
        return response


class BookResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        super(BookResource, self).__init__()

    def get(self, id):
        response = dict(data=[])
        book = db.session.query(
            Book.id,
            Book.name,
            Book.description,
            Book.user_id,
            User.email,
        ).outerjoin(
            User, User.id == Book.user_id
        ).filter(id == id)
        response['data'] = book.first()
        response['status'] = 200
        return response
