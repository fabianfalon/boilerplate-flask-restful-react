# -*- coding: utf-8 -*-
from flask_security import UserMixin, RoleMixin
from flask import current_app as app

import sqlalchemy as sa

from api.core import db, BaseModel, limits
from api.helpers import JsonSerializer
from api import settings

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

from passlib.context import CryptContext
import base64
import hashlib
import hmac

import datetime
from flask import current_app
from dateutil.tz import tzlocal
from dateutil.relativedelta import relativedelta

pwd_context = CryptContext(schemes='sha512_crypt', default='sha512_crypt')


def get_hmac(passwd):
    h = hmac.new(
        current_app.config['SECURITY_PASSWORD_SALT'].encode('utf-8'),
        passwd.encode('utf-8'), hashlib.sha512
    )
    return base64.b64encode(h.digest())

users_roles = sa.Table(
    'users_roles',
    BaseModel.metadata,
    sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id')),
    sa.Column('role_id', sa.Integer(), sa.ForeignKey('roles.id'))
)


class Role(RoleMixin, JsonSerializer, BaseModel):
    __tablename__ = 'roles'

    __json_public__ = ['id', 'name', 'description']

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(80), unique=True)
    description = sa.Column(sa.String(255))

    def __eq__(self, other):
        return (self.name == other or
                self.name == getattr(other, 'name', None))

    def __ne__(self, other):
        return (self.name != other and
                self.name != getattr(other, 'name', None))

    def __hash__(self):
        return hash(self.name)

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()

    @property
    def role_id(self):
        return self.id


class User(JsonSerializer, UserMixin, BaseModel):
    __tablename__ = 'users'
    __json_public__ = ['id', 'email', 'first_name', 'last_name',
                       'verified', 'active', 'name', 'comments', 'role_id']

    id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.String(255), unique=True)
    password = sa.Column(sa.String(120))
    first_name = sa.Column(sa.String(255))
    last_name = sa.Column(sa.String(255))
    verified = sa.Column(sa.Boolean())
    active = sa.Column(sa.Boolean())
    registration_token = sa.Column(sa.String(255))

    login_count = sa.Column(sa.Integer)

    created_at = sa.Column(sa.DateTime(), default=datetime.datetime.now())
    updated_at = sa.Column(sa.DateTime(), default=datetime.datetime.now())
    registered_at = sa.Column(sa.DateTime())
    confirmed_at = sa.Column(sa.DateTime())
    current_login_at = sa.Column(sa.DateTime())
    last_login_at = sa.Column(sa.DateTime())

    last_login_ip = sa.Column(sa.String(30))
    current_login_ip = sa.Column(sa.String(30))

    roles = db.relationship('Role', secondary=users_roles,
                            backref=db.backref('users', lazy='dynamic'))
    role_id = sa.Column(sa.Integer)
    comments = sa.Column(sa.Text(300, collation='utf8_unicode_ci'))

    _my_permissions = -1

    @property
    def name(self):
        return (self.first_name and self.first_name) and u"{0} {1}".format(
            self.first_name, self.last_name
        )

    @property
    def user_id(self):
        return self.id

    def find(self, **kwargs):
        return self.query.filter_by(**kwargs)

    def first(self, **kwargs):
        self.find(**kwargs).first()

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()

    def check_password(self, password):
        password = get_hmac(password)
        # return pwd_context.verify(password, self.password)
        return (password == self.password)

    def is_admin(self):
        return (self.role_id == 1)
