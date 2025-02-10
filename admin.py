from flask import render_template, request, redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db, License
from config import config
from datetime import datetime

def create_admin_app(app):
    admin = Admin(app, name='License Admin', template_mode='bootstrap4')
    admin.add_view(ModelView(License, db.session))

    @app.route('/admin/license')
    def license_list():
        licenses = License.query.all()
        return render_template('license_list.html', licenses=licenses)

    @app.route('/admin/license/new', methods=['GET', 'POST'])
    @app.route('/admin/license/<int:id>/edit', methods=['GET', 'POST'])
    def license_form(id=None):
        if id:
            license = License.query.get(id)
            form_title = "Edit Lisensi"
            form_action = url_for('license_form', id=id)
        else:
            license = License()
            form_title = "Tambah Lisensi"
            form_action = url_for('license_form')

        if request.method == 'POST':
            license.ip_address = request.form['ip_address']
            license.license_key = request.form['license_key']
            active_until_str = request.form['active_until']
            license.active_until = datetime.strptime(active_until_str, '%Y-%m-%dT%H:%M')

            if id:
                db.session.commit()
            else:
                db.session.add(license)
                db.session.commit()
            
            return redirect(url_for('license_list'))

        return render_template('license_form.html', form_title=form_title, form_action=form_action, license=license)

    @app.route('/admin/license/<int:id>/delete')
    def license_delete(id):
        license = License.query.get(id)
        db.session.delete(license)
        db.session.commit()
        return redirect(url_for('license_list'))