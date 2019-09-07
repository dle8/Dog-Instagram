import firebase_admin
from firebase_admin import credentials, db, storage
from main.config import config
from main import errors
from werkzeug.security import generate_password_hash

FIREBASE_ADMINSDK_JSON = 'dog-instagram-firebase-adminsdk.json'

cred = credentials.Certificate(config.CREDENTIALS_DIR_PATH + '/' + FIREBASE_ADMINSDK_JSON)
firebase_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://dog-instagram.firebaseio.com/',
    'storageBucket': 'dog-instagram.appspot.com'
})
root = db.reference()
users_ref = root.child('users')


def create_user(email=None, password=None):
    try:
        user = get_user(email)
        if user:
            raise errors.UserEmailAlreadyExistedError()

        users_ref.push({
            'email': email,
            'password': generate_password_hash(password),
            'confirmed': False
        })
    except Exception:
        raise Exception('There is an error in creating a new user')


def set_user_attr(**kwargs):
    try:
        if 'email' in kwargs:
            user = get_user(email=kwargs['email'])
            if 'password' in kwargs:
                user.child('password').set(kwargs['password'])
            if 'confirm' in kwargs:
                user.child('confirmed').set(kwargs['confirmed'])
    except Exception:
        raise Exception('There is an error in setting user attribute')


def get_user(email=None):
    try:
        users = users_ref.get()
        if users:
            for user in users.values():
                if email == user['email']:
                    return user
        return None
    except Exception:
        raise Exception('There is an error in getting user information')
