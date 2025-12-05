from backend.database.firestore import db as DB
from google.cloud.firestore_v1.base_query import FieldFilter

# Create a chore
def create_chore(email: str,
                 title: str, 
                 desc: str, 
                 xp_val: int, 
                 assigned_to: str, 
                 due_date: str,
                 task_type: str):
    # Use a collection reference to generate an auto-ID
    chore_ref = DB.collection("FAMILY UNIT").document(email).collection("CHORE").document()
    
    chore_data = {
        "id": chore_ref.id,
        "Title": title,
        "Description": desc,
        "XP Value": xp_val,
        "Status": "Not Completed!",
        "Completed": False,
        "Submitted": False,
        "AssignedTo": assigned_to,
        "DueDate": due_date,
        "TaskType": task_type
    }
    
    chore_ref.set(chore_data)
    return chore_data

# Mark chore as complete
def complete_chore(email: str, chore_id: str):
    doc_ref = DB.collection("FAMILY UNIT").document(email).collection("CHORE").document(chore_id)
    doc = doc_ref.get()
    
    if doc.exists:
        doc_ref.update({
            "Status": "Completed!",
            "Completed": True
        })
        return doc.to_dict()  # Return the chore data so we know how many points to award
    else:
        raise Exception("Chore not found")

# Remove chore
def remove_chore(email: str, chore_id: str):
    DB.collection("FAMILY UNIT").document(email).collection("CHORE").document(chore_id).delete()

# Get all chores (useful for the dashboard)
def get_all_chores(email: str):
    docs = DB.collection("FAMILY UNIT").document(email).collection("CHORE").stream()
    chores = []
    for doc in docs:
        chores.append(doc.to_dict())
    return chores

# Get chores specific to a user
def get_chores_by_user(email: str, username: str):
    search = DB.collection("FAMILY UNIT").document(email).collection("CHORE")
    result = search.where(filter=FieldFilter("AssignedTo", "==", username)).stream()
    
    chores = []
    for doc in result:
        chores.append(doc.to_dict())
    return chores

# Get single chore by ID
def get_chore_by_id(email: str, chore_id: str):
    doc = DB.collection("FAMILY UNIT").document(email).collection("CHORE").document(chore_id).get()
    if doc.exists:
        return doc.to_dict()
    return None