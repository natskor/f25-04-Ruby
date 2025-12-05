from fastapi import APIRouter, Form, HTTPException
from backend.database.firestore import db as DB
from backend.database.family_unit import add_current_xp
from backend.routes.collabrewards_routes import update_collab_progress

router = APIRouter(prefix="/verification", tags=["Task Verification"])

@router.post("/approve/")
async def approve_task(task_id: str = Form(...), feedback: str = Form("")):
    
    email, chore_id = task_id.split(":")

    ref = DB.collection("FAMILY UNIT").document(email).collection("CHORE").document(chore_id)
    chore_doc = ref.get()

    if not chore_doc.exists:
        raise HTTPException(status_code=404, detail="Chore not found")

    chore = chore_doc.to_dict()

    # Award XP
    xp = chore.get("XP Value", 0)
    child = chore.get("AssignedTo")
    task_type = chore.get("TaskType", "individual")
    
    if task_type == "individual":
        add_current_xp(email, child, xp)

    elif task_type == "family":
        await update_collab_progress(email=email, member_id=child, xp_earned=xp)

    else:
        print(f"Unknown task type '{task_type}', no XP awarded.")

    ref.update({
        "Completed": True,
        "Submitted": False,
        "Status": "Approved"
    })

    print(f"Approved chore {chore_id} for {child}. Awarded {xp} XP.")

    return {
        "message": f"Task approved! Awarded {xp} XP.",
        "task_id": task_id,
        "feedback": feedback,
        "status": "approved"
    }
    

@router.post("/reject/")
async def reject_task(task_id: str = Form(...), feedback: str = Form("")):
    email, chore_id = task_id.split(":")
    ref = DB.collection("FAMILY UNIT").document(email).collection("CHORE").document(chore_id)
    ref.update({
            "Completed": False,
            "Submitted": False,
            "Status": "redo"
        })

    print(f"Rejected chore {chore_id}")
    
    return {
        "message": "Task rejected.",
        "task_id": task_id,
        "feedback": feedback,
        "status": "redo"
    }

@router.get("/{email}/{chore_id}")
async def get_proof_image(email: str, chore_id: str):
    ref = DB.collection("FAMILY UNIT").document(email).collection("CHORE").document(chore_id)
    doc = ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Chore not found")
    
    data = doc.to_dict()
    return {
        "proof_image": data.get("ProofImageURL"),
        "title": data.get("Title"),
        "description": data.get("Description"),
        "assigned_to": data.get("AssignedTo"),
        "reward_points": data.get("XP Value"),
        "due_date": data.get("DueDate"),
    }