import calendar
from datetime import datetime
import pytz

import flet as ft

# Functionality to Implement:
# -> ARROW Buttons: Change Month/Year
# -> ADD EVENT Button: Add a Task to User's Calendar
# -> DATE Tiles: Current = Blue, Clicked = White + Updates 'Today's Schedule'

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
    
    def go_dashboard(e):
        page.go("/dashboard")

    def go_store(e):
        page.go("/store")

    def go_calendar(e):
        page.go("/calendar")
    
    def go_settings(e):
        page.go("/settings")

    def logout(e):
        page.go("/")

    def on_nav_change(e: ft.ControlEvent):
        selected_index = e.control.selected_index
        
        if selected_index == 0:
            go_dashboard(e)
        elif selected_index == 1:
            go_store(e)
        elif selected_index == 2:
            go_calendar(e)

    page.appbar = ft.AppBar(
        leading=ft.PopupMenuButton(
            icon=ft.Icons.MENU,
            icon_color="#ffffff",
            items=[
                ft.PopupMenuItem(text="Settings", icon=ft.Icons.SETTINGS, on_click=go_settings),
                ft.PopupMenuItem(),
                ft.PopupMenuItem(text="Log Out", icon=ft.Icons.LOGOUT, on_click=logout),
            ],
        ),
        center_title=True,
        bgcolor="#404040",
    )
    
    # Navigation bar
    page.navigation_bar = ft.NavigationBar(
        bgcolor="#C2B280",
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME_ROUNDED, label="Home"),
            ft.NavigationBarDestination(icon=ft.Icons.SHOPPING_BAG, label="Store"),
            ft.NavigationBarDestination(icon=ft.Icons.CALENDAR_MONTH_OUTLINED, label="Calendar"),
        ],
        on_change=on_nav_change,
    )
    page.navigation_bar.selected_index = -1
    
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
        return ft.Container (
            content=ft.TextButton(content=date), 
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
            if (day == 0): 
                dates.append(date_container_format(schedule_text_format(" ")))
            else:
                dates.append(date_container_format(schedule_text_format(day)))
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
        ft.Text (
            "Today's Schedule...", 
            color="#000000",
            weight=ft.FontWeight.BOLD, 
            font_family="LibreBaskerville", 
            size=18,
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