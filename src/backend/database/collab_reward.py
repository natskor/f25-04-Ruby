from backend.database.firestore import db as DB

def get_family_reward(email: str):
    ref = (DB.collection("FAMILY UNIT")
               .document(email)
               .collection("COLLAB REWARD")
               .document("active"))
    doc = ref.get()
    if doc.exists():
        return doc.to_dict()
    return None

def create_collab_reward(
    email: str,
    name: str,
    desc: str,
    lvl: int,
    xp_goal: int,
):
    reward_ref = (DB.collection("FAMILY UNIT")
                  .document(email)
                  .collection("COLLAB REWARD")
                  .document("active"))
    
    reward_ref.set({
        "Title": name,
        "Description": desc,
        "Level Req": lvl,
        "XP Goal": xp_goal,
        "Current XP": 0,
    })
    
    return True
    
def update_collab_reward(email: str, add_xp: int):
    ref = (DB.collection("FAMILY UNIT")
           .document(email)
           .collection("COLLAB REWARD")
           .document("active"))
    
    doc = ref.get()
    
    if doc.exists:
        current = doc.to_dict().get("Current XP", 0)
        ref.update({"Current XP": current + add_xp})

def clear_collab_reward(email: str):
    reward_ref = (
        DB.collection("FAMILY UNIT")
          .document(email)
          .collection("COLLAB REWARD")
          .document("active")
    )
    reward_ref.delete()