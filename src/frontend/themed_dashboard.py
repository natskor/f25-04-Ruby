import flet as ft
import utils as u
import requests

def themedDashboard(page: ft.Page):
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
    
    # Collaborative Progress update
    collab_response = requests.get("http://127.0.0.1:8000/collabrewards/progress")
    collab_data = collab_response.json()

    collab_current = collab_data.get("current_xp", 0)
    collab_goal = collab_data.get("goal_xp", 1)
    collab_total = collab_current / collab_goal if collab_goal > 0 else 0

    # Do the same for individual progress
    member_id = "Kaleb"  # replace this with logged-in user from db
    user_response = requests.get(f"http://127.0.0.1:8000/progress/xp/{member_id}")
    user_data = user_response.json()
    user_current = user_data.get("current_xp", 0)
    user_goal = user_data.get("goal_xp", 1)
    user_total = user_current / user_goal if user_goal > 0 else 0

    # Individual Progress Bar 
    progress_card = ft.Container(
        image=ft.DecorationImage(
            src="images/airplane.png",
            fit=ft.ImageFit.CONTAIN,
            opacity=.7,
            alignment=ft.alignment.bottom_left,
        ),
        content=ft.Row(
            [
                ft.Column(
                    [
                        ft.Text(
                            f"{user_current} / {user_goal}",
                            size=14,
                            color="#473c9c",
                            font_family="LibreBaskerville",
                            text_align="center",
                            ),
                        ft.Container(
                            content=ft.ProgressBar(
                                value=user_total, #value 0.6
                                height=22,
                                width=200,
                                bar_height=40,
                                border_radius=ft.border_radius.all(20),
                                color="#eeca5c",
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
            vertical_alignment="center",
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
                            f"{collab_current} XP / {collab_goal} XP",
                            size=14,
                            color="#473c9c",
                            font_family="LibreBaskerville",
                            text_align="center",
                            ),
                        ft.Container(
                            content=ft.ProgressBar(
                                value=collab_total,
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


    # --------------temporary----------------------
        # Clickable chore that will lead to the verification page

    def go_verification(e: ft.ControlEvent):
        page.go("/verification")
        page.update()
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
        on_click=go_verification, 
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

     # --------------temporary----------------------


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
                    # temporary ----------------------------
                    ft.Text("~ Family Progress ~",
                            font_family="LibreBaskerville", 
                            color="#ffffff"),
                    child_progress_card,
                    # temporary ----------------------------
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
            image=ft.DecorationImage(
                src="images/boat.png",
                fit=ft.ImageFit.FIT_WIDTH,
                alignment=ft.alignment.bottom_center,
                opacity=.8,
            ),
            alignment=ft.alignment.center,
        )

def main(page: ft.Page):
    page.add(themedDashboard(page))

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")