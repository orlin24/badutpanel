from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from models import db, License
from config import config

def create_api_app(app):
    limiter = Limiter(key_func=get_remote_address, storage_uri=app.config['RATELIMIT_STORAGE_URI'])
    limiter.init_app(app)

    @app.route('/validate_license', methods=['POST'])
    @limiter.limit("5 per minute")
    def validate_license():
        data = request.json
        license_key = data.get('license_key')
        ip_address = request.remote_addr

        license = License.query.filter_by(license_key=license_key, ip_address=ip_address).first()

        if license and license.is_valid():
            return jsonify({"valid": True, "expiry_date": license.active_until.isoformat()}), 200
        else:
            return jsonify({"valid": False}), 403
