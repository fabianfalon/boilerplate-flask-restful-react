# -*- coding: utf-8 -*-
"""
    manage
    ~~~~~~
    Manager module
"""
import logging
import sys
import unittest
import coverage
from flask.ext.script import Manager
from api.db.syncdb import CreateUserCommand
from api import create_app
from flask_migrate import Migrate, MigrateCommand
from api.core import BaseModel

COV = coverage.coverage(
    branch=True,
    include='api/*',
    omit=[
        'api/tests/*',
    ]
)
COV.start()

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


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('api/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('api/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1

if __name__ == "__main__":
    manager.run()
