import flet as ft

def parentDashboard(page: ft.Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.theme_mode = "light"
    
    # To remove the white space border around the gradient background
    page.padding=0
    page.spacing=0
    
    page.fonts = {
        "LibreBaskerville": "/fonts/LibreBaskerville-Regular.ttf",
        "LibreBaskerville-Bold": "/fonts/LibreBaskerville-Bold.ttf",
        "LibreBaskerville-Italic": "/fonts/LibreBaskerville-Italic.ttf",
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

    # App Bar
    app_bar = ft.Container(
        bgcolor="#404040",
        padding=ft.padding.symmetric(horizontal=15, vertical=10),
        content=ft.Row(
            [
                ft.PopupMenuButton(
                    icon=ft.Icons.MENU,
                    icon_color="#ffffff",
                    items=[
                        ft.PopupMenuItem(text="Settings", icon=ft.Icons.SETTINGS, on_click=go_settings),
                        ft.PopupMenuItem(),
                        ft.PopupMenuItem(text="Log Out", icon=ft.Icons.LOGOUT, on_click=logout),
                    ],
                ),
            ],
            alignment="spaceBetween",
            vertical_alignment="center",
        ),
    )
    
    # Navigation bar
    nav_bar = ft.Container(
        content=ft.NavigationBar(
            bgcolor="#C2B280",
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME_ROUNDED, label="Home"),
                ft.NavigationBarDestination(icon=ft.Icons.SHOPPING_BAG, label="Store"),
                ft.NavigationBarDestination(icon=ft.Icons.CALENDAR_MONTH_OUTLINED, label="Calendar"),
            ],
            on_change=on_nav_change,
        ),
        expand=False,
    )
    nav_bar.selected_index = -1


    # Collab Reward Progress Bar 
    progress_card = ft.Container(
        content=ft.Row(
            [
                ft.Column(
                    [
                        ft.Icon(ft.Icons.FAMILY_RESTROOM, 
                            color="#473c9c", 
                            size=60,
                            opacity=.8,),
                        ft.Text(
                            "3000 XP / 5000 XP",
                            size=14,
                            color="#473c9c",
                            font_family="LibreBaskerville",
                            text_align="center",
                            ),
                        ft.Container(
                            content=ft.ProgressBar(
                                value=0.6,
                                height=22,
                                width=200,
                                bar_height=40,
                                border_radius=ft.border_radius.all(20),
                                color="#8c52ff",
                                bgcolor="#ffffff",
                            ),
                            height=50,
                            alignment=ft.alignment.center,   
                        ),
                    ],
                    alignment="center",
                    horizontal_alignment="center",
                    spacing=5,
                ),
            ],
            alignment="center",
            vertical_alignment="center",
        ),
        #placeholder for on_click for specific specifc child progress
        on_click=lambda e: page.go("/child_progress"), 
        padding=20,
        border_radius=20,
        shadow=ft.BoxShadow(blur_radius=10, color="#999999"),
        width=350,
        gradient=ft.LinearGradient(
            rotation=135,
            colors=["#94b9ff", "#cdffd8"],
        ),
    )
    
    # Clickable chore that will lead to the verification page
    child_chore = ft.Container(
        content=ft.Row(
            [
                ft.Column(
                    [
                        ft.Text(
                            "Wash Dishes",
                            size=12,
                            color="#473c9c",
                            font_family="LibreBaskerville",
                            text_align="left",
                            ),
                    ],
                    alignment="center",
                    horizontal_alignment="left",
                    spacing=5,
                ),
                ft.Column(
                    [
                        ft.Stack(
                            [
                                ft.Text(
                                    spans=[
                                        ft.TextSpan(
                                            "View",
                                            ft.TextStyle(
                                                size=12,
                                                weight=ft.FontWeight.BOLD,
                                                font_family="LibreBaskerville",
                                                foreground=ft.Paint(
                                                    color="#ffffff",
                                                    stroke_width=6,
                                                    style=ft.PaintingStyle.STROKE,
                                                ),
                                            ),
                                        ),
                                    ],
                                ),
                                ft.Text(
                                    spans=[
                                        ft.TextSpan(
                                            "View",
                                            ft.TextStyle(
                                                size=12,
                                                weight=ft.FontWeight.BOLD,
                                                color="#b8b8b8",
                                                font_family="LibreBaskerville",
                                            ),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                    alignment="center",
                    horizontal_alignment="end",
                    spacing=5
                ),
            ],
            alignment="spaceBetween",
            vertical_alignment="center"
        ),

        #placeholder for on_click for specific verification
        on_click=lambda e: page.go("/verification"), 
        padding=10,
        border_radius=20,
        shadow=ft.BoxShadow(blur_radius=10, color="#999999"),
        width=300,
        gradient=ft.LinearGradient(
            rotation=135,
            colors=["#94b9ff", "#cdffd8"],
        ),
        visible=False,
        opacity=0,
    )

    def toggle(_):
        expanded = not child_chore.visible
        child_chore.visible = expanded
        child_chore.opacity = 1.0 if expanded else 0.0
        child_chore.update()


    # Child's Info
    child_info = ft.Container(
        content=ft.Row(
            [
                ft.Column(
                    [
                        ft.Text(
                            "Kaleb",
                            size=14,
                            color="#473c9c",
                            font_family="LibreBaskerville",
                            text_align="left",
                            ),
                            ft.Row([
                                    ft.Text(
                                    "Progress",
                                    size=14,
                                    color="#8f8e8e",
                                    font_family="LibreBaskerville",
                                    text_align="left",
                                ),
                            ])
                    ],
                    spacing=2,
                ),
                ft.Row(
                    [
                    ft.Image(
                        src="images/dragon.png",
                        width=100,
                        height=100,
                        ),
                    ],
                    spacing=5,
                    vertical_alignment="center"
                )
            ],
            alignment="spaceBetween",
            vertical_alignment="center",
        ),
        on_click=toggle,
        padding=0,
    )

    # View of Child Info and chores
    child_progress_card=ft.Container(
        padding=20,
        border_radius=20,
        shadow=ft.BoxShadow(blur_radius=10, color="#999999"),
        width=300,
        gradient=ft.LinearGradient(
            rotation=135,
            colors=["#94b9ff", "#cdffd8"],
        ),
        content=ft.Column([child_info, child_chore], spacing=5)
    )

    # Assigned Tasks 
    task_card = ft.Container(
        content=ft.Row(
            [
                ft.Column(
                    [
                        ft.Text(
                            "Wash Dishes",
                            size=14,
                            color="#473c9c",
                            font_family="LibreBaskerville",
                            text_align="left",
                            ),
                        ft.Text(
                            "Due June 15 at 5:00pm",
                            size=10,
                            color="#404040",
                            font_family="LibreBaskerville",
                            text_align="left",
                            ),
                    ],
                    alignment="center",
                    horizontal_alignment="left",
                    spacing=5,
                ),
                ft.Column(
                    [
                        ft.Stack(
                            [
                                ft.Text(
                                    spans=[
                                        ft.TextSpan(
                                            "+50",
                                            ft.TextStyle(
                                                size=20,
                                                weight=ft.FontWeight.BOLD,
                                                font_family="LibreBaskerville",
                                                foreground=ft.Paint(
                                                    color="#ffffff",
                                                    stroke_width=6,
                                                    style=ft.PaintingStyle.STROKE,
                                                ),
                                            ),
                                        ),
                                    ],
                                ),
                                ft.Text(
                                    spans=[
                                        ft.TextSpan(
                                            "+50",
                                            ft.TextStyle(
                                                size=20,
                                                weight=ft.FontWeight.BOLD,
                                                color="#7ed957",
                                                font_family="LibreBaskerville",
                                            ),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                    alignment="center",
                    horizontal_alignment="right",
                    spacing=5
                ),
            ],
            alignment="spaceBetween",
            vertical_alignment="center"
        ),
        #placeholder for on_click for specific task description
        on_click=lambda e: page.go("/task_description"), 
        padding=20,
        border_radius=20,
        shadow=ft.BoxShadow(blur_radius=10, color="#999999"),
        width=300,
        gradient=ft.LinearGradient(
            rotation=135,
            colors=["#94b9ff", "#cdffd8"],
        ),
    )


    content = ft.Column(
        [
            app_bar,
            ft.Column(
                [
                    ft.Text("~ Family Reward ~",
                    font_family="LibreBaskerville", 
                    color="#ffffff"),
                    progress_card,
                    ft.Text("~ Family Progress ~",
                            font_family="LibreBaskerville", 
                            color="#ffffff"),
                    child_progress_card,
                    ft.Text("~ Adventure Awaits ~",
                            font_family="LibreBaskerville", 
                            color="#ffffff"),
                    task_card,
                ],
                horizontal_alignment="center",
                spacing=25,
                expand=True,
            ),
           nav_bar, 
        ],
        alignment="spaceBetween",
        horizontal_alignment="center",
        expand=True,
    )

    return ft.Container(
            content=content,
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                rotation=45,
                colors=["#ffd27f", "#4ca2b5", "#003f82", "#000b21"],
            ),
            alignment=ft.alignment.center,
        )

def main(page: ft.Page):
    page.add(parentDashboard(page))

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")