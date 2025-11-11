from firestore import db as DB
from google.cloud.firestore_v1.base_query import FieldFilter

### DOCUMENT INITIALIZATION
def create_member(email: str):
    new_member = DB.collection("FAMILY MEMBER").document(email)
    new_member.set({ 
                     "MemberID": email,
                     "First":    "",
                     "Last":     "",
                     "Role":     "",
                     "PIN":      0000,
                     "FamilyID": 0 
                    })

### ADD DATA

# Member ID (supplied email)
def add_member_id(email: str):
    member = DB.collection("FAMILY MEMBER").document(email)
    member.update({"MemberID": email})

# First Name
def add_first_name(email: str, first: str):
    member = DB.collection("FAMILY MEMBER").document(email)
    member.update({"First": first})

# Last Name
def add_last_name(email: str, last: str):
    member = DB.collection("FAMILY MEMBER").document(email)
    member.update({"Last": last})

# Role
def add_role(email: str, role: str):
    member = DB.collection("FAMILY MEMBER").document(email)
    member.update({"Role": role})

# PIN
def add_pin(email: str, pin: int):
    member = DB.collection("FAMILY MEMBER").document(email)
    member.update({"PIN": pin})

# Family ID (N/A right now)
def add_family_id(email: str, family_id: int):
    member = DB.collection("FAMILY MEMBER").document(email)
    member.update({"FamilyID": family_id})

### RETRIEVE DATA

# Provide: the member's email.
# Returns: formatted information of member information.
def get_member_info(email: str):
    search = DB.collection("FAMILY MEMBER")
    result = search.where(filter=FieldFilter("MemberID", "==", email)).stream()
    
    for doc in result:
        print(f"{doc.id} => {doc.to_dict()}")

# LOGGING OFF, WORK IN PROGRESS!
# Provide: the member's email & desired "column".
# Returns: selected member's information.
#def select_member_info(email: str, column: str):
#    search = DB.collection("FAMILY MEMBER")
#    result = search.where(filter=FieldFilter("MemberID", "==", email.stream()))
#    
#    for doc in result:
#        print(f"{doc.to_dict()}")