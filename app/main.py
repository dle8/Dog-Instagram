from flask import Flask, render_template, request, Response, redirect, session, url_for, g, send_file, jsonify, flash
from glob import glob
import os.path
import json
import hashlib
from UserInfo import AddUser, CheckCredentials, UserExists, upload_blob, download_blobs, delete_blob, getUserNewsfeed, addFollow, isFollowed, unFollow
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        s = request.form.to_dict()['json_string']
        json_acceptable_string = s.replace("'", "\"")
        d = json.loads(json_acceptable_string)

        ##hashes password
        h = hashlib.md5(d['password'].encode())
        hashed_password = h.hexdigest()

        if (CheckCredentials(d['username'], hashed_password)):
            session['user'] = d['username']
        else:
            return ("False")
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    print("Signing up")
    s = request.form.to_dict()['json_string']
    json_acceptable_string = s.replace("'", "\"")
    d = json.loads(json_acceptable_string)
    if (True):
        ##hashes password
        h = hashlib.md5(d['password'].encode())
        hashed_password = h.hexdigest()
        if AddUser(d['username'],hashed_password):
        ##starts session with this user
            session['user'] = d['username']
        else:
            return "False"

    return render_template('index.html')

@app.route('/landing')
def landing():
    if g.user:
        return render_template('landing.html', user = g.user)
    return redirect(url_for('login'))

@app.route('/dropsession')
def dropsession():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if g.user:
        return render_template('profile.html', user = g.user)
    return redirect(url_for('login'))

@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if not g.user:
        return redirect(url_for('login'))
    if request.method == "GET":
        return redirect(url_for('landing'))
    else:
        if 'image' not in request.files: # if nothing was uploaded
            return redirect(url_for('landing'))
        file = request.files['image']
        if file.filename == '':
            return redirect(url_for('landing'))
        if file:
            filename = secure_filename(file.filename)
            file.seek(0)
            upload_blob(file, g.user)
            flash("Image uploaded successfully")
            return redirect(url_for('landing'))

@app.route('/user/<username>/images')
def getUserImages(username):
    # get the images that belong to the user called <username>
    if not UserExists(username):
        print("User not existed")
        return "False"
    elif not g.user:
        return redirect(url_for('login'))
    return download_blobs(username)

@app.route('/user/images')
def getCurrentUserImages():
#     get all images belong to the current user
#   in the json list of image urls
    if not g.user:
        return redirect(url_for('login'))
    return getUserImages(g.user)

@app.route('/user/newsfeed')
def getCurrentUserNewsfeed():
#     get all images that belong to the one who the current user follows
    if not g.user:
        return redirect(url_for('login'))
    return getUserNewsfeed(g.user)

@app.route('/search/<username>', methods=["GET", "POST"])
def search(username):
    if not UserExists(username):
        return "False"
    if g.user:
        if (g.user == username):
            return render_template('profile.html', user=g.user)
        else:
            return render_template('search.html', user=username)
    else:
        return redirect(url_for('login'))

@app.route('/checkfollow/<username>', methods=["GET", "POST"])
def checkfollow(username):
    if not g.user:
        return redirect(url_for('login'))
    if not isFollowed(g.user, username):
        return "False"
    return "True"

@app.route('/follow/<username>', methods=["GET", "POST"])
def follow(username):
    if not g.user:
        return redirect(url_for('login'))
    if not isFollowed(g.user, username):
        addFollow(g.user, username)
    else:
        unFollow(g.user, username)
    return "True"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
