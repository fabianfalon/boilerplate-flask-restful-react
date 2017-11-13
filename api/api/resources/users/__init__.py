# -*- coding: utf-8 -*-

from .users import *
from .registration import *

resources = [
    ('users', UserCollection, "users.list_users"),
    ('users/me', MeResource, "users.me"),
    ('users/<int:user_id>', UserResource, "users.show_user"),
    ('users/roles', RoleCollection, "users.roles"),
    ('users/ping', UserPingCollection, "users.ping"),

]
