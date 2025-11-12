from fastapi import APIRouter, Form

router = APIRouter(prefix="/verification", tags=["Task Verification"])

@router.post("/approve/")
async def approve_task(task_id: str = Form(...), feedback: str = Form("")):
    
    print(f"Approved: {task_id}, feedback = {feedback}")
    return {
        "message": "Task approved!",
        "task_id": task_id,
        "feedback": feedback,
        "status": "approved"
    }

@router.post("/reject/")
async def reject_task(task_id: str = Form(...), feedback: str = Form("")):
    
    print(f"Rejected: {task_id}, feedback = {feedback}")
    return {
        "message": "Task rejected.",
        "task_id": task_id,
        "feedback": feedback,
        "status": "rejected"
    }
