from flask import render_template, request, redirect, url_for, session, flash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db, License
from config import config
from datetime import datetime
from functools import wraps
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required

# Dummy credentials for demonstration
USERNAME = 'admin'
PASSWORD = 'internet'

# User model for authentication
class User(UserMixin):
    def __init__(self, id):
        self.id = id

def create_admin_app(app):
    admin = Admin(app, name='License Admin', template_mode='bootstrap4')
    admin.add_view(ModelView(License, db.session))

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        error = None
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if username == USERNAME and password == PASSWORD:
                user = User(id=1)
                login_user(user)
                return redirect(url_for('license_list'))
            else:
                error = 'Invalid Credentials. Please try again.'
        return render_template('login.html', error=error)

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/admin/license')
    @login_required
    def license_list():
        search_ip = request.args.get('search_ip')
        if search_ip:
            licenses = License.query.filter(License.ip_address.contains(search_ip)).all()
        else:
            licenses = License.query.all()
        return render_template('license_list.html', licenses=licenses, search_ip=search_ip)

    @app.route('/admin/license/new', methods=['GET', 'POST'], endpoint='new_license')
    @login_required
    def new_license():
        license = License()
        form_title = "Tambah Lisensi"
        form_action = url_for('new_license')

        if request.method == 'POST':
            license.ip_address = request.form['ip_address']
            license.license_key = request.form['license_key']
            active_until_str = request.form['active_until']
            license.active_until = datetime.strptime(active_until_str, '%Y-%m-%dT%H:%M')

            db.session.add(license)
            db.session.commit()
            
            return redirect(url_for('license_list'))

        return render_template('license_form.html', form_title=form_title, form_action=form_action, license=license)

    @app.route('/admin/license/<int:id>/edit', methods=['GET', 'POST'], endpoint='edit_license')
    @login_required
    def edit_license(id):
        license = License.query.get(id)
        form_title = "Edit Lisensi"
        form_action = url_for('edit_license', id=id)

        if request.method == 'POST':
            license.ip_address = request.form['ip_address']
            license.license_key = request.form['license_key']
            active_until_str = request.form['active_until']
            license.active_until = datetime.strptime(active_until_str, '%Y-%m-%dT%H:%M')

            db.session.commit()
            
            return redirect(url_for('license_list'))

        return render_template('license_form.html', form_title=form_title, form_action=form_action, license=license)

    @app.route('/admin/license/<int:id>/delete', endpoint='delete_license')
    @login_required
    def license_delete(id):
        license = License.query.get(id)
        db.session.delete(license)
        db.session.commit()
        return redirect(url_for('license_list'))
