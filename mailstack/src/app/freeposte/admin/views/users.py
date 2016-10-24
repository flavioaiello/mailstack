from freeposte.admin import app, db, models, forms, access

import flask
import flask_login
import wtforms_components


@app.route('/user/list/<domain_name>', methods=['GET'])
@access.domain_admin(models.Domain, 'domain_name')
def user_list(domain_name):
    domain = models.Domain.query.get(domain_name) or flask.abort(404)
    return flask.render_template('user/list.html', domain=domain)


@app.route('/user/create/<domain_name>', methods=['GET', 'POST'])
@access.domain_admin(models.Domain, 'domain_name')
def user_create(domain_name):
    domain = models.Domain.query.get(domain_name) or flask.abort(404)
    if domain.max_users and len(domain.users) >= domain.max_users:
        flask.flash('Too many users for domain %s' % domain, 'error')
        return flask.redirect(
            flask.url_for('.user_list', domain_name=domain.name))
    form = forms.UserForm()
    if form.validate_on_submit():
        if domain.has_email(form.localpart.data):
            flask.flash('Email is already used', 'error')
        else:
            user = models.User(domain=domain)
            form.populate_obj(user)
            user.set_password(form.pw.data)
            db.session.add(user)
            db.session.commit()
            flask.flash('User %s created' % user)
            return flask.redirect(
                flask.url_for('.user_list', domain_name=domain.name))
    return flask.render_template('user/create.html',
        domain=domain, form=form)


@app.route('/user/edit/<user_email>', methods=['GET', 'POST'])
@access.domain_admin(models.User, 'user_email')
def user_edit(user_email):
    user = models.User.query.get(user_email) or flask.abort(404)
    form = forms.UserForm(obj=user)
    wtforms_components.read_only(form.localpart)
    form.pw.validators = []
    if form.validate_on_submit():
        form.populate_obj(user)
        if form.pw.data:
            user.set_password(form.pw.data)
        db.session.commit()
        flask.flash('User %s updated' % user)
        return flask.redirect(
            flask.url_for('.user_list', domain_name=user.domain.name))
    return flask.render_template('user/edit.html', form=form, user=user, domain=user.domain)


@app.route('/user/delete/<user_email>', methods=['GET', 'POST'])
@access.domain_admin(models.User, 'user_email')
@access.confirmation_required("delete {user_email}")
def user_delete(user_email):
    user = models.User.query.get(user_email) or flask.abort(404)
    db.session.delete(user)
    db.session.commit()
    flask.flash('User %s deleted' % user)
    return flask.redirect(
        flask.url_for('.user_list', domain_name=user.domain.name))


@app.route('/user/settings', methods=['GET', 'POST'], defaults={'user_email': None})
@app.route('/user/usersettings/<user_email>', methods=['GET', 'POST'])
@access.owner(models.User, 'user_email')
def user_settings(user_email):
    user_email_or_current = user_email or flask_login.current_user.email
    user = models.User.query.get(user_email_or_current) or flask.abort(404)
    form = forms.UserSettingsForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flask.flash('Settings updated for %s' % user)
        if user_email:
            return flask.redirect(
                flask.url_for('.user_list', domain_name=user.domain.name))
    return flask.render_template('user/settings.html', form=form, user=user)


@app.route('/user/password', methods=['GET', 'POST'], defaults={'user_email': None})
@app.route('/user/password/<user_email>', methods=['GET', 'POST'])
@access.owner(models.User, 'user_email')
def user_password(user_email):
    user_email_or_current = user_email or flask_login.current_user.email
    user = models.User.query.get(user_email_or_current) or flask.abort(404)
    form = forms.UserPasswordForm()
    if form.validate_on_submit():
        if form.pw.data != form.pw2.data:
            flask.flash('Passwords do not match', 'error')
        else:
            user.set_password(form.pw.data)
            db.session.commit()
            flask.flash('Password updated for %s' % user)
            if user_email:
                return flask.redirect(flask.url_for('.user_list',
                    domain_name=user.domain.name))
    return flask.render_template('user/password.html', form=form, user=user)


@app.route('/user/forward', methods=['GET', 'POST'], defaults={'user_email': None})
@app.route('/user/forward/<user_email>', methods=['GET', 'POST'])
@access.owner(models.User, 'user_email')
def user_forward(user_email):
    user_email_or_current = user_email or flask_login.current_user.email
    user = models.User.query.get(user_email_or_current) or flask.abort(404)
    form = forms.UserForwardForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flask.flash('Forward destination updated for %s' % user)
        if user_email:
            return flask.redirect(
                flask.url_for('.user_list', domain_name=user.domain.name))
    return flask.render_template('user/forward.html', form=form, user=user)


@app.route('/user/reply', methods=['GET', 'POST'], defaults={'user_email': None})
@app.route('/user/reply/<user_email>', methods=['GET', 'POST'])
@access.owner(models.User, 'user_email')
def user_reply(user_email):
    user_email_or_current = user_email or flask_login.current_user.email
    user = models.User.query.get(user_email_or_current) or flask.abort(404)
    form = forms.UserReplyForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flask.flash('Auto-reply message updated for %s' % user)
        if user_email:
            return flask.redirect(
                flask.url_for('.user_list', domain_name=user.domain.name))
    return flask.render_template('user/reply.html', form=form, user=user)
