from firestore import db as DB
from google.cloud.firestore_v1.base_query import FieldFilter

# Create a chore.
def create_chore(title: str, 
                 desc: str, 
                 xp_val: int, 
                 auth: str, 
                 recipient: str):
    chore_ref = DB.collection("CHORE").document(recipient + ", " + title)
    chore_ref.set({
        "Title": title,
        "Description": desc,
        "XP Value": xp_val,
        "Status": "Not Completed!",
        "Author": auth,
        "Recipient": recipient
    })

# Chore completion changes.
def complete_chore(title: str, recipient: str):
    DB.collection("CHORE").document(
        recipient + ", " + title
    ).update({"Status": "Completed!"})

# Remove chore.
def remove_chore(title: str, recipient: str):
    DB.collection("CHORE").document(
        recipient + ", " + title
    ).delete()

# Get all data.
def get_chore(title: str, recipient: str):
    search = DB.collection("CHORE")

    result = search.where(
        filter = FieldFilter(
            "Title", "==", title
        )
    ).where(
        filter = FieldFilter(
            "Recipient", "==", recipient
        )
    ).stream()

    for doc in result:
        print(f"{doc.id} => {doc.to_dict()}")

# Select data.
def select_chore(title: str, recipient: str, column: str):
    search = DB.collection("CHORE")

    result = search.where(
        filter = FieldFilter(
            "Title", "==", title
        )
    ).where(
        filter = FieldFilter(
            "Recipient", "==", recipient
        )
    ).stream()

    for doc in result:
        val = doc.to_dict()
        print(f"{val[column]}")
