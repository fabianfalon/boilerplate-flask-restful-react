

import json
import datetime

from api import db
from api.models import User
from api.tests.base import BaseTestCase
from api.tests.utils import add_user
import requests

class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_users(self):
        """Ensure the /ping route behaves correctly."""
        response = requests.get('http://localhost:5000/api/v1/users/ping')
        self.assertEqual(response.json(), {'hello': 'world'})
        data = json.loads(response.json())
        self.assertEqual(data.status_code, 200)
        self.assertIn(data.message)
        self.assertEqual(data.message, 'pong')

