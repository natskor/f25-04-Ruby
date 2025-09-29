import datetime
import flet as ft

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
    calendar = ft.Container (
        # Formatting (no design)
            # Set Timezone
            # Get Calendar dates
            # Move to 'Formatting (w/ design)'
            
        # Formatting (w/ design)...
            # Current Month & Year, w/ clickable navigation arrows
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