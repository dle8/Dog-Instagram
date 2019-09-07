import datetime
import os
import json
from werkzeug.utils import secure_filename
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("./test-firebase-e922f-firebase-adminsdk-pdic3-06d90c5c5e.json")
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://test-firebase-e922f.firebaseio.com',
    'storageBucket': 'test-firebase-e922f.appspot.com'
})
root = db.reference()
users_ref = root.child('users')

def AddUser(username, password):
    if UserExists(username):
        return False
    # newEntry = username + " " + password + "\n"
    users_ref.push({
        'username': username,
        'password': password
    })
    return True

def UserExists(username):
    users = users_ref.get()
    if (users == None):
        return False
    for key, val in users.items():
        if username == val['username']:
            return True
    return False

def CheckCredentials(username, password):
    users = users_ref.get()
    if (users == None):
        return False
    for key, val in users.items():
        if username == val['username'] and password == val['password']:
            return True
    return False

def upload_blob(file, username):
    # upload a file to the bucket
    bucket = storage.bucket()
    blob = bucket.blob(username+"/"+secure_filename(file.filename))
    blob.upload_from_file(file)

def download_blobs(user):
    # download all images for a user
    # blob: binary large object
    # doi tuong duoi dang nhi phan, co the duoc luu tru trong csdl
    # blob co the chua hinh anh, bang tinh, video clips, va cac tap tin thi hanh
    bucket = storage.bucket()
    blobs = bucket.list_blobs(prefix=user)
    a = []
    for blob in blobs:
        a.append({
            "link": blob.generate_signed_url(datetime.timedelta(seconds=300)),
            "name": blob.name
        })
    # convert python object to json string using json.dumps
    return json.dumps(a)

def delete_blob(username, imagename):
    # delete an image from the server
    bucket = storage.bucket()
    blob = bucket.blob(username+"/"+imagename)
    blob.delete()

def getUserNewsfeed(username):
    # get images from everyone this user follows
    bucket = storage.bucket()
    a = []
    users = users_ref.get()
    for key, val in users.items():
        if username == val['username']:
            follows = users_ref.child(key).child('follow').get()
            if follows != None:
                for keyf, valf in follows.items():
                    blobs = bucket.list_blobs(prefix=valf['user'])
                    for blob in blobs:
                        a.append({
                            "link": blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET'),
                            "name": blob.name,
                            "user": valf['user']
                        })
            break
    blobs = bucket.list_blobs(prefix=username)
    for blob in blobs:
        a.append({
            "link": blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET'),
            "name": blob.name,
            "user": username
        })
    return json.dumps(a)

def addFollow(username, user):
    # username: current user
    # user: username to follow
    if UserExists(username) and UserExists(user):
        users = users_ref.get()
        for key, val in users.items():
            if username == val['username']:
                flag = True
                follows = users_ref.child(key).child('follow').get()
                if follows != None:
                    for keyf, valf in follows.items():
                        if valf['user'] == user:
                            flag = False
                            break
                if flag:
                    users_ref.child(key).child('follow').push({'user': user})
                else:
                    return "False"

def unFollow(username, user):
    if UserExists(username) and UserExists(user):
        users = users_ref.get()
        for key, val in users.items():
            if username == val['username']:
                follows = users_ref.child(key).child('follow').get()
                if follows != None:
                    for keyf, valf in follows.items():
                        if valf['user'] == user:
                            users_ref.child(key).child('follow').update({ keyf: None})


def isFollowed(username, user):
    # check if the current user follows user
    users = users_ref.get()
    for key, val in users.items():
        if username == val['username']:
            follows = users_ref.child(key).child('follow').get()
            if follows == None:
                break
            for keyf, valf in follows.items():
                if valf['user'] == user:
                    return True
    return False