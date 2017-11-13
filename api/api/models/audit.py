# -*- coding: utf-8 -*-
import sqlalchemy as sa

from api.core import db, BaseModel
from api.helpers import JsonSerializer

import datetime


class Audit(BaseModel, JsonSerializer):
    __tablename__ = 'audit'
    __json_public__ = ['id', 'object', 'object_id', 'user_id']

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    object_type = sa.Column(sa.String(30))
    object_id = sa.Column(sa.Integer)
    user_id = sa.Column(sa.Integer)
    before = sa.Column(sa.Text)
    after = sa.Column(sa.Text)
    date = sa.Column(sa.DateTime(), default=datetime.datetime.now)
    action = sa.Column(sa.CHAR(1))

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
