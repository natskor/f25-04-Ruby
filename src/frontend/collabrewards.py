import flet as ft
import utils as u
import requests

def CollabRewards(page: ft.Page):
    page.title = "Family Reward"
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
    
    # App Bar
    app_bar = u.application_bar(page)
    # Navigation bar
    nav_bar = u.navigation_bar(page)
    
    # Title
    title = ft.Text(
        "Family Reward",
        size=40,
        weight=ft.FontWeight.BOLD,
        color= "black",
        text_align="center",
        font_family="LibreBaskerville",
        )
    
    # Send GET request to backend
    collab_response = requests.get("http://127.0.0.1:8000/collabrewards/progress")
    
     # Converts it to JSON format
    collab_data = collab_response.json()
    
    current_xp = collab_data.get("current_xp", 0)
    goal_xp = collab_data.get("goal_xp", 1)
    
    # Calculate Progress
    collab_total = current_xp / goal_xp if goal_xp > 0 else 0
    
    # Do the same for individual progress
    member_id = "Kaleb"  # replace this with logged-in user from db
    user_response = requests.get(f"http://127.0.0.1:8000/progress/xp/{member_id}")
    user_data = user_response.json()
    user_current = user_data.get("current_xp", 0)
    user_goal = user_data.get("goal_xp", 1)
    user_total = user_current / user_goal if user_goal > 0 else 0
 
    
    progress_text = ft.Text(
        f"{current_xp} XP / {goal_xp} XP",
        size=14,
        color="#473c9c",
        font_family="LibreBaskerville",
    )

    # Reward container
    reward_card = ft.Container(
        content=ft.Column(
            [
                ft.Text("Trip to Busch Gardens\nWilliamsburg",
                        size=18, 
                        weight=ft.FontWeight.BOLD, 
                        text_align="center", 
                        font_family="LibreBaskerville"),
                ft.Text("Limited Time Reward Expires in:\n14 Days", 
                        text_align="center",
                        size=14, 
                        color="#473c9c", 
                        font_family="LibreBaskerville"),
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=5,
        ),
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=15,
        shadow=ft.BoxShadow(blur_radius=10, color="#999999"),
        width=350,
        gradient=ft.RadialGradient(
            center=ft.alignment.center,
            radius=1.5,
            colors=["#f6f6f6", "#d8d5d5"],
        ),
    )
    
    # Family Progress Ring
    family_progress = ft.Container(
        content=ft.Column(
            [
                ft.ProgressRing(
                        value=collab_total,
                        color="#8c52ff",
                        width=125,
                        height=125,
                        stroke_width=25,
                        bgcolor="#74a8ce"),            
                ft.Icon(ft.Icons.FAMILY_RESTROOM, 
                        color="#473c9c", 
                        size=60),
                ft.Text("Family Progress", 
                        size=18, 
                        weight=ft.FontWeight.BOLD, 
                        font_family="LibreBaskerville"),
                progress_text,
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=10,
        ),
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=20,
        shadow=ft.BoxShadow(blur_radius=10, color="#999999"),
        width=350,
        gradient=ft.RadialGradient(
            center=ft.alignment.center,
            radius=1.5,
            colors=["#f6f6f6", "#d8d5d5"],
        ),
    )

    # Individual Progress Bar for family reward contribution
    your_progress = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.STAR, color="#df961a", size=45),
                ft.Column(
                    [
                        ft.Container(
                            content=ft.ProgressBar(
                                value=user_total,
                                width=180,
                                bar_height=25,
                                height=30,
                                border_radius=ft.border_radius.all(10),
                                color="#473c9c",
                                bgcolor="#9d9d9d",
                            ),
                            height=25,
                            border_radius=15,
                            alignment=ft.alignment.center,   
                        ),
                        ft.Text(
                            "Your Progress",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            font_family="LibreBaskerville-Bold",
                            text_align="center",
                        ),
                        ft.Text(
                            f"{user_current} XP / {user_goal} XP",
                            size=14,
                            color="#473c9c",
                            font_family="LibreBaskerville",
                            text_align="center",
                        ),
                    ],
                    alignment="center",
                    horizontal_alignment="center",
                    spacing=5,
                ),
                ft.Icon(ft.Icons.STAR, color="#df961a", size=45),
            ],
            alignment="spaceBetween",
            vertical_alignment="center",
        ),
        padding=20,
        border_radius=20,
        shadow=ft.BoxShadow(blur_radius=10, color="#999999"),
        width=350,
        gradient=ft.RadialGradient(
            center=ft.alignment.center,
            radius=1.5,
            colors=["#f6f6f6", "#d8d5d5"],
        ),
    )

    content = ft.Column(
        [
            app_bar,
            ft.Column(
                [title, reward_card, family_progress, your_progress],
                alignment="center",
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
            colors=["#cdffd8", "#94b9ff"],
        ),
        alignment=ft.alignment.center,
    )
    
    
def main(page: ft.Page):
    page.add(CollabRewards(page))

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")