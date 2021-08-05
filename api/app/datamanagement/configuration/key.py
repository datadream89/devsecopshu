import os

SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'



FIREBASE_CONFIG = {
    "apiKey": "AIzaSyDEvwCMalayYXnmT-XnyAY9gy1QnkPlV5A",
    "authDomain": "dqwebapp.firebaseapp.com",
    "projectId": "dqwebapp",
    "storageBucket": "dqwebapp.appspot.com",
    "databaseURL": "https://dqwebapp-default-rtdb.firebaseio.com", #"https://dqwebapp.firebaseio.com",
    "messagingSenderId": "729746220608",
    "appId": "1:729746220608:web:15c760180d48945139a1a5",
    "serviceAccount": os.path.abspath(os.path.dirname(__file__)) + "/serviceAccountKey.json"
}



