from firestore import db as DB
from google.cloud.firestore_v1.base_query import FieldFilter

# Reward creation.
def create_ind_reward(name: str, 
                      desc: str, 
                      lvl: int,
                      xp: int, 
                      author: str,
                      recipient: str):
    reward_ref = DB.collection("INDIVIDUAL REWARD").document(
        recipient + ", " + name
        )
    reward_ref.set({
                     "Title": name,
                     "Description": desc,
                     "Level Req": lvl,
                     "XP Req": xp,
                     "Author": author,
                     "Recipient": recipient,
                     "Redeemed": False
                    })
    
# Reward redemption changes.
def redeem_ind_reward(name: str, recipient: str):
    DB.collection("INDIVIDUAL REWARD").document(
        recipient + ", " + name
        ).update({"Redeemed": True})

# Remove reward.
def remove_ind_reward(name: str, recipient: str):
    DB.collection("INDIVIDUAL REWARD").document(
        recipient + ", " + name
    ).delete()

# Get all data.
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

    for doc in result:
        print(f"{doc.id} => {doc.to_dict()}")

# Select data.
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

    for doc in result:
        val = doc.to_dict()
        print(f"{val[column]}")
