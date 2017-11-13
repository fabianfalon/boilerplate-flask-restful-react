from api.helpers import JsonSerializer, JSONEncoder

from flask_mail import Mail

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.sqlalchemy import declarative_base, _QueryProperty, Model, _BoundDeclarativeMeta, BaseQuery

encoder = JSONEncoder()

mail = Mail()

db = SQLAlchemy(session_options={'expire_on_commit': False})


def make_declarative_base(self):
    """Creates the declarative base."""
    base = declarative_base(cls=Model, name='Model',
                            metaclass=_BoundDeclarativeMeta)
    base.query = _QueryProperty(self)
    return base


BaseModel = make_declarative_base(db)

