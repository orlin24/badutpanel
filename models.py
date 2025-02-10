from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()

class License(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45), unique=True, nullable=False)
    license_key = db.Column(db.String(50), unique=True, nullable=False)
    active_until = db.Column(db.DateTime, nullable=False)

    def is_valid(self):
        return self.active_until > datetime.utcnow()