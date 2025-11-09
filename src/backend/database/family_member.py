from firestore import db as DB

##### DOCUMENT INITIALIZATION
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
# Member ID (supplied email)
#def get_member_id(email: str):

# First Name
#def get_first_name(email: str):

# Last Name
#def get_last_name(email: str):

# Role
#def get_role(email: str):

# PIN
#def get_pin(email: str):

# Family ID (N/A right now)
#def get_family_id(email: str):