from flask import jsonify
from main import app, errors
from main.utils import jwt_required
from main.libs.firebase.user import update_user_follow


@app.route('/users/<string:email>/follows/<string:followee_email>', methods=['PUT'])
@jwt_required()
def update_follow(email, followee_email, **kwargs):
    if email != kwargs['sub']:
        raise errors.Unauthorized()
    followed = update_user_follow(follower_email=email, followee_email=followee_email)
    if followed:
        message = 'Unfollowed.'
    else:
        message = 'Followed.'

    return jsonify({'message': message})
