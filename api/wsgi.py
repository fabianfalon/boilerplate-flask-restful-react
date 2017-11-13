# -*- coding: utf-8 -*-
from wsgiref import simple_server

from api import create_app

from werkzeug.contrib.fixers import ProxyFix

app = create_app()

app.wsgi_app = ProxyFix(app.wsgi_app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add(
        'Access-Control-Allow-Headers',
        'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


if __name__ == "__main__":
    app.run('0.0.0.0', 5000, debug=True)
