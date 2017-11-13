import os
import uuid

# Add the current directory to the python path
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECURITY_POST_LOGIN_VIEW = '/account'
SECURITY_PASSWORD_HASH = 'sha512_crypt'
SECURITY_PASSWORD_SALT = 'uh3dkXvKAJ9UJJ'
SECURITY_REMEMBER_SALT = 'KBR7A3RdzvYqWK'
SECURITY_RESET_SALT = 'wda7XnDcGj8mFs'
PASSWORD_RESET_EMAIL = SECURITY_RESET_SALT
SECURITY_RESET_WITHIN = '5 days'
SECURITY_CONFIRM_WITHIN = '5 days'
SECURITY_SEND_REGISTER_EMAIL = False
SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False
SECURITY_RECOVERABLE = True
SECURITY_RESET_PASSWORD = True
SECURITY_REGISTERABLE = True
SECURITY_TRACKABLE = True
SECRET_KEY = 'XwePyQ66EDyDPD'

# EMAIL
MAIL_DEFAULT_SENDER = 'foo@foo.com'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 25
MAIL_USE_TLS = True
MAIL_USERNAME = 'foo@foo.com'
MAIL_PASSWORD = 'foo'


SYSTEM_UUID = uuid.UUID('15e70b5a-aed2-4582-82e5-be726b8457c5')
SYSTEM_EMAIL = 'foo@foo.com'
SYSTEM_NAME = 'd1.hwdevel.com'
MAIL_CATCH_ALL = True
SEND_MAIL_ENABLED = True
FORCED_MAIL = (u'd1.hwdevel.com', 'dsupport@foo.com')
ADMINS = ['fabian.falon@foo.com']

MYSQL_HOST = u'localhost'
MYSQL_USER = u'root'
MYSQL_PASSWORD = u'root'
MYSQL_DB = u'test_db'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:3306/{}?charset=utf8&use_unicode=0'.format(MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB)

# TEMPLATES
DOMAIN_NAME = '127.0.0.1:5001'
URI_SERVICE = 'http'


DEBUG = False

print "DEBUG mode: {}".format(repr(DEBUG))


# Restrict the extensions allowed for the uploaded files, we do other checks
# on the views, but this is the first level
ALLOWED_EXTENSIONS = [
    'cer', 'crt', 'pfx', 'key', 'pem', 'arm', 'crt'
]


DEFAULT_API = 'v1'

# Site domain, you usually want this to be your frontend url. This is used for
# login verification between other things
SITE_DOMAIN = 'localhost'
LOGIN_URL = 'localhost'

# How long the user session will last (in hours). Default: 168 (7 days)
SESSION_EXPIRES = 168

# Service tokens, this are usually the "client secret" or private API keys
# that you need to finish the OAuth validation. Remember NOT to commit back
# this values! They should remain known to you only!
GITHUB_SECRET = ''
FACEBOOK_SECRET = ''
LINKEDIN_SECRET = ''
GOOGLEPLUS_SECRET = ''
TWITTER_KEY = ''
TWITTER_SECRET = ''  # Twitter consumer secret
TWITTER_CALLBACK_URI = ''

# Main server token Make it unique and keep it away from strangers! This token
# is used in authentication and part of the storage encryption. This token
# is an example. **You MUST replace it!**
# SECRET = '-&3whmt0f&h#zvyc@yk4bs3g6biu9l&a%0l=5u*q2+rz(sypdk'
SECRET = 'XwePyQ66EDyDPD'


# Logging settings. This is a standard python logging configuration. The levels
# are supposed to change depending on the settings file, to avoid clogging the
# logs with useless information.
LOGFILE = 'mtapi-falcon.log'
LOG_CONFIG = {
    "version": 1,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(filename)s->%(funcName)s:%(lineno)s] %(message)s",
            'datefmt': "%Y/%m/%d %H:%M:%S"
        },
    },
    'handlers': {
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, LOGFILE),
            'maxBytes': 2097152,  # 2MB per file
            'backupCount': 2,  # Store up to three files
            'formatter': 'standard',
        },
    },
    'loggers': {
        'sikr': {
            'handlers': ["logfile", ],
            'level': 'DEBUG',
        },
    }
}

ENDPOINT = '/api/v1'
