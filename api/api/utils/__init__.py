from .logs import *
from dateutil.relativedelta import relativedelta
import datetime
import decimal
from api.models import *
from pprint import pprint as pp


def printquery(statement, bind=None):
    """
    print a query, with values filled in
    for debugging purposes *only*
    for security, you should always separate queries from their values
    please also note that this function is quite slow
    """
    import sqlalchemy.orm
    if isinstance(statement, sqlalchemy.orm.Query):
        if bind is None:
            bind = statement.session.get_bind(
                statement._mapper_zero_or_none()
            )
        statement = statement.statement
    elif bind is None:
        bind = statement.bind

    dialect = bind.dialect
    compiler = statement._compiler(dialect)

    class LiteralCompiler(compiler.__class__):
        def visit_bindparam(
                self, bindparam, within_columns_clause=False,
                literal_binds=False, **kwargs
        ):
            return super(LiteralCompiler, self).render_literal_bindparam(
                bindparam, within_columns_clause=within_columns_clause,
                literal_binds=literal_binds, **kwargs
            )

        def render_literal_value(self, value, type_):
            """Render the value of a bind parameter as a quoted literal.
            This is used for statement sections that do not accept bind
            paramters on the target driver/database.
            This should be implemented by subclasses using the quoting services
            of the DBAPI.
            """
            if isinstance(value, basestring):
                value = value.replace("'", "''")
                return "'%s'" % value
            elif value is None:
                return "NULL"
            elif isinstance(value, (float, int, long)):
                return repr(value)
            elif isinstance(value, decimal.Decimal):
                return str(value)
            elif isinstance(value, datetime.datetime):
                return "'{}'".format(value.strftime("%Y-%m-%d %H:%M:%S"))
            elif isinstance(value, datetime.date):
                return "'{}'".format(value.strftime("%Y-%m-%d"))
            else:
                raise NotImplementedError(
                    "Don't know how to literal-quote value %r" % value)

    compiler = LiteralCompiler(dialect, statement)
    pp(compiler.process(statement))


def user_info(token):
    token = token.split()
    user = User.query.filter_by(registration_token=token[1]).first()
    return user.id

# verifica si es admin filtrando por el token
def is_admin(token):
    token = token.split()
    user = User.query.filter_by(registration_token=token[1]).first()
    return (user.role_id == 1)


def is_user_admin(id):
    user = User.query.get(id)
    return (user.role_id == 1)
