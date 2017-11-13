# -*- coding: utf-8 -*-
import simplejson as json

from flask.ext.sqlalchemy import declarative_base, _QueryProperty, Model, _BoundDeclarativeMeta, BaseQuery

from api import settings
from api.utils.logs import logger
