# -*- coding: utf-8 -*-
import sqlalchemy as sa

from api.core import db, BaseModel
from api.helpers import JsonSerializer


class Book(BaseModel, JsonSerializer):
    """ class Book"""
    __tablename__ = 'books'
    __json_public__ = ['id', 'name', 'description', 'user_id']

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(125))
    description = sa.Column(sa.String(125))
    user_id = sa.Column(sa.Integer)

    def save(self, commit=True):
        """ save """
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
