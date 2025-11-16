from backend.database.firestore import db as DB
from google.cloud.firestore_v1.base_query import FieldFilter

### Initialization.

# New family account creation.
def create_family(email: str):
    family_ref = DB.collection("FAMILY UNIT").document(email)
    family_ref.set({ 
                     "FamilyID": email,
                     "Password": "", 
                    })

# New profile creation for family account.
def create_profile(email: str, first: str):
    family_ref = DB.collection("FAMILY UNIT").document(email)
    new_profile = family_ref.collection("PROFILE").document(first)
    new_profile.set({
                     "First": first,
                     "Last": "",
                     "Role": "",
                     "PIN": 0000
                    })

### Add Data - FAMILY UNIT collection.

def add_password(email: str, password: str):
    account = DB.collection("FAMILY UNIT").document(email)
    account.update({"Password": password})

### Add Data - PROFILE subcollection.

def add_last(email: str, first: str, last: str):
    profile_ref = DB.collection("FAMILY UNIT").document(email).collection("PROFILE").document(first)
    profile_ref.update({"Last": last})

def add_role(email: str, first: str, role: str):
    profile_ref = DB.collection("FAMILY UNIT").document(email).collection("PROFILE").document(first)
    profile_ref.update({"Role": role})
    
def add_pin(email: str, first: str, pin: int):
    profile_ref = DB.collection("FAMILY UNIT").document(email).collection("PROFILE").document(first)
    profile_ref.update({"Role": pin})

### Get Data - FAMILY UNIT collection. -!!! Not working currently. Fix later.

def get_family_info(email: str):
    search = DB.collection("FAMILY UNIT").document(email)
    result = search.where(filter=FieldFilter("FamilyID", "==", email))
    
    for doc in result:
        print(f"{doc.id} => {doc.to_dict()}")

### Get Data - PROFILE subcollection. -!!! Not working currently. Fix later.

def get_profile_info(email: str, first: str):
    search = DB.collection("FAMILY UNIT").document(email).collection("PROFILE").document(first)
    result = search.where(filter=FieldFilter("First", "==", first))
    
    for doc in result:
        print(f"{doc.id} => {doc.to_dict()}")
    
### Testing area...

## FAMILY UNIT collection.
#create_family("test@email")
#add_password("test@email", "yolo")

## PROFILE subcollection.
#create_profile("test@email", "chud")
#add_last("test@email", "chud", "life")
#add_role("test@email", "chud", "child")
#add_pin("test@email", "chud", 1234)

## Display data from each.
#get_family_info("test@email")
#get_profile_info("test@email", "chud")