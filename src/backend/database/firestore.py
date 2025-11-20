import os
from dotenv import load_dotenv

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

### Load our environment variable
load_dotenv()
### Get the environment variable
service_account = os.getenv("GOOGLE_FS_DB_CREDS")

### I used a relative path, so this should only apply if you do as well
if not os.path.isabs(service_account):
    service_account = os.path.abspath(service_account)

### Access to Firestore
cred = credentials.Certificate(service_account)
firebase_admin.initialize_app(cred)

### Database Object
db = firestore.client()
