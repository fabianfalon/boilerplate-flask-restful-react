# -*- coding: utf-8 -*-

from .auth import *
from .status import *

resources = [
    ('auth', AuthResource, "auth.auth"),
    ('status', StatusResource, "auth.status"),
    # ('users/token', TokenResource, "users.get_token"),
]
