from firestore import db as DB
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
def create_profile(email: str, user: str):
    family_ref = DB.collection("FAMILY UNIT").document(email)
    new_profile = family_ref.collection("PROFILE").document(user)
    new_profile.set({
                     "User": user,
                     "Role": "",
                     "PIN": 0000
                    })

### Add Data - FAMILY UNIT collection.

def add_password(email: str, password: str):
    account = DB.collection("FAMILY UNIT").document(email)
    account.update({"Password": password})

### Add Data - PROFILE subcollection.

def add_role(email: str, user: str, role: str):
    profile_ref = DB.collection("FAMILY UNIT").document(email).collection("PROFILE").document(user)
    profile_ref.update({"Role": role})

def add_pin(email: str, user: str, pin: int):
    profile_ref = DB.collection("FAMILY UNIT").document(email).collection("PROFILE").document(user)
    profile_ref.update({"PIN": pin})

### Get Data - FAMILY UNIT collection.

def get_family_info(email: str):
    search = DB.collection("FAMILY UNIT")
    result = search.where(filter=FieldFilter("FamilyID", "==", email)).stream()
    
    for doc in result:
        print(f"{doc.id} => {doc.to_dict()}")

def select_family_info(email: str, column: str):
    search = DB.collection("FAMILY UNIT")
    result = search.where(filter=FieldFilter("FamilyID", "==", email)).stream()
    
    for doc in result:
        val = doc.to_dict()
        print(f"{val[column]}")

### Get Data - PROFILE subcollection.

def get_profile_info(email: str, user: str):
    search = DB.collection("FAMILY UNIT").document(email).collection("PROFILE")
    result = search.where(filter=FieldFilter("User", "==", user)).stream()
    
    for doc in result:
        print(f"{doc.id} => {doc.to_dict()}")
    
def select_profile_info(email: str, user: str, column: str):
    search = DB.collection("FAMILY UNIT").document(email).collection("PROFILE")
    result = search.where(filter=FieldFilter("User", "==", user)).stream()
    
    for doc in result:
        val = doc.to_dict()
        print(f"{val[column]}")

### Testing area...

# Display ALL data from each, respectively.
#get_family_info("TEST@email")
#get_profile_info("TEST@email", "Chud")

# Display SELECTED data from each.
#select_family_info("TEST@email", "FamilyID")
#select_family_info("TEST@email", "Password")

#select_profile_info("TEST@email", "Chud", "User")
#select_profile_info("TEST@email", "Chud", "Role")
#select_profile_info("TEST@email", "Chud", "PIN")