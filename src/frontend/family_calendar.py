import calendar
from datetime import datetime
import requests

import flet as ft
import utils as u

# Functionality to Implement:
# -> ARROW Buttons: Change Month/Year
# -> ADD EVENT Button: Add a Task to User's Calendar
# -> DATE Tiles: Current = Blue, Clicked = White + Updates 'Today's Schedule'

def FamilyCalendar(page: ft.Page):
    page.title="Family Calendar"
    page.vertical_alignment="center"
    page.horizontal_alignment="center"
    page.padding=0
    page.spacing=0
    
    # Fonts
    page.fonts = {
        "LibreBaskerville": "/fonts/LibreBaskerville-Regular.ttf",
        "LibreBaskerville-Bold": "/fonts/LibreBaskerville-Bold.ttf",
    }
    
    # App Bar
    app_bar = u.application_bar(page)
    # Navigation bar
    nav_bar = u.navigation_bar(page)
    
    
    response = requests.get("http://127.0.0.1:8000/family_calendar/all")
    data = response.json()
    all_chores = data.get("chores", [])
    selected = ft.Text("Select a date to see chores.", size=14, color="#473c9c")
    
    # Title
    title = ft.Text (
        "Family Calendar",
        size=40,
        weight=ft.FontWeight.BOLD,
        color="indigo",
        text_align="center",
        font_family="LibreBaskerville",
    )
    
    # Calendar

    # -> Text formatting for text held in calendar
    def schedule_text_format(day):
        return ft.Text (
            value=day, 
            size=10, 
            color="#ffffff", 
            font_family="LibreBaskerville", 
            weight=ft.FontWeight.BOLD,
        )
    
    # -> Container formatting for days of the week
    def day_container_format(day_text):
        return ft.Container (
            content=day_text, 
            width=62, 
            height=50, 
            alignment=ft.alignment.center, 
            border=ft.border.all(1, "#000000"),
            bgcolor="#59226b",
        )
    
    # -> Container formatting for dates of the month
    def date_container_format(date):  
        def show_chores(e):
            if isinstance(date, ft.Text):
                return
            selected_date = f"{current_year}-{current_month:02d}-{int(date):02d}"
            chores_today = [c for c in all_chores if c["date"] == selected_date]
            
            if chores_today:
                task_list = "\n".join(f"• {c['title']} - {c['assignee']}" for c in chores_today)
                selected.value = f"Chores for {selected_date}:\n{task_list}"
            else:
                selected.value = f"No chores for {selected_date}"
            page.update()
        
        return ft.Container (
            content=ft.TextButton(content=ft.Text(str(date)), on_click=show_chores), 
            width=62, 
            height=50, 
            alignment=ft.alignment.center, 
            border=ft.border.all(1, "#000000"), 
            bgcolor="#b97ccb",
        )
    
    # -! BELONGS IN CONTROLLER
    cal = calendar.Calendar(6)
    currently = datetime.now()
    current_month = currently.month
    current_year = currently.year
    
    # -! BELONGS IN CONTROLLER
    # -> Iterate over a list of days in a month and encapsulate in a container
    def get_dates(year, month):
        dates = []
        for day in cal.itermonthdays(year, month):
            if day == 0: 
                dates.append(date_container_format(" "))
            else:
                dates.append(date_container_format(day))
        return dates
    
    # -> Days of the week
    weekdays = ft.Row (
        [
            day_container_format(schedule_text_format("Sun")),
            day_container_format(schedule_text_format("Mon")),
            day_container_format(schedule_text_format("Tue")),
            day_container_format(schedule_text_format("Wed")),
            day_container_format(schedule_text_format("Thu")),
            day_container_format(schedule_text_format("Fri")),
            day_container_format(schedule_text_format("Sat")),
        ],
        spacing=0,
        alignment=ft.MainAxisAlignment.CENTER,
    )
    
    # -> Weeks of the month
    week_dates = ft.Row (
        wrap=True,
        controls=get_dates(current_year, current_month),
        spacing=0,
        run_spacing=0,
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
    
    # -> Button action (future implementation)
    def button_clicked(yes):
        page.update()
    
    # -> Container prompting user for text inputs
    #add_event_container = ft.Container (
    #    content=ft.TextField(label="Event",),
    #    blur=10,
    #    height=300,
    #    width=300,
    #    alignment=ft.MainAxisAlignment.CENTER,
    #    visible=False,
    #)
        
    # -> Adding action to 'Add Event' button
    #def show_add_event(e):
    #    add_event_container.visible = not add_event_container.visible
    #    page.update()
        
    
    # -> Month's Schedule
    schedule = ft.Column (
        [
            weekdays,
            week_dates,    
        ],
        spacing=0,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    
    # Build Calendar
    family_calendar = ft.Container (
        ft.Column (
            [
            ft.Row ( # Month & Year
                [
                    ft.IconButton (
                        ft.Icons.ARROW_CIRCLE_LEFT_OUTLINED, 
                        on_click=button_clicked,
                        icon_color="#59226b",
                        icon_size=36,
                        alignment=ft.alignment.center_left,
                        ),
                    ft.Text (
                        "October 2025",
                        color="#000000",
                        size=28,
                        font_family="LibreBaskerville",
                        text_align="center",
                        weight=ft.FontWeight.BOLD,
                        ),
                    ft.IconButton (
                        ft.Icons.ARROW_CIRCLE_RIGHT_OUTLINED,
                        on_click=button_clicked,
                        icon_color="#59226b",
                        icon_size=36,
                        alignment=ft.alignment.center_right,
                    ),
                ],
                spacing=45,
                alignment=ft.MainAxisAlignment.CENTER,
            ),   
            schedule,
            ft.Row ( # 'Add Event' button
                [
                    ft.ElevatedButton (
                        content=ft.Text (
                            "Add Task", 
                            size=12, 
                            color="#ffffff", 
                            font_family="LibreBaskerville", 
                        ),
                        color="#ffffff",
                        bgcolor="#59226b",
                        #on_click=show_add_event,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
            ],
        ),
        height=450,
        width=450,
        alignment=ft.alignment.center,
        border_radius=35,
        padding=5,
        border=ft.border.all(2, "#59226b"),
        bgcolor="#ffffff", 
    )
    
    # Events Summary
    events_summary = ft.Container (
        content=ft.Column(
            [
                ft.Text (
                    "Today's Schedule...", 
                    color="#000000",
                    weight=ft.FontWeight.BOLD, 
                    font_family="LibreBaskerville", 
                    size=18,
                    text_align="center",
                ),
                selected,
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=10,
        ),
        alignment=ft.alignment.top_center,
        width=450,
        height=300,
        border_radius=35,
        padding=5,
        margin=3,
        border=ft.border.all(2, "#59226b"),
        bgcolor="#ffffff",
    )
    
    
    # Adding Page Contents
    content = ft.Column (
            [
                app_bar,
                ft.Column(
                    [
                        title,
                        family_calendar,
                        events_summary,
                    ],
                    alignment="center",
                    horizontal_alignment="center",
                    spacing=25,
                    expand=True,
                ),
                nav_bar,
            ],
        alignment="center",
        horizontal_alignment="center",
        spacing=25,
        expand=True,
    )
    
    return ft.Container (
        content=content,
        gradient=ft.LinearGradient (
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#cdffd8", "#94b9ff"],
        ),
        alignment=ft.alignment.center,
        expand=True,
    )

def main(page: ft.Page):
    page.add(FamilyCalendar(page))

if __name__== "__main__":
    ft.app(target=main, assets_dir="assets")