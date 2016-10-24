import flask
import flask_sqlalchemy
import flask_bootstrap
import flask_login
import flask_script
import flask_migrate
import flask_babel

import os
import docker


# Create application
app = flask.Flask(__name__, static_url_path='/admin/app_static')

default_config = {
    'SQLALCHEMY_DATABASE_URI': 'sqlite:////database/mailstack.db',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SECRET_KEY': 'changeMe',
    'DOCKER_SOCKET': 'unix:///var/run/docker.sock',
    'HOSTNAME': 'mail.freeposte.io',
    'DOMAIN': 'freeposte.io',
    'POSTMASTER': 'postmaster',
    'DEBUG': False,
    'BOOTSTRAP_SERVE_LOCAL': True,
    'DKIM_PATH': '/dkim/{domain}.{selector}.key',
    'DKIM_SELECTOR': 'dkim',
    'BABEL_DEFAULT_LOCALE': 'en',
    'BABEL_DEFAULT_TIMEZONE': 'UTC'
}

# Load configuration from the environment if available
for key, value in default_config.items():
    app.config[key] = os.environ.get(key, value)

# Setup components
flask_bootstrap.Bootstrap(app)
db = flask_sqlalchemy.SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
babel = flask_babel.Babel(app)

# Manager commnad
manager = flask_script.Manager(app)
manager.add_command('db', flask_migrate.MigrateCommand)

# Connect to the Docker socket
dockercli = docker.Client(base_url=app.config['DOCKER_SOCKET'])

# Finally setup the blueprint and redirect /
from freeposte import admin
app.register_blueprint(admin.app, url_prefix='/admin')

@app.route("/")
def index():
    return flask.redirect(flask.url_for("admin.index"))
