import unittest
import json
from base64 import b64encode
from api import create_app
from api.models import User
from api.db import syncdb
from api.core import db
from api.tests.utils import add_user


class TestUsers(unittest.TestCase):
    '''Test users endpoint'''

    def setUp(self):
        syncdb.generate_db_schema()
        syncdb.generate_data()
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        syncdb.drop_all()
        self.app_context.pop()

    def test_ping(self):
        response = self.client.get(
            '/api/v1/users/ping')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['status_code'], 200)
        self.assertEqual(data['message'], 'pong')

    def test_user_me(self):
        resp_login = self.client.post(
            '/api/v1/auth',
            data=json.dumps(dict(
                email='fabian.falon@gmail.com',
                password='fabian'
            )),
            content_type='application/json'
        )

        response = self.client.get(
            '/api/v1/users/me',
            content_type='application/json',
            headers=dict(
                Authorization='Bearer ' + json.loads(
                    resp_login.data.decode()
                )['token']
            )
        )

        data = json.loads(response.data)
        self.assertEqual(data['first_name'], 'fabian')
        self.assertEqual(data['id'], 1)


    def test_add_new_user(self):
        add_user('test@test.com', 'test', 'test', 'test', 1)
        user = User.query.filter_by(email='test@test.com').first()
        db.session.commit()
        with self.client:
            # user login
            resp_login = self.client.post(
                '/api/v1/auth',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )

            response = self.client.post(
                '/api/v1/users',
                data=json.dumps(dict(
                    username='fabian1',
                    email='fabian1.falon1@gmail.com',
                    password='fabian1'
                )),
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(data['status_code'], 201)
            self.assertIn('The user was created successfully', data['message'])

    def test_update_user(self):
        resp_login = self.client.post(
            '/api/v1/auth',
            data=json.dumps(dict(
                email='fabian.falon@gmail.com',
                password='fabian'
            )),
            content_type='application/json'
        )

        response = self.client.put(
            '/api/v1/users/2',
            data=json.dumps(dict(
                first_name='user'
            )),
            content_type='application/json',
            headers=dict(
                Authorization='Bearer ' + json.loads(
                    resp_login.data.decode()
                )['token']
            )
        )
        data = json.loads(response.data.decode())
        self.assertEqual(data['status_code'], 200)
        self.assertIn('User has been successfully modified', data['message'])
