# from api.db.connector import BaseModel
from api.core import db, BaseModel
from api.models import *
from api.utils.logs import logger
from flask import current_app
import unicodedata
from flask.ext.script import Command, prompt, prompt_pass


def generate_db_schema():
    # Try to create the database tables, don't do anything if they fail
    try:
        print "Dropeando schema"
        BaseModel.metadata.drop_all(bind=db.engine)
        print "Creando schema"
        BaseModel.metadata.create_all(bind=db.engine)
    except Exception as e:
        logger.error(e)
        print(e)

def drop_all():
    BaseModel.metadata.drop_all(bind=db.engine)

def generate_data():
    print "creando roles...."
    role = Role(id=1, name='ADMIN',
                description='ADMINISTRADOR')
    role.save()
    print "creando usuarios...."
    user = User(
        email='fabian.falon@gmail.com',
        id=1, first_name=u'fabian', last_name="falon",
        active=True, role_id=1)
    user.password = get_hmac('fabian')
    user.save()
    user = User(
        email='user1.user1@user.com',
        id=2, first_name=u'user', last_name="s",
        active=True, role_id=1)
    user.password = get_hmac('user')
    user.save()


def elimina_tildes(s):
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))


def get_hmac(passwd):
    h = hmac.new(
        current_app.config['SECURITY_PASSWORD_SALT'].encode('utf-8'),
        passwd.encode('utf-8'), hashlib.sha512
    )
    return base64.b64encode(h.digest())


class CreateUserCommand(Command):
    """Create a user"""

    def run(self):
        email = prompt('Email')
        password = prompt_pass('Password')
        first_name = prompt('First name')
        last_name = prompt('Last name')
        role_id = prompt('Role: (1) Administrator, (2) Invited]:')

        user = User(
            email=email,
            first_name=first_name, last_name=last_name,
            active=True, role_id=role_id)
        user.password = get_hmac(password)
        user.save()
        print 'user {} created'.format(user.email)
        return user.id
