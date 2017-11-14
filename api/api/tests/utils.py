import datetime

from flask import current_app
from api import db
from api.models import User

import hashlib
import base64
from api.db.syncdb import get_hmac

def add_user(email, first_name, last_name, password, role_id, created_at=datetime.datetime.utcnow()):
    user = User(
        email=email,
        first_name=first_name, last_name=last_name,
        active=True, role_id=role_id,
        created_at=created_at)
    user.password = get_hmac(password)
    user.save()
    return user
