import flet as ft

def main(page: ft.Page):
    page.title = "Rewards Store"
    page.vertical_alignment="center"
    page.horizontal_alignment="center"
    page.padding=0
    page.spacing=0
    
    # Fonts to use
    page.fonts = {
        "LibreBaskerville": "/fonts/LibreBaskerville-Regular.ttf",
        "LibreBaskerville-Bold": "/fonts/LibreBaskerville-Bold.ttf",
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

    # Title at the top of the page
    title = ft.Text (
        "Rewards Store",
        size=40,
        weight=ft.FontWeight.BOLD,
        color="indigo",
        text_align="center",
        font_family="LibreBaskerville",
    )
    
    # User Summary
    user_summary = ft.Container (
        content=ft.Column(
            [
                ft.Text(
                    "Level 1",
                    size=24,
                    color="#eeca5c",
                    text_align="center",
                    font_family="LibreBaskerville",
                ),
                ft.Text(
                    "Spendable XP:",
                    size=20,
                    color="#cccbff",
                    text_align="center",
                    font_family="LibreBaskerville"),
                ft.Text("500",
                    color="#cccbff",
                    size=20,
                    text_align="center",
                    font_family="LibreBaskerville"),
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=5,
        ),
        height=125,
        width=300,
        alignment=ft.alignment.center,
        border_radius=10,
        border=ft.border.all(2, "#59226b"),
        gradient=ft.LinearGradient (
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=["#0571d3","#f9b3ff"],
        ),
    )
    
    # Rewards Table
    rewards_table = ft.Container (
        content=ft.Column ([
            ft.Row ([
                ft.Column ([
                    ft.Image (
                        src="images/icecream.webp",
                        width=300,
                        height=175,
                        border_radius=8,
                        fit=ft.ImageFit.COVER,
                    ),
                    ft.Container (
                        ft.Text(
                            "Ice Cream", 
                            size=15, 
                            color="#000000", 
                            weight=ft.FontWeight.BOLD, 
                            text_align="center",
                        ),
                        width=200, 
                        height=25, 
                        alignment=ft.alignment.center,
                        border_radius=10, 
                        border=ft.border.all(2, "#59226b"), 
                        bgcolor="#ffffff", 
                        margin=5,
                    ),  
                ], 
                alignment=ft.alignment.center, width=225, spacing=5,),
                ft.Column ([
                    ft.Text(
                        "100 XP", 
                        size=25, 
                        color="#3aeb05", 
                        weight=ft.FontWeight.BOLD, 
                        text_align="center", 
                        font_family="LibreBaskerville",
                    ),
                    ft.ElevatedButton("Claim!", bgcolor="#00bf63", color="#ffffff", width=200,),
                ], 
                alignment=ft.alignment.center, 
                width=225,
                ),
            ], 
            alignment=ft.alignment.center, 
            width=450,
            ),
            ft.Divider(
                height=5, 
                thickness=2, 
                color="#59226b",
                ),
            ft.Row ([
                ft.Column ([
                    ft.Image (
                        src="images/movietheater.jpg",
                        width=300,
                        height=175,
                        border_radius=8,
                        fit=ft.ImageFit.COVER,
                    ),
                    ft.Container (
                        ft.Text(
                            "Movie Night", 
                            size=15, 
                            color="#000000", 
                            weight=ft.FontWeight.BOLD, 
                            text_align="center",
                            ),
                        width=200, 
                        height=25, 
                        alignment=ft.alignment.center,
                        border_radius=10, 
                        border=ft.border.all(2, "#59226b"), 
                        bgcolor="#ffffff", 
                        margin=5,
                    ),
                ], 
                alignment=ft.alignment.center, 
                width=225, 
                spacing=5,),
                ft.Column([
                    ft.Text(
                        "500 XP", 
                        size=25, 
                        color="#df0000", 
                        weight=ft.FontWeight.BOLD, 
                        text_align="center", 
                        font_family="LibreBaskerville",),
                    ft.ElevatedButton(
                        "Claim!", 
                        bgcolor="#8f8e8e", 
                        color="#535353", 
                        width=200,),
                ], 
                alignment=ft.alignment.center, 
                width=225,),
            ], 
            alignment=ft.alignment.center, 
            width=450,),
        ]),
        height=475,
        width=500,
        alignment=ft.alignment.center,
        border_radius=10,
        border=ft.border.all(2, "#59226b"),
        gradient=ft.LinearGradient (
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=["#0571d3", "#f9b3ff"],
        ),
    )
    # Reminder Message
    reminder = ft.Container (
        ft.Column ([
            ft.Row (
            [
                ft.Text (
                    "Level Up to Unlock More Rewards!",
                    text_align="center",
                    size=25,
                    font_family="LibreBaskerville",
                    weight=ft.FontWeight.BOLD,
                    color="#ffffff",
                ),
            ],
            alignment=ft.alignment.center,
            ),],
        ),
        height=100,
        width=500,
        padding=30,
        alignment=ft.alignment.center,
        border_radius=10,
        border=ft.border.all(2, "#59226b"),
        gradient=ft.LinearGradient (
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=["#0571d3", "#f9b3ff"],),
    )
    
    # Content for page
    content = ft.Column (
        [
            title,
            user_summary,
            ft.Divider (
                height=5, 
                thickness=2, 
                color="#59226b", 
                leading_indent=150, 
                trailing_indent=150,
            ),
            rewards_table,
            reminder
        ],
        alignment="center",
        horizontal_alignment="center",
        spacing=25,
        expand=True,
    )
    
    # Add the items to the page
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