from flask import jsonify
from marshmallow import fields, Schema
from main import app


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


class UserEmailAlreadyExistedError(Error):
    status_code = StatusCode.BAD_REQUEST
    error_code = ErrorCode.USER_ALREADY_EXISTS
    error_message = 'This email is already registered. Click here to login.'


class UserDoesNotExist(Error):
    status_code = StatusCode.BAD_REQUEST
    error_code = ErrorCode.USER_DOES_NOT_EXIST
    error_message = 'User does not exist'


class UnconfirmedEmail(Error):
    status_code = StatusCode.BAD_REQUEST
    error_code = ErrorCode.UNCONFIRMED_EMAIL
    error_message = 'This email has not been confirmed. Please use confirmation code to confirm this email.'


class EmailAndPasswordNotMatch(Error):
    status_code = StatusCode.BAD_REQUEST
    error_code = ErrorCode.BAD_REQUEST
    error_message = "Invalid email or password."


class Unauthorized(Error):
    status_code = StatusCode.UNAUTHORIZED
    error_code = ErrorCode.UNAUTHORIZED
    error_message = 'Unauthorized'


class NotFound(Error):
    status_code = StatusCode.NOT_FOUND
    error_code = ErrorCode.NOT_FOUND
    error_message = 'Not found'

    def __init__(self, code=ErrorCode.NOT_FOUND, message='Not found', data=None):
        super(self.__class__, self).__init__(data)
        self.error_code = code
        self.error_message = message


class BadRequest(Error):
    status_code = StatusCode.BAD_REQUEST
    error_code = ErrorCode.BAD_REQUEST
    error_message = "Bad request"

    def __init__(self, error_data=None, code=ErrorCode.BAD_REQUEST, message='Bad Request'):
        super(self.__class__, self).__init__(error_data)
        self.error_code = code
        self.error_message = message


class MethodNotAllowed(Error):
    status_code = StatusCode.METHOD_NOT_ALLOWED
    error_code = ErrorCode.METHOD_NOT_ALLOWED
    error_message = 'Method not allowed'


@app.errorhandler(404)
def page_not_found(error):
    return NotFound().to_response()


@app.errorhandler(405)
def method_not_allowed(error):
    return MethodNotAllowed().to_response()


@app.errorhandler(Exception)
def error_handler(error):
    if isinstance(error, Error):
        return error.to_response()

    return jsonify(error_message=str(error)), 500
