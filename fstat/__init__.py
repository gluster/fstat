from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_github import GitHub
try:
    import sentry_sdk
    from sentry_sdk.integrations.flask import FlaskIntegration
    sentry_sdk.init(integrations=[FlaskIntegration()])
except ImportError:
    pass


app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('default.cfg')
app.config.from_pyfile('application.cfg', silent=True)
Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
github = GitHub(app)


from .controller import index  # noqa: E402,F401
from .model import Failure, FailureInstance  # noqa: E402,F401
