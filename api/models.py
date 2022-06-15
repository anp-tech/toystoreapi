from . import db
from datetime import datetime, timedelta
from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.security import check_password_hash
import base64
import os


# represent 'employee' table in the database
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean, nullable=False)
    token = db.Column(db.String(32), unique=True)
    token_expiration = db.Column(db.DateTime)

    # generate token to the sign-in users
    def generate_token(self, expiration_time=90):
        # if current token > one minute before the expiration
        if self.token and self.token_expiration > datetime.utcnow() + timedelta(seconds=60):
            # return current token
            return self.token
        # otherwise, generate a random token 20 characters long in base64
        self.token = base64.b64encode(os.urandom(15)).decode('utf-8')
        # set expiration time
        self.token_expiration = datetime.utcnow() + timedelta(minutes=expiration_time)
        db.session.add(self)
        return self.token

    def password_hash(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def verify_valid_token(token):
        employee = Employee.query.filter_by(token=token).first()
        # if no employee or the token is expired
        if employee is None or employee.token_expiration < datetime.utcnow():
            return None
        return employee


# represent 'items' table in the database
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    token_expiration = db.Column(db.DateTime)


def error_handling(status, error_message=None):
    payload = {'error message': HTTP_STATUS_CODES.get(status, 'unknown error')}
    if error_message:
        payload['reason'] = error_message
    res = jsonify(payload)
    res.status_code = status
    return res


def admin_only():
    return jsonify({'message': 'Only Admin users can perform this function!'})


