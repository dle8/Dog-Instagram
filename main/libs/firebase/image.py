from main.libs.firebase import bucket, users_ref
from main.libs.firebase.user import get_user_key_or_none
from werkzeug.utils import secure_filename
import datetime


def upload_user_image(image=None, email=None):
    try:
        blob = bucket.blob(email + '/' + secure_filename(image.filename))
        blob.upload_from_file(image)
    except Exception:
        raise Exception('There is an error uploading user picture')


def get_user_images(email=None):
    try:
        blobs = bucket.list_blobs(prefix=email)
        images = [{
            'url': blob.generate_signed_url(datetime.timedelta(seconds=3600), method='GET'),
            'name': blob.name
        } for blob in blobs]

        return images
    except Exception:
        raise Exception('There is an error getting user picture')


def delete_user_image(image_name=None, email=None):
    try:
        blob = bucket.blob(email + '/' + image_name)
        blob.delete()
    except Exception:
        raise Exception('There is an error deleting user picture')


def get_user_followees_images(email=None):
    try:
        images = []
        user_images = get_user_images(email)
        for user_image in user_images:
            images.append({
                'url': user_image['url'],
                'name': user_image['name'],
                'email': email
            })

        user_key = get_user_key_or_none(email=email)
        followees = users_ref.child(user_key).child('followees').get()
        for key, value in followees:
            followee_images = get_user_images(value['email'])
            for followee_image in followee_images:
                images.append({
                    'url': followee_image['url'],
                    'name': followee_image['name'],
                    'email': value['email']
                })

        return images
    except Exception:
        raise Exception('There is an error getting followees\' pictures')
