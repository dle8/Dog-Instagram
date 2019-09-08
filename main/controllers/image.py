from flask import jsonify, request
from main import app, errors
from main.utils import jwt_required
from main.libs.firebase.image import get_user_images, upload_user_image, delete_user_image, get_user_followees_images
# from main.dog_detector import dog_included

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}


def allowed_image_extension(image_name):
    return '.' in image_name and \
           image_name.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/users/<string:email>', methods=['GET'])
@jwt_required()
def get_followees_images(email):
    images = get_user_followees_images(email=email)

    return jsonify(images)


@app.route('/users/<string:email>/images', methods=['GET'])
@jwt_required()
def get_images(email):
    images = get_user_images(email=email)

    return jsonify(images)


@app.route('/users/<string:email>/images/<string:image_name>', methods=['DELETE'])
@jwt_required()
def delete_image(email, image_name):
    delete_user_image(email=email, image_name=image_name)

    return jsonify({'message': 'Image deleted successfully'})


@app.route('/users/<string:email>/images', methods=['POST'])
@jwt_required()
def upload_image(email):
    if 'file' not in request.files:
        raise errors.BadRequest('Please attach an image.')
    file = request.files['file']
    if allowed_image_extension(file.filename):
        # if dog_included(file):
        file.seek(0)
        upload_user_image(email=email, image=file)
        # else:
        #     raise errors.BadRequest('Can only upload pictures of doggo!')

    return jsonify({'message': 'Picture uploaded successfully'})
