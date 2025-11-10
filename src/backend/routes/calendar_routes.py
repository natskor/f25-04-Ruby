from fastapi import APIRouter
from datetime import datetime
from backend.routes import chore_routes

router = APIRouter(prefix="/family_calendar", tags=["Family Calendar"])

# Replace later when Junsen makes his endpoints
# chores = [
#     {"title": "Clean Room", "assignee": "Alice", "date": "2025-10-29"},
#     {"title": "Take Out Trash", "assignee": "Kaleb", "date": "2025-10-29"},
#     {"title": "Mow Lawn", "assignee": "Dad", "date": "2025-10-30"},
#     {"title": "Do Dishes", "assignee": "Mom", "date": "2025-10-31"},
# ]
chores = []
    
@router.get("/all")
def get_all_chores():
    
    calendar_events = []
    
    for c in chore_routes.chore_list:
        calendar_events.append({
            "title": c.title,
            "assignee": c.assigned_to,
            "date": c.due_date,
            "completed": c.completed,
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
