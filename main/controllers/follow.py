from flask import jsonify
from main import app
from main.utils import jwt_required
from main.libs.firebase.user import update_user_follow


@app.route('/users/<string:email>/follows/<string:followee_email>', methods=['PUT'])
@jwt_required()
def update_follow(email, followee_email):
    follow_status = update_user_follow(follower_email=email, followee_email=followee_email)
    if not follow_status:
        message = 'User unfollowed.'
    else:
        message = 'User followed.'

    return jsonify({'message': message})
