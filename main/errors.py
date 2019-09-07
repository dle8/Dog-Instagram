from flask import jsonify
from marshmallow import fields, Schema


class Error(Exception):
    def __init__(self, error_data=None):
        super(Error)
        self.error_data = error_data or {}

    def to_response(self):
        resp = jsonify(ErrorSchema().dump(self))
        resp.status_code = self.status_code
        return resp


class ErrorSchema(Schema):
    error_code = fields.Int()
    error_message = fields.String()
    error_data = fields.Raw()


class StatusCode:
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405


class ErrorCode:
    BAD_REQUEST = 40000
    VALIDATION_ERROR = 40001
    USER_ALREADY_EXISTS = 40002
    USER_DOES_NOT_EXIST = 40003
    UNAUTHORIZED = 40100
    NOT_FOUND = 40400
    METHOD_NOT_ALLOWED = 40005

    INVALID_EMAIL = 40097
    UNCONFIRMED_EMAIL = 40098


class InvalidEmail(Error):
    status_code = StatusCode.BAD_REQUEST
    error_code = ErrorCode.INVALID_EMAIL
    error_message = 'This email is invalid. Please try another one.'
