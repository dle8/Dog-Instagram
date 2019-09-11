#Dog Instagram

Dog-instagram is a photo-sharing website for dog lovers, which supports functionalities such as photo posting, real-time
messaging, user following, newsfeed displaying, user and dog breed searching with Firebase Realtime Database and Storage.

# Features
Photo posting
Real-time messaging
User following
Newsfeed displaying
User and dog breed searching

# Tech stacks
Python
Flask
Marshmallow
Keras
Firebase Realtime Database and Storage
Werkzeug

## Setup
1. Clone this repository by using this command: 
```
https://github.com/dle8/Dog-Instagram.git
cd Dog-Instagram
```
2. Create and start virtual env
```
virtualenv venv
. venv/bin/activate 
```
3. Install project dependencies
```
pip install -r requirements.txt
```
4. Goes into main/configs and clone another copy of base_sample.py and named it base.py
```
cd main/configs
mv base_sample.py base.py
```
5. Set the base configuration values which has been specified in the module base.py
6. The program base on FLASK_ENV environment variable to decide the environment of the project. So go ahead and set
FLASK_ENV to 'development' or 'production' to run in your desired testing. For example, setting the FLASK_ENV variable
into 'development':
```
export FLASK_ENV=development
```

## Todo list
- Integrate this backend implementation with a fancy front end!
- Set up a server on Google Cloud Engine or Heroku.
- Maybe this can open for cat-lovers as well?

ENJOY TESTING THE APIS!!