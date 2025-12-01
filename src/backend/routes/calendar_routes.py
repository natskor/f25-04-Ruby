from fastapi import APIRouter
from datetime import datetime
from backend.database.chore import get_all_chores as db_get_all_chores

router = APIRouter(prefix="/family_calendar", tags=["Family Calendar"])
chores = []
    
@router.get("/all")
def get_all_chores():
    
    chores = db_get_all_chores()
    
    calendar_events = []
    
    for c in chores:
        calendar_events.append({
            "title": c.get("Title"),
            "assignee": c.get("AssignedTo"),
            "date": c.get("DueDate"),
            "completed": c.get("Completed"),
        })
    
    return {
        "chores": calendar_events
    }

# Helper function for chore integration(added by JS)   
def add_event_to_calendar(user: str, title: str, date: str, description: str = ""):
    """Helper function for chore integration."""
    chores.append({
        "title": title,
        "assignee": user,
        "date": date,
        "description": description,
    })
    
    # Simulate adding a calendar event for a user
    print(f"Added calendar event for {user}: {title} on {date}")
