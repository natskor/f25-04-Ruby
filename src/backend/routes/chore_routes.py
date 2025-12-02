from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from backend.database import chore as chore_db
from backend.routes import calendar_routes, collabrewards_routes

router = APIRouter(
    prefix="/chores",
    tags=["Chores"]
)

# Models
class ChoreCreate(BaseModel):
    email: str
    title: str
    description: Optional[str] = None
    assigned_to: str
    due_date: Optional[str] = None
    task_type: Optional[str] = None
    reward_points: int = 0

class ChoreResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    assigned_to: str
    due_date: Optional[str]
    completed: bool
    reward_points: int
    task_type: Optional[str]

# Endpoints

@router.post("/", response_model=ChoreResponse)
def create_chore(chore: ChoreCreate):
    """Create a new chore in Firestore and add to calendar."""
    try:
        # 1. Save to Database
        new_chore_data = chore_db.create_chore(
            email=chore.email,
            title=chore.title,
            desc=chore.description,
            xp_val=chore.reward_points,
            assigned_to=chore.assigned_to,
            due_date=chore.due_date,
            task_type=chore.task_type
        )

        # 2. Integration with Calendar
        try:
            calendar_routes.add_event_to_calendar(
                user=chore.assigned_to,
                title=chore.title,
                date=chore.due_date,
                description=chore.description
            )
        except Exception as e:
            print(f"Warning: Could not add event to calendar: {e}")

        # Map DB keys to Pydantic model keys
        return ChoreResponse(
            id=new_chore_data["id"],
            title=new_chore_data["Title"],
            description=new_chore_data["Description"],
            assigned_to=new_chore_data["AssignedTo"],
            due_date=new_chore_data["DueDate"],
            completed=new_chore_data["Completed"],
            reward_points=new_chore_data["XP Value"],
            task_type=new_chore_data["TaskType"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[ChoreResponse])
def get_all_chores(email: str, user: Optional[str] = None):
    """Get all chores, optionally filtered by assigned user."""
    try:
        if user:
            raw_chores = chore_db.get_chores_by_user(email, user)
        else:
            raw_chores = chore_db.get_all_chores(email)
            
        # Transform DB format to Response format
        return [
            ChoreResponse(
                id=c["id"],
                title=c["Title"],
                description=c.get("Description"),
                assigned_to=c["AssignedTo"],
                due_date=c.get("DueDate"),
                completed=c.get("Completed", False),
                reward_points=c.get("XP Value", 0),
                task_type=c.get("TaskType")
            )
            for c in raw_chores
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{chore_id}", response_model=ChoreResponse)
def get_chore_details(chore_id: str, email: str):
    """Get details of a specific chore."""
    try:
        chore = chore_db.get_chore_by_id(email, chore_id)
        if not chore:
            raise HTTPException(status_code=404, detail="Chore not found")
        
        return ChoreResponse(
            id=chore["id"],
            title=chore["Title"],
            description=chore.get("Description"),
            assigned_to=chore["AssignedTo"],
            due_date=chore.get("DueDate"),
            completed=chore.get("Completed", False),
            reward_points=chore.get("XP Value", 0),
            task_type=chore.get("TaskType")
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{chore_id}/complete")
def complete_chore(chore_id: str, email: str):
    """Mark chore complete and award the ACTUAL reward points."""
    try:
        # 1. Get current chore status to check if already done
        chore = chore_db.get_chore_by_id(email, chore_id)
        if not chore:
            raise HTTPException(status_code=404, detail="Chore not found")
        
        if chore.get("Completed"):
            raise HTTPException(status_code=400, detail="Chore already completed.")

        # 2. Update status in DB
        updated_chore = chore_db.complete_chore(email, chore_id)
        
        # 3. Award Points (FIXED: Uses actual XP value from chore)
        points_to_award = chore.get("XP Value", 0)
        
        try:
            collabrewards_routes.award_points(chore["AssignedTo"], points=points_to_award)
        except Exception as e:
            print(f"Warning: Could not award points: {e}")

        return {"message": f"Chore '{chore['Title']}' marked complete! Awarded {points_to_award} points."}

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{chore_id}")
def delete_chore(chore_id: str, email: str):
    try:
        chore_db.remove_chore(email, chore_id)
        return {"message": f"Chore {chore_id} deleted."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))