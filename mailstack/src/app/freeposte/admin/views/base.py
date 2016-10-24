from freeposte import dockercli
from freeposte.admin import app, db, models, forms, access

import flask
import flask_login


@app.route('/', methods=["GET"])
@access.authenticated
def index():
    return flask.redirect(flask.url_for('.user_settings'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = models.User.login(form.email.data, form.pw.data)
        if user:
            flask_login.login_user(user)
            return flask.redirect(flask.url_for('.index'))
        else:
            flask.flash('Wrong e-mail or password', 'error')
    return flask.render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
@access.authenticated
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('.index'))


@app.route('/services', methods=['GET'])
@access.global_admin
def services():
    containers = {}
    for brief in dockercli.containers(all=True):
        if brief['Image'].startswith('freeposte/'):
            container = dockercli.inspect_container(brief['Id'])
            container['Image'] = dockercli.inspect_image(container['Image'])
            name = container['Config']['Labels']['com.docker.compose.service']
            containers[name] = container
    return flask.render_template('services.html', containers=containers)
