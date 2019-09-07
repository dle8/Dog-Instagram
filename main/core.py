from functools import wraps
from flask import request


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
