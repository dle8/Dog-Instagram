import firebase_admin
from firebase_admin import credentials, db, storage
from main.config import config

cred = credentials.Certificate(config.CREDENTIALS_DIR_PATH + '/' + config.FIREBASE_ADMINSDK_JSON)
firebase_app = firebase_admin.initialize_app(cred, {
    'databaseURL': config.DATABASE_URL,
    'storageBucket': config.STORAGE_BUCKET
})

root = db.reference()
users_ref = root.child('users')
messages_ref = root.child('messages')
bucket = storage.bucket()
