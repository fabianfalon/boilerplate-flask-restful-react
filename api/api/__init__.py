# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.cors import CORS
from api.resources import users, auth, books
from api.helpers import JSONEncoder
import flask.ext.restful.representations.json
flask.ext.restful.representations.json.settings["cls"] = JSONEncoder

from celery import Celery
from celery.signals import worker_process_init


def create_app():
    from api.core import *
    app = Flask(__name__)
    app.config.from_object('api.settings')
    cors = CORS(app, resources={r"/*": {"origins": "*", "allow_headers": "Origin, X-Requested-With, Content-Type, Accept", 'allow_credentials': True, 'allow_methods': 'GET, POST, DELETE, PUT, OPTIONS'}})
    app.json_encoder = JSONEncoder
    db.init_app(app)

    from flask.ext import restful
    api = restful.Api(app)

    mail.init_app(app)

    for url, res, endpoint in users.resources:
        api.add_resource(res, '{}/{}'.format(
            app.config['ENDPOINT'], url, endpoint=endpoint))
    for url, res, endpoint in auth.resources:
        api.add_resource(res, '{}/{}'.format(
            app.config['ENDPOINT'], url, endpoint=endpoint))
    for url, res, endpoint in books.resources:
        api.add_resource(res, '{}/{}'.format(
            app.config['ENDPOINT'], url, endpoint=endpoint))
    return app


def on_worker_process_init(*args, **kwargs):
    pass


def create_celery_app(app=None):
    app = app or create_app()

    celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    app.extensions['celery'] = celery
    return celery

worker_process_init.connect(on_worker_process_init)

