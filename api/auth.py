from flask_httpauth import HTTPTokenAuth, HTTPBasicAuth
from .models import Employee, error_handling


"""
    two functions for basic authentication to verify the username and password and handle error with response 
    two functions for token authentication to return the current user with valid token and handle error with response
"""

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme='Bearer')


@basic_auth.verify_password
def verify_password(username, password):
    employee = Employee.query.filter_by(username=username).first()
    if employee and employee.password_hash(password):
        return employee


@basic_auth.error_handler
def basic_auth_error_handler(status):
    return error_handling(status)


@token_auth.verify_token
def verify_token(token):
    # return the current user if token is valid, otherwise, return None
    return Employee.verify_valid_token(token) if token else None


@token_auth.error_handler
def token_auth_error_handler(status):
    return error_handling(status)
