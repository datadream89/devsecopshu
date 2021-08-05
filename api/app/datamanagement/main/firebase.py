import pyrebase
from datamanagement.configuration import key

# import json
# with open("./ServiceAccountKey.json", "r") as f:
#   api_keys = json.load(f.read())



def get_files():
  # pdb.set_trace()
  firebase = pyrebase.initialize_app(key.FIREBASE_CONFIG)
  storage = firebase.storage()

  # storage.child("uploads/srv_data.csv").download("./srv_data.csv")
  print(storage.list_files())

if __name__ == "__main__":
  get_files()
