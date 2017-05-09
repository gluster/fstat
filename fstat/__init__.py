from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from controller import index
from model import Failure, FailureInstance

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('default.cfg')
app.config.from_pyfile('application.cfg', silent=True)
Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
