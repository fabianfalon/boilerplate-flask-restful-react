# -*- coding: utf-8 -*-

from .users import *
from .audit import *
from .books import *


class DB(object):
    pass


container = DB()
container.User = User
container.Role = Role
container.Book = Book
container.Audit = Audit


container.User.db = container
container.Role.db = container
container.Book.db = container
container.Audit.db = container
