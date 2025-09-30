import calendar
import datetime
import pytz

import flet as ft

# Functionality to Implement:
# -> Set Timezone 
# -> Arrow Buttons: Change Month/Year
# -> Add Event Button: Add a Task to User's Calendar
# -> Clickable Dates: Show User's Tasks for Day
# -> Schedule Updates to Current Events

def main(page: ft.Page):
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
    
    # Menu Bar
    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.MENU, icon_color="#ffffff",),
        center_title=True,
        bgcolor="#404040",
        actions=[
            ft.IconButton(ft.Icons.NOTIFICATIONS_OUTLINED, icon_color="#ffffff",),
            ft.IconButton(ft.Icons.SETTINGS, icon_color="#ffffff"),
            ft.IconButton(ft.Icons.SEARCH, icon_color="#ffffff"),
        ],
    )
    
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
    def button_clicked(yes):
        page.update()
        
    cal = calendar.Calendar(6)
    
    # -> Get Month/Days data
    def get_dates(year, month):
        return cal.monthdays2calendar(year, month)
    
    dates = ft.Text(get_dates(2025, 9))

    # -> Construct Weekday Formatting
    def day_text_format(day):
        return ft.Text(value=day, size=10, color="#ffffff", font_family="LibreBaskerville", weight=ft.FontWeight.BOLD,)
    
    def day_container_format(day_text):
        return ft.Container(content=day_text, width=50, height=50, alignment=ft.alignment.center, border=ft.border.all(2, "#000000"), bgcolor="#59226b",)
    
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
                        "September 2025",
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
            ft.Row ([ # Days of the Week
                day_container_format(day_text_format("Sun")),
                day_container_format(day_text_format("Mon")),
                day_container_format(day_text_format("Tue")),
                day_container_format(day_text_format("Wed")),
                day_container_format(day_text_format("Thu")),
                day_container_format(day_text_format("Fri")),
                day_container_format(day_text_format("Sat")),
            ],
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER,
            ),  
            ft.Row ( # Scheduled Dates
                [
                    ft.Text("This is placeholder text.", color="#000000"),
                ],
                spacing=45,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row ( # Add Event button
                [
                    ft.ElevatedButton (
                        "Add Task",
                        on_click=button_clicked,
                        color="#ffffff",
                        bgcolor="#59226b",
                    ),
                ],
                spacing=45,
                alignment=ft.MainAxisAlignment.CENTER,
            )
            ],
        ),
        height=500,
        width=450,
        alignment=ft.alignment.center,
        border_radius=35,
        padding=5,
        border=ft.border.all(2, "#59226b"),
        bgcolor="#ffffff",
        # Load ALL current month date tiles
        # Dates (loads current day w/ fitted blue tile) 
        # User clicks date = Selected date has fitted white tile  
    )
    
    # Events Summary
    events_summary = ft.Container (
        ft.Text (
            "Today's Schedule...", 
            color="#000000",
            weight=ft.FontWeight.BOLD, 
            font_family="LibreBaskerville", 
            size=16,
            text_align="center",
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
            title,
            family_calendar,
            events_summary,
        ],
        alignment="center",
        horizontal_alignment="center",
        spacing=25,
        expand=True,
    )
    
    page.add (
        ft.Container (
            content=content,
            gradient=ft.LinearGradient (
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=["#cdffd8", "#94b9ff"],
            ),
            alignment=ft.alignment.center,
            expand=True,
        )
    )
    
ft.app(target=main, assets_dir="assets")