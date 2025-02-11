from flask import Flask, redirect, url_for
from models import db
from config import config
from admin import create_admin_app
from api import create_api_app

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.secret_key = config.SECRET_KEY

    db.init_app(app)
    with app.app_context():
        db.create_all()

    create_admin_app(app)
    create_api_app(app)

    @app.route('/')
    def home():
        return redirect(url_for('license_list'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)