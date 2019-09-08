from main import errors
from werkzeug.security import generate_password_hash, check_password_hash
from main.libs.firebase import users_ref


def create_user(email=None, password=None):
    try:
        user_key = get_user_key_or_none(email)
        if user_key:
            raise errors.UserEmailAlreadyExistedError()

        users_ref.push({
            'email': email,
            'password': generate_password_hash(password),
            'confirmed': False
        })
    except Exception:
        raise Exception('There is an error in creating a new user')


def check_user_credentials(email=None, password=None):
    try:
        user_key = get_user_key_or_none(email)
        if not user_key:
            return False
        if password:
            hashed_password_in_db = users_ref.child(user_key).get()['password']
            if not check_password_hash(pwhash=hashed_password_in_db, password=password):
                return False

        return True
    except Exception:
        raise Exception('There is an error in checking user credentials')


def set_user_attr(**kwargs):
    try:
        if 'email' in kwargs:
            user_key = get_user_key_or_none(email=kwargs['email'])
            if 'password' in kwargs:
                users_ref.child(user_key).child('password').set(kwargs['password'])
            if 'confirmed' in kwargs:
                users_ref.child(user_key).child('confirmed').set(kwargs['confirmed'])
    except Exception:
        raise Exception('There is an error in setting user attribute')


def get_user_key_or_none(email=None):
    try:
        users = users_ref.get()
        for key, val in users.items():
            if email == val['email']:
                return key

        return None
    except Exception:
        raise Exception('There is an error in getting user information')


def update_user_follow(follower_email, followee_email):
    try:
        follower_key = get_user_key_or_none(email=follower_email)
        followee_key = get_user_key_or_none(email=followee_email)
        if not follower_key or not followee_key:
            raise errors.UserDoesNotExist()

        followee_followers = users_ref.child(followee_key).child('followers').get()
        follower_followees = users_ref.child(follower_key).child('followees').get()

        followed = False
        if followee_followers:
            for key, value in followee_followers.items():
                if value['email'] == follower_email:
                    followed = True
                    users_ref.child(followee_key).child('followers').child(key).delete()

            if not followed:
                users_ref.child(followee_key).child('followers').push({'email': follower_email})
        else:
            users_ref.child(followee_key).child('followers').push({'email': follower_email})

        if follower_followees:
            for key, value in follower_followees.items():
                if value['email'] == followee_email:
                    users_ref.child(follower_key).child('followees').child(key).delete()

            if not followed:
                users_ref.child(follower_key).child('followees').push({'email': followee_email})
        else:
            users_ref.child(follower_key).child('followees').push({'email': followee_email})

        return followed
    except Exception:
        raise Exception('There is an error following another user')
