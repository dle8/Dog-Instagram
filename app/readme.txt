The use of g.user to determine if a user is already logged in.
To check this we use before_request event from Flask.
Any function that are decorated with before_request will run before the view function each time a request is received
-> this a right place to setup our g.user variable

@app.before_request
def before_request():
    g.user = current_user