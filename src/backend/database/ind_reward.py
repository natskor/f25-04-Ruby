from backend.database.family_unit import *
from backend.database.family_unit import *
from backend.database.firestore import db as DB
from google.cloud.firestore_v1.base_query import FieldFilter

# Reward creation.
def create_ind_reward(email: str,
                      profile: str,
                      title: str,
                      lvl: int,
                      xp: int,
                      image: str):
    reward_ref = DB.collection("FAMILY UNIT").document(
                    email).collection("PROFILE").document(profile
                        ).collection("INDIVIDUAL REWARD").document(profile + ", " + title)
    reward_ref.set({
                     "Author": email,
                     "Recipient": profile,
                     "Title": title,
                     "Level Req": lvl,
                     "XP Req": xp,
                     "Image": image,
                     "Redeemed": False
                    })
    
# Reward redemption changes.
def check_redemption(email: str, profile: str, title: str, reward_cost: int):
    reward_ref = DB.collection("FAMILY UNIT").document(email).collection(
                    "PROFILE").document(profile).collection(
                        "INDIVIDUAL REWARD").document(profile + ", " + title)
    
    rew_lvl = reward_ref.get().to_dict().get("Level Req")
    
    if subtract_current_xp(email, profile, reward_cost, rew_lvl) is True:
        reward_ref.update({"Redeemed": True})
        return True
    else:
        return False

# Remove reward.
def remove_ind_reward(email: str, profile: str, title: str):
    DB.collection("FAMILY UNIT").document(email).collection(
        "PROFILE").document(profile).collection(
            "INDIVIDUAL REWARD").document(profile + ", " + title).delete()

# Get all data.
<<<<<<< HEAD
def get_ind_reward(name: str, recipient: str):
    search = DB.collection("INDIVIDUAL REWARD")
    result = search.where(
        filter=FieldFilter(
            "Title", "==", name
        )
    ).where(
        filter=FieldFilter(
            "Recipient", "==", recipient
        )
    ).stream()
=======
def get_ind_reward(email: str, profile: str, title: str):
    search = DB.collection("FAMILY UNIT").document(email).collection(
                "PROFILE").document(profile).collection("INDIVIDUAL REWARD")
    
    result = search.where(filter=FieldFilter("Title", "==", title)).stream()
>>>>>>> 6bb49a5eb33c5ebf29e77fa4b3d42dd8502b786c

    details = []
    for doc in result:
        details.append(doc.to_dict())

    return details

# Select data.
<<<<<<< HEAD
def select_ind_reward(name: str, recipient: str, column: str):
    search = DB.collection("INDIVIDUAL REWARD")
    result = search.where(
        filter=FieldFilter(
            "Title", "==", name
        )
    ).where(
        filter=FieldFilter(
            "Recipient", "==", recipient
        )
    ).stream()
=======
def select_ind_reward(email: str, profile: str, title: str, column: str):
    search = DB.collection("FAMILY UNIT").document(email).collection(
                "PROFILE").document(profile).collection("INDIVIDUAL REWARD")
    
    result = search.where(filter=FieldFilter("Title", "==", title)).stream()
>>>>>>> 6bb49a5eb33c5ebf29e77fa4b3d42dd8502b786c

    for doc in result:
        val = doc.to_dict()
    return val[column]
