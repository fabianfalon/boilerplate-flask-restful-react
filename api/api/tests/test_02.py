import unittest
import json
from flask import url_for
from api import create_app
from api.core import db

class TestCase02(unittest.TestCase):
    '''Test case 02'''
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def test_404(self):
        response = self.client.get(
            '/api/v1/users')
        self.assertTrue(response.status_code == 401)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['message'] == 'Missing authorization header')

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
