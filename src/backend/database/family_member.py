from firestore import db as DB

##### DOCUMENT INITIALIZATION
doc_ref = DB.collection("FAMILY_MEMBER").document("KidOne")
doc_ref.set({ "MemberID": 1,
              "First": "Kid",
              "Last": "One",
              "Role": "child",
              "PIN": 12345,
              "FamilyID": 1 })

### ADD DATA

# Member ID (supplied email)
#def add_member_id():

# First Name
#def add_first_name():

# Last Name
#def add_last_name():

# Role
#def add_role():

# PIN
#def add_pin():

# Family ID (N/A right now)
#def add_family_id():


### RETRIEVE DATA

# Member ID (supplied email)


# First Name


# Last Name


# Role


# PIN


# Family ID (N/A right now)

