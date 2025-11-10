from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from backend.routes import calendar_routes, collabrewards_routes

router = APIRouter(
    prefix="/chores",
    tags=["Chores"]
)

# Models
class Chore(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    assigned_to: str  # username
    due_date: Optional[str] = None
    completed: bool = False
    created_at: datetime = datetime.now()
    task_type: Optional[str] = None
    reward_points: Optional[int] = 0

class ChoreCreate(BaseModel):
    title: str
    description: Optional[str] = None
    assigned_to: str
    due_date: Optional[str] = None
    task_type: Optional[str] = None
    reward_points: Optional[int] = 0

#In-memory store
chore_list = []
chore_id_counter = 1


#Endpoints
@router.post("/", response_model=Chore)
def create_chore(chore: ChoreCreate):
    """Create a new chore and add it to the user's calendar."""
    global chore_id_counter

    new_chore = Chore(
        id=chore_id_counter,
        title=chore.title,
        description=chore.description,
        assigned_to=chore.assigned_to,
        due_date=chore.due_date,
        completed=False,
        task_type=chore.task_type,
        reward_points=chore.reward_points,
    )
    
    chore_id_counter += 1
    chore_list.append(new_chore)

    #Integration with Calendar
    try:
        calendar_routes.add_event_to_calendar(
            user=chore.assigned_to,
            title=chore.title,
            date=chore.due_date,
            description=chore.description
        )
    except Exception as e:
        print(f"Warning: Could not add event to calendar: {e}")

    return new_chore


@router.get("/", response_model=List[Chore])
def get_all_chores():
    return chore_list


@router.get("/{chore_id}", response_model=Chore)
def get_chore(chore_id: int):
    for c in chore_list:
        if c.id == chore_id:
            return c
    raise HTTPException(status_code=404, detail="Chore not found")


@router.post("/{chore_id}/complete")
def complete_chore(chore_id: int):
    """Mark chore complete and award rewards."""
    for c in chore_list:
        if c.id == chore_id:
            if c.completed:
                raise HTTPException(status_code=400, detail="Chore already completed.")
            c.completed = True

            # ✅ Integration with CollabRewards or Rewards Store
            try:
                collabrewards_routes.award_points(c.assigned_to, points=10)
            except Exception as e:
                print(f"Warning: Could not award points: {e}")

            return {"message": f"Chore '{c.title}' marked complete for {c.assigned_to}!"}

    raise HTTPException(status_code=404, detail="Chore not found")


@router.delete("/{chore_id}")
def delete_chore(chore_id: int):
    global chore_list
    chore_list = [c for c in chore_list if c.id != chore_id]
    return {"message": f"Chore {chore_id} deleted."}
