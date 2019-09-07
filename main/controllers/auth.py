from flask import jsonify
from main import app, errors
from main.core import parse_args_with
from main.schemas.user import AuthSchema, ConfirmationCodeSchema
from main.libs.firebase.user import create_user, get_user, set_user_attr
from main import jwttoken
from werkzeug.security import check_password_hash


@app.route('/auth', methods=['POST'])
@parse_args_with(AuthSchema())
def auth(args):
    email = args.get('email')
    user = get_user(email=email)
    if not user:
        raise errors.EmailAndPasswordNotMatch()
    hashed_password = user['password']
    if not check_password_hash(pwhash=hashed_password, password=args.get('password')):
        raise errors.EmailAndPasswordNotMatch()

    access_token = jwttoken.encode(user)
    return jsonify(access_token=access_token.decode('utf-8'))


@app.route('/register', methods=['POST'])
@parse_args_with(AuthSchema())
def register(args):
    email = args.get('email')
    user = get_user(email=email)
    if user:
        raise errors.UserEmailAlreadyExistedError()

    create_user(email=email, password=args.get('password'))
    return jsonify({'message': 'User created successfully. Please confirm your account.'})


@app.route('/confirm', methods=['POST'])
@parse_args_with(ConfirmationCodeSchema())
def confirm(args):
    email = args.get('email')
    user = get_user(email=email)
    if not user:
        raise errors.UserDoesNotExist()

    if user['confirmed']:
        return jsonify({'message': 'Email already confirmed'})

    set_user_attr(email=email, confirmed=True)
    return jsonify({'message': 'Account confirmed successfully'})


@app.route('/confirmation_email', methods=['POST'])
def get_confirmation_email():
    pass
