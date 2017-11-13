# Flask Restful boilerplate

## Development Environment

At the bare minimum you'll need the following for your development environment:

1. [Python](http://www.python.org/)
2. [MySQL](http://www.mysql.com/)

It is strongly recommended to also install and use the following tools:

1. [virtualenv](https://python-guide.readthedocs.org/en/latest/dev/virtualenvs/#virtualenv)
2. [virtualenvwrapper](https://python-guide.readthedocs.org/en/latest/dev/virtualenvs/#virtualenvwrapper)

### Local Setup

The following assumes you have all of the recommended tools listed above installed.

#### 1. Clone the project:

    $ git clone 
    $ cd demo-project

#### 2. Create and initialize virtualenv for the project:

    $ virtualenv env
    $ source env/bin/activate
    $ pip install -r requirements.txt

#### 3. Generate schema and data:
	$ python manage.py shell
	$ from api.db.syncdb import *
	$ generate_db_schema()
	$ generate_data()

#### 7. Run the development server:

    $ python wsgi.py




#### 9. In another console run the Celery app:

    $ celery -A api.backend.celery worker -l debug

#### 10. Open [http://localhost:3000/login](http://localhost:3000/login)


### Development

If all went well in the setup above you will be ready to start hacking away on
the application.


#### Management Commands

Management commands can be listed with the following command:

    $ python manage.py
    $ python manage.py create_user


#### Migrations

Migrations commands:
 
    $ python manage.py db init     (creates the migrations folder with all the necessary settings)
    $ python manage.py db migrate  (detects if there were changes in the models)
    $ python manage.py db upgrade  (run the migration)
