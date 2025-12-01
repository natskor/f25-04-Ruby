# from firestore import db as DB
from backend.database.firestore import db as DB

def get_family_reward(email: str):
    return(DB.collection("FAMILY UNIT").document(email).collection("COLLAB REWARD").document("reward"))

def create_collab_reward(
    name: str,
    desc: str,
    lvl: int,
    xp_goal: int,
    author: str
):
    reward_ref = DB.collection("COLLAB REWARD").document(name)
    reward_ref.set({
        "Title": name,
        "Description": desc,
        "Level Req": lvl,
        "XP Goal": xp_goal,
        "Current XP": 0,
        "Author": author,
        "Redeemed": False
    })
    
def update_collab_reward(name: str, add_xp: int):
    ref = DB.collection("COLLAB REWARD").document(name)
    doc = ref.get()
    
    if doc.exists:
        data = doc.to_dict()
        new_xp = data.get("Current XP", 0) + add_xp
        ref.update({"Current XP": new_xp})
        
def redeem_collab_reward(name: str):
    DB.collection("COLLAB REWARD").document(name).update({"Redeemed": True})

def get_all():
    all_rewards = DB.collection("COLLAB REWARD").stream()
    return [doc.to_dict() for doc in all_rewards]