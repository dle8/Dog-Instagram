from functools import wraps
from flask import request
from main import errors
from main.config import config
from main.libs.firebase.user import check_user_credentials
import datetime
import jwt


def parse_args_with(schema):
    def parse_args_with_decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            request_args = request.get_json() or {}
            if request.method == 'GET':
                request_args = request.args.to_dict()
            if 'file' in request.files:
                request_args['file'] = request.files['file']
            parsed_args = schema.load(request_args)
            kwargs['args'] = parsed_args
            return f(*args, **kwargs)

        return decorated_function

    return parse_args_with_decorator


def jwt_required():
    def validate_jwt(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            authorization_header = request.headers.get('Authorization')
            if authorization_header is None:
                raise errors.Unauthorized
            token_parts = authorization_header.split(' ')
            if len(token_parts) != 2:
                raise errors.Unauthorized
            token = token_parts[1]
            try:
                payload = jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM])
            except jwt.InvalidTokenError:
                raise errors.Unauthorized
            for field in ['email']:
                if field not in payload:
                    raise errors.Unauthorized
            email = payload.get('email')
            if not check_user_credentials(email=email):
                raise errors.Unauthorized
            kwargs['email'] = email

            return f(*args, **kwargs)

        return decorated_function

    return validate_jwt


def encode(account):
    iat = datetime.datetime.utcnow()
    return jwt.encode({
        'sub': account['email'],
        'iat': iat,
        'exp': iat + datetime.timedelta(days=365),
    }, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)


def decode(access_token):
    try:
        payload = jwt.decode(access_token, config.JWT_SECRET)
    except jwt.InvalidTokenError:
        return None
    return payload
