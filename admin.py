from flask import render_template, request, redirect, url_for, session, flash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db, License
from config import config
from datetime import datetime
from functools import wraps

# Dummy credentials for demonstration
USERNAME = 'admin'
PASSWORD = 'password'

def create_admin_app(app):
    admin = Admin(app, name='License Admin', template_mode='bootstrap4')
    admin.add_view(ModelView(License, db.session))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        error = None
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if username == USERNAME and password == PASSWORD:
                session['logged_in'] = True
                return redirect(url_for('license_list'))
            else:
                error = 'Invalid Credentials. Please try again.'
        return render_template('login.html', error=error)

    @app.route('/logout')
    def logout():
        session.pop('logged_in', None)
        return redirect(url_for('login'))

    def login_required(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if not session.get('logged_in'):
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return wrap

    @app.route('/admin/license')
    @login_required
    def license_list():
        search_ip = request.args.get('search_ip')
        if search_ip:
            licenses = License.query.filter(License.ip_address.contains(search_ip)).all()
        else:
            licenses = License.query.all()
        return render_template('license_list.html', licenses=licenses)

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