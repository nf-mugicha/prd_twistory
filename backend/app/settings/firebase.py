import firebase_admin
from firebase_admin import credentials, storage
from . import twitter_api

cred = credentials.Certificate(twitter_api.FIREBASE_STORAGE_PATH)
firebase_admin.initialize_app(
    cred, {
        "storageBucket": "aitter-twigene.appspot.com"
    })

bucket = storage.bucket()
