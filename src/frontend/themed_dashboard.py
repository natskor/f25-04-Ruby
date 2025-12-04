import flet as ft
import utils as u
import requests  # <-- needed for API calls

# Define the backend API address
API_BASE_URL = "http://127.0.0.1:8000"


def themedDashboard(page: ft.Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.theme_mode = "light"

    # Remove extra padding/spacing so gradient fills the screen
    page.padding = 0
    page.spacing = 0

    # Pull current user info from session
    email = page.session.get("email")
    # Avatar selection page stores "profile" and "avatar"
    profile_name = page.session.get("profile") or "Adventurer"
    avatar_path = page.session.get("avatar") or "images/dragon.png"

    page.fonts = {
        "LibreBaskerville": "/fonts/LibreBaskerville-Regular.ttf",
        "LibreBaskerville-Bold": "/fonts/LibreBaskerville-Bold.ttf",
        "LibreBaskerville-Italic": "/fonts/LibreBaskerville-Italic.ttf",
    }

    # ---------- ROUTE HANDLERS ----------

    def go_chore_details(chore_id: str):
        page.session.set("selected_chore_id", chore_id)
        page.go("/details")
        page.update()

    def go_child_progress(e: ft.ControlEvent):
        page.go("/child_progress")
        page.update()

    def go_collab_reward(e: ft.ControlEvent):
        page.go("/collab_rewards")
        page.update()

    # ---------- TASK LIST / QUESTS ----------

    def create_task_card(chore_data: dict) -> ft.Control:
        """Generate UI cards based on the JSON data returned by the API."""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(
                                chore_data.get("title", "Unknown Task"),
                                size=14,
                                color="#473c9c",
                                font_family="LibreBaskerville",
                                text_align="left",
                            ),
                            ft.Text(
                                f"Due: {chore_data.get('due_date', 'No Date')}",
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
                                                f"+{chore_data.get('reward_points', 0)}",
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
                                                f"+{chore_data.get('reward_points', 0)}",
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
                        spacing=5,
                    ),
                ],
                alignment="spaceBetween",
                vertical_alignment="center",
            ),
            on_click=lambda e, cid=chore_data["id"]: go_chore_details(cid),
            padding=20,
            border_radius=20,
            shadow=ft.BoxShadow(blur_radius=10, color="#999999"),
            width=300,
            gradient=ft.LinearGradient(
                rotation=135,
                colors=["#94b9ff", "#cdffd8"],
            ),
        )

    # Task list container (initially empty, filled by load_data())
    task_list_col = ft.Column(spacing=15, horizontal_alignment="center")

    def load_data():
        task_list_col.controls.clear()

        if not email or not profile_name:
            task_list_col.controls.append(
                ft.Text(
                    "No user session found. Please log in again.",
                    color="red",
                    font_family="LibreBaskerville",
                )
            )
            page.update()
            return

        try:
            # Retrieve chores for this logged-in profile
            res = requests.get(
                f"{API_BASE_URL}/chores/",
                params={"email": email, "user": profile_name},
            )
            if res.status_code == 200:
                chores = res.json()
                if not chores:
                    task_list_col.controls.append(
                        ft.Text(
                            "No active quests! Chill time 😎",
                            color="white",
                            font_family="LibreBaskerville",
                        )
                    )
                else:
                    for chore in chores:
                        if not chore.get("completed", False):
                            task_list_col.controls.append(create_task_card(chore))
            else:
                print("Failed to fetch chores:", res.text)
                task_list_col.controls.append(
                    ft.Text("Could not load quests.", color="red")
                )
        except Exception as ex:
            print(f"Error loading data: {ex}")
            task_list_col.controls.append(
                ft.Text("Connection Error", color="red")
            )

        page.update()

    # ---------- APP & NAV BARS ----------

    app_bar = u.application_bar(page)
    nav_bar = u.navigation_bar(page)

    # ---------- PROGRESS BARS (REAL DATA) ----------

    try:
        # Collaborative family reward progress
        collab_response = requests.get(f"{API_BASE_URL}/collabrewards/progress")
        collab_data = collab_response.json()
        # Adjust keys to match your backend (these are placeholders)
        collab_current = collab_data.get("current_xp", collab_data.get("Current XP", 0))
        collab_goal = collab_data.get("goal_xp", collab_data.get("XP Goal", 1))
        collab_total = collab_current / collab_goal if collab_goal > 0 else 0

        # Individual user progress
        member_id = profile_name  # use the current profile as member id
        user_response = requests.get(
            f"{API_BASE_URL}/progress/xp/{member_id}"
        )
        user_data = user_response.json()
        user_current = user_data.get("current_xp", 0)
        user_goal = user_data.get("goal_xp", 1)
        user_total = user_current / user_goal if user_goal > 0 else 0
    except Exception as ex:
        print("Error fetching progress:", ex)
        collab_current, collab_goal, collab_total = 0, 100, 0
        user_current, user_goal, user_total = 0, 100, 0

    # Individual Progress Card (now uses real data)
    progress_card = ft.Container(
        image=ft.DecorationImage(
            src="images/airplane.png",
            fit=ft.ImageFit.CONTAIN,
            opacity=0.7,
            alignment=ft.alignment.bottom_left,
        ),
        content=ft.Row(
            [
                ft.Column(
                    [
                        ft.Text(
                            f"{user_current} XP / {user_goal} XP",
                            size=14,
                            color="#473c9c",
                            font_family="LibreBaskerville",
                            text_align="center",
                        ),
                        ft.Container(
                            content=ft.ProgressBar(
                                value=user_total,
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

    # Collaborative Reward Progress Card (also uses real data)
    collab_progress_card = ft.Container(
        content=ft.Row(
            [
                ft.Column(
                    [
                        ft.Icon(
                            ft.Icons.FAMILY_RESTROOM,
                            color="#473c9c",
                            size=60,
                            opacity=0.8,
                        ),
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

    # ---------- TEMPORARY VERIFICATION SECTION (KEPT, BUT USING USER NAME) ----------

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
                    spacing=5,
                ),
            ],
            alignment="spaceBetween",
            vertical_alignment="center",
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

    # Child Info now uses actual profile name + avatar
    child_info = ft.Container(
        content=ft.Row(
            [
                ft.Column(
                    [
                        ft.Text(
                            profile_name,
                            size=14,
                            color="#473c9c",
                            font_family="LibreBaskerville",
                            text_align="left",
                        ),
                        ft.Row(
                            [
                                ft.Text(
                                    "Progress",
                                    size=14,
                                    color="#8f8e8e",
                                    font_family="LibreBaskerville",
                                    text_align="left",
                                ),
                            ]
                        ),
                    ],
                    spacing=2,
                ),
                ft.Row(
                    [
                        ft.Image(
                            src=avatar_path,
                            width=100,
                            height=100,
                        ),
                    ],
                    spacing=5,
                    vertical_alignment="center",
                ),
            ],
            alignment="spaceBetween",
            vertical_alignment="center",
        ),
        on_click=toggle,
        padding=0,
    )

    child_progress_card = ft.Container(
        padding=20,
        border_radius=20,
        shadow=ft.BoxShadow(blur_radius=10, color="#999999"),
        width=300,
        gradient=ft.LinearGradient(
            rotation=135,
            colors=["#94b9ff", "#cdffd8"],
        ),
        content=ft.Column([child_info, child_chore], spacing=5),
    )

    # ---------- PAGE LAYOUT ----------

    content = ft.Column(
        [
            app_bar,
            ft.Column(
                [
                    progress_card,
                    ft.Text(
                        "~ Adventure Awaits ~",
                        font_family="LibreBaskerville",
                        color="#ffffff",
                    ),
                    task_list_col,
                    ft.Text(
                        "~ Family Reward ~",
                        font_family="LibreBaskerville",
                        color="#ffffff",
                    ),
                    collab_progress_card,
                    ft.Text(
                        "~ Family Progress ~",
                        font_family="LibreBaskerville",
                        color="#ffffff",
                    ),
                    child_progress_card,
                    ft.Text(
                        "~ Verification ~",
                        font_family="LibreBaskerville",
                        color="#ffffff",
                    ),
                ],
                horizontal_alignment="center",
                spacing=25,
                expand=True,
                scroll=ft.ScrollMode.AUTO,
            ),
            nav_bar,
        ],
        alignment="spaceBetween",
        horizontal_alignment="center",
        expand=True,
    )

    # Load quests for this user
    load_data()

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
            opacity=0.8,
        ),
        alignment=ft.alignment.center,
    )


def main(page: ft.Page):
    page.add(themedDashboard(page))


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
