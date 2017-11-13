import os

confpath = os.path.abspath(os.path.dirname(__file__)+'/..')

LOCAL_INSTANCE = os.path.isfile(
    os.path.join(
        confpath,
        'local_instance_on'
    )
)

DEBUG = os.path.isfile(
    os.path.join(
        confpath,
        'debug_on'
    )
)


if DEBUG == False:
    from development import *
else:
    from production import *
