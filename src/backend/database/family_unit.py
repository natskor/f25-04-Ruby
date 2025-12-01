from firestore import db as DB
#from backend.database.firestore import db as DB
from google.cloud.firestore_v1.base_query import FieldFilter
from google.cloud.firestore import Increment

# New family account creation.

def create_family(email: str):
    family_ref = DB.collection("FAMILY UNIT").document(email)
    family_ref.set({ 
                     "FamilyID": email,
                     "Username": "",
                     "Password": "", 
                    })

# New profile creation for family account.

def create_profile(email: str, user: str):
    family_ref = DB.collection("FAMILY UNIT").document(email)
    new_profile = family_ref.collection("PROFILE").document(user)
    new_profile.set({
                     "User": user,
                     "Avatar": "",
                     "Role": "",
                     "PIN": "",
                    })

# New progress creation for an individual user's profile.

def create_profile_progress(email: str, user: str):
    family_ref = DB.collection("FAMILY UNIT").document(email)
    profile_ref = family_ref.collection("PROFILE").document(user)
    user_xp_ref = profile_ref.collection("PROGRESSION").document(
        user + " Prog."    
    )
    user_xp_ref.set({
        "User": user,
        "Next Level": 1,
        "Needed XP": 100,
        "Current Level": 0,
        "Current XP": 0
    })

##### Add Data - FAMILY UNIT collection.

def add_username(email: str, username: str):
    account = DB.collection("FAMILY UNIT").document(email)
    account.update({"Username": username})

def add_password(email: str, password: str):
    account = DB.collection("FAMILY UNIT").document(email)
    account.update({"Password": password})

##### Add Data - PROFILE subcollection.

def add_role(email: str, user: str, role: str):
    profile_ref = DB.collection("FAMILY UNIT").document(email).collection("PROFILE").document(user)
    profile_ref.update({"Role": role})

def add_pin(email: str, user: str, pin: str):
    profile_ref = DB.collection("FAMILY UNIT").document(email).collection("PROFILE").document(user)
    profile_ref.update({"PIN": pin})

def add_avatar(email: str, user: str, avatar: str):
    profile_ref = DB.collection("FAMILY UNIT").document(email).collection("PROFILE").document(user)
    profile_ref.update({"Avatar": avatar})

##### Add Data - PROGRESSION sub-subcollection

# This will be NEEDED when the child reaches the next level.
def set_needed_xp(email: str, user: str, set_amount: int):
    prog_ref = DB.collection(
        "FAMILY UNIT").document(email).collection(
            "PROFILE").document(user).collection(
                "PROGRESSION").document(user + " Prog.")
    prog_ref.update({"Needed XP": set_amount})

def update_progression(email: str, user: str, amount: int):
    prog_ref = DB.collection(
        "FAMILY UNIT").document(email).collection(
            "PROFILE").document(user).collection(
                "PROGRESSION").document(user + " Prog.")
    
    prog_ref.update({"Current XP": Increment(amount), 
                     "Needed XP": Increment(-(amount))})
    increment_level(email, user)

# Nested inside of update_progression()... Should not be used.
def increment_level(email:str, user: str):
    prog_ref = DB.collection(
        "FAMILY UNIT").document(email).collection(
            "PROFILE").document(user).collection("PROGRESSION").document(user + " Prog.")
    
    user_doc = prog_ref.get()
    data = user_doc.to_dict()
    need_xp = data.get("Needed XP")
    
    if need_xp is not None and need_xp <= 0:
        prog_ref.update({"Current Level": Increment(1),
                         "Next Level": Increment(1),
                         "Current XP": 0})

##### Get Data - FAMILY UNIT collection.

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

##### Get Data - PROFILE subcollection.

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


##### Get Data - PROGRESSION sub-subcollection

def get_experience_info(email: str, user: str):
    search = DB.collection(
        "FAMILY UNIT").document(email).collection(
            "PROFILE").document(user).collection(
                "PROGRESSION")
    result = search.where(filter=FieldFilter("User", "==", user)).stream()
    
    for doc in result:
        print(f"{doc.id} => {doc.to_dict()}")

def select_progression_info(email: str, user: str, column: str):
    search = DB.collection(
        "FAMILY UNIT").document(email).collection(
            "PROFILE").document(user).collection(
                "PROGRESSION")
    result = search.where(filter=FieldFilter("User", "==", user)).stream()
    
    for doc in result:
        val = doc.to_dict()
        print(f"{val[column]}")

###########################################################
### Testing area.
###########################################################
# VARIABLES THAT ARE USED
email : str = "parent@gmail.com"
user_name : str = "Metal Eater"
password : str = "superDopePassword77"
role : str = "Parent"
avatar : str = "wizard"
give_this : int = 200
set_this : int = 500
###########################################################
# FAMILY operations
#create_family(email)
#add_username(email, user_name)
#add_password(email, password)

#get_family_info(email)
#select_family_info(email, "FamilyID")
#select_family_info(email, "Username")
#select_family_info(email, "Password")
###########################################################
# PROFILE operations
#create_profile(email, user_name)
#add_role(email, user_name, role)
#add_pin(email, user_name, password)
#add_avatar(email, user_name, avatar)

#get_profile_info(email, user_name)
#select_profile_info(email, user_name, "User")
#select_profile_info(email, user_name, "Avatar")
#select_profile_info(email, user_name, "Role")
#select_profile_info(email, user_name, "PIN")
###########################################################
# PROGRESSION operations
#create_profile_progress(email, user_name)
#set_needed_xp(email, user_name, set_this)
#update_progression(email, user_name, give_this)

#get_experience_info(email, user_name)
#select_progression_info(email, user_name, "User")
#select_progression_info(email, user_name, "Next Level")
#select_progression_info(email, user_name, "Needed XP")
#select_progression_info(email, user_name, "Current Level")
#select_progression_info(email, user_name, "Current XP")
###########################################################