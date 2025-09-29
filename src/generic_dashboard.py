import flet as ft

def main(page: ft.Page):
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

    # Menu bar with icons
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

    # Navigation bar
    page.navigation_bar = ft.NavigationBar(
        bgcolor="#d1d1d1",
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.SHOPPING_BAG, label="Store"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON, label="Profile"),
            ft.NavigationBarDestination(icon=ft.Icons.CALENDAR_MONTH_OUTLINED, label="Calendar"),
        ]
    )

    # Individual Progress Bar 
    progress_card = ft.Container(
        content=ft.Row(
            [
                ft.Column(
                    [
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
                                color="#7ed957",
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
        padding=20,
        border_radius=20,
        shadow=ft.BoxShadow(blur_radius=10, color="#999999"),
        width=350,
        gradient=ft.LinearGradient(
            rotation=135,
            colors=["#94b9ff", "#cdffd8"],
        ),
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
            progress_card,
            ft.Text("~ Adventure Awaits ~",
                    font_family="LibreBaskerville", 
                    color="#ffffff"),
            task_card,
        ],
        horizontal_alignment="center",
        spacing=25,
        expand=True,
    )

    page.add(
        ft.Container(
            padding=25,
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
    )

ft.app(target=main, assets_dir="assets")