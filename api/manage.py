# -*- coding: utf-8 -*-
"""
    manage
    ~~~~~~
    Manager module
"""
import logging
import sys

from flask.ext.script import Manager
from api.db.syncdb import CreateUserCommand
from api import create_app
from flask_migrate import Migrate, MigrateCommand
from api.core import BaseModel

root = logging.getLogger()
root.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

app = create_app()
manager = Manager(app)
manager.add_command('create_user', CreateUserCommand())


migrate = Migrate(app, BaseModel)

manager.add_command('db', MigrateCommand)

root = logging.getLogger()
root.setLevel(logging.INFO)

if __name__ == "__main__":
    manager.run()