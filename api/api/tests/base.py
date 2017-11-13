# project/tests/base.py


import unittest

from api import create_app
from api.db import syncdb

app = create_app()


class BaseTestCase(unittest.TestCase):
    def create_app(self):
        self.app = create_app()
        self.client = self.app.test_client()
        return self

    def setUp(self):
        syncdb.generate_db_schema()
        syncdb.generate_data()

    def tearDown(self):
        pass
