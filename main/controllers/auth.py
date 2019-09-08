from flask import jsonify
from main import app, errors
from main.utils import parse_args_with
from main.schemas.user import AuthSchema, ConfirmationCodeSchema
from main.libs.firebase.user import create_user, get_user_key_or_none, check_user_credentials
from main import utils


@app.route('/auth', methods=['POST'])
@parse_args_with(AuthSchema())
def auth(args):
    check_user_credentials(email=args.get('email'), password=args.get('password'))
    access_token = utils.encode({'email': args.get('email')})
    return jsonify(access_token=access_token.decode('utf-8'))


@app.route('/register', methods=['POST'])
@parse_args_with(AuthSchema())
def register(args):
    email = args.get('email')
    user_key = get_user_key_or_none(email=email)
    if user_key:
        raise errors.UserEmailAlreadyExistedError()

    create_user(email=email, password=args.get('password'))
    return jsonify({'message': 'User created successfully. Please confirm your account.'})


@app.route('/confirm', methods=['POST'])
@parse_args_with(ConfirmationCodeSchema())
def confirm(args):
    email = args.get('email')
    user_key = get_user_key_or_none(email=email)
    if not user_key:
        raise errors.UserDoesNotExist()

    # if user['confirmed']:
    #     return jsonify({'message': 'Email already confirmed'})
    #
    # set_user_attr(email=email, confirmed=True)
    return jsonify({'message': 'Account confirmed successfully'})


@app.route('/confirmation_email', methods=['POST'])
def get_confirmation_email():
    pass
