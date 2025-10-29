import flet as ft
import utils as u

def genericDashboard(page: ft.Page):
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

    def go_chore_details(e: ft.ControlEvent):
        page.go("/details")
        page.update()

    def go_child_progress(e: ft.ControlEvent):
        page.go("/child_progress")
        page.update()
    
    def go_collab_reward(e: ft.ControlEvent):
        page.go("/collab_rewards")
        page.update()

    # App Bar
    app_bar = u.application_bar(page)
    # Navigation bar
    nav_bar = u.navigation_bar(page)

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
        on_click=go_child_progress, 
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
        on_click=go_chore_details, 
        padding=20,
        border_radius=20,
        shadow=ft.BoxShadow(blur_radius=10, color="#999999"),
        width=300,
        gradient=ft.LinearGradient(
            rotation=135,
            colors=["#94b9ff", "#cdffd8"],
        ),
    )

    # Collab Reward Progress Bar 
    collab_progress_card = ft.Container(
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
        on_click=go_collab_reward,
        padding=20,
        border_radius=20,
        shadow=ft.BoxShadow(blur_radius=10, color="#999999"),
        width=350,
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
                    progress_card,
                    ft.Text("~ Adventure Awaits ~",
                        font_family="LibreBaskerville", 
                        color="#ffffff"),
                    task_card,
                    ft.Text("~ Family Reward ~",
                    font_family="LibreBaskerville", 
                    color="#ffffff"),
                    collab_progress_card,
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
    page.add(genericDashboard(page))

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")