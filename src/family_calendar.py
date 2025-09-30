import calendar
import datetime
import pytz

import flet as ft

# Functionality to Implement:
    # Set Timezone 

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
    #calendar = calendar.TextCalendar()   
    
    def button_clicked(e):
        page.update()
    
    calendar = ft.Container (
        # Formatting (w/ design)...
        ft.Column (
            [
            ft.Row ( # MONTH/YEAR
                [
                    ft.IconButton (
                        ft.Icons.ARROW_CIRCLE_LEFT_OUTLINED, 
                        on_click=button_clicked,
                        icon_color="#59226b",
                        icon_size=36,
                        alignment=ft.alignment.center_left,
                        ),
                    ft.Text (
                        "July",
                        color="#000000",
                        size=28,
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
            ],
        ),
        height=500,
        width=450,
        alignment=ft.alignment.center,
        border_radius=35,
        padding=5,
        border=ft.border.all(2, "#59226b"),
        bgcolor="#ffffff",
        # Get Calendar dates
        # Days of the Week
        # Dates (loads current day w/ white tile) 
        # User clicks date = Selected date has white tile  
        # Prompt User to add event ('Add Event' button)
    )
    
    # Events Summary
    events_summary = ft.Container (
        # Static CLOCK icon w/ "Today's Schedule"
        # Events added by user
    )
    
    # Adding Page Contents
    content = ft.Column (
        [
            title,
            calendar,
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