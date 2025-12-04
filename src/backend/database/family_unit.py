from backend.database.firestore import db as DB
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

### "FAMILY" collection.

def add_username(email: str, username: str):
    account = DB.collection("FAMILY UNIT").document(email)
    account.update({"Username": username})


def add_password(email: str, password: str):
    account = DB.collection("FAMILY UNIT").document(email)
    account.update({"Password": password})


def add_role(email: str, user: str, role: str):
    profile_ref = DB.collection("FAMILY UNIT").document(email).collection("PROFILE").document(user)
    profile_ref.update({"Role": role})


def get_family_info(email: str):
    search = DB.collection("FAMILY UNIT")
    result = search.where(filter=FieldFilter("FamilyID", "==", email)).stream()
    
    details = []
    for doc in result:
        details.append(doc.to_dict())

    return details

       
def select_family_info(email: str, column: str):
    search = DB.collection("FAMILY UNIT")
    result = search.where(filter=FieldFilter("FamilyID", "==", email)).stream()
    
    for doc in result:
        val = doc.to_dict()
    
    return val[column]


### "PROFILE" sub-collection.

def add_pin(email: str, user: str, pin: str):
    profile_ref = DB.collection("FAMILY UNIT").document(email).collection("PROFILE").document(user)
    profile_ref.update({"PIN": pin})


def add_avatar(email: str, user: str, avatar: str):
    profile_ref = DB.collection("FAMILY UNIT").document(email).collection("PROFILE").document(user)
    profile_ref.update({"Avatar": avatar})


def get_profile_info(email: str, user: str):
    search = DB.collection("FAMILY UNIT").document(email).collection("PROFILE")
    result = search.where(filter=FieldFilter("User", "==", user)).stream()
    
    details = []
    for doc in result:
        details.append(doc.to_dict())

    return details


def select_profile_info(email: str, user: str, column: str):
    search = DB.collection("FAMILY UNIT").document(email).collection("PROFILE")
    result = search.where(filter=FieldFilter("User", "==", user)).stream()
    
    for doc in result:
        val = doc.to_dict()
    
    return val[column]


### "PROGRESSION" sub-sub-collection.

def set_needed_xp(email: str, user: str, set_amount: int):
    prog_ref = DB.collection(
        "FAMILY UNIT").document(email).collection(
            "PROFILE").document(user).collection(
                "PROGRESSION").document(user + " Prog.")
    prog_ref.update({"Needed XP": set_amount})


def add_current_xp(email: str, user: str, amount: int):
    prog_ref = DB.collection(
        "FAMILY UNIT").document(email).collection(
            "PROFILE").document(user).collection(
                "PROGRESSION").document(user + " Prog.")
    
    need_xp = prog_ref.get().to_dict().get("Needed XP")
    curr_xp = prog_ref.get().to_dict().get("Current XP")
    total_xp = need_xp + curr_xp

    prog_ref.update({"Current XP": Increment(amount), 
                     "Needed XP": Increment(-(amount))})
    increment_level(email, user, total_xp)


def increment_level(email:str, user: str, prev_goal: int):
    prog_ref = DB.collection(
        "FAMILY UNIT").document(email).collection(
            "PROFILE").document(user).collection("PROGRESSION").document(user + " Prog.")

    need_xp = prog_ref.get().to_dict().get("Needed XP")
    set_need = prev_goal + 100
    
    if need_xp is not None and need_xp <= 0:
        prog_ref.update({"Current Level": Increment(1),
                         "Next Level": Increment(1)})
        prog_ref.update({"Current XP": 0})
        set_needed_xp(email, user, set_need)

def subtract_current_xp(email: str, user: str, reward_cost: int, reward_level: int) -> bool:
    prog_ref = DB.collection(
        "FAMILY UNIT").document(email).collection(
            "PROFILE").document(user).collection(
                "PROGRESSION").document(user + " Prog.")
    
    curr_xp = prog_ref.get().to_dict().get("Current XP")
    curr_lvl = prog_ref.get().to_dict().get("Current Level")

    if curr_xp >= reward_cost and curr_lvl >= reward_level:
        prog_ref.update({"Current XP": Increment(-(reward_cost)),
                         "Needed XP": Increment(reward_cost)})
        return True
    else:
        print("Not enough XP for reward.")
        return False


def get_experience_info(email: str, user: str):
    search = DB.collection(
        "FAMILY UNIT").document(email).collection(
            "PROFILE").document(user).collection(
                "PROGRESSION")
    result = search.where(filter=FieldFilter("User", "==", user)).stream()
    
    details = []
    for doc in result:
        details.append(doc.to_dict())

    return details


def select_progression_info(email: str, user: str, column: str):
    search = DB.collection(
        "FAMILY UNIT").document(email).collection(
            "PROFILE").document(user).collection(
                "PROGRESSION")
    result = search.where(filter=FieldFilter("User", "==", user)).stream()
    
    for doc in result:
        val = doc.to_dict()
    return val[column]
