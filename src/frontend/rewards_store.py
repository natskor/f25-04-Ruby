import flet as ft
import utils as u
import requests

# Functionality to Implement:
# -> Claim Button: Deducts Points from User's Spendable XP
# -> Scrollbar: View Longer List of Rewards

# Maybe:
# -? Parent is Notified when Award is Claimed
# -? Reward Image Upload
# -? Flesh out Logic More Clearly.

API_BASE = "http://127.0.0.1:8000"  # use http unless you're actually serving https


def StorePage(page: ft.Page):
    page.title = "Rewards Store"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.padding = 0
    page.spacing = 0

    # later this can come from login/session
    family_id = "demo-family"

    # Fonts to use
    page.fonts = {
        "LibreBaskerville": "/fonts/LibreBaskerville-Regular.ttf",
        "LibreBaskerville-Bold": "/fonts/LibreBaskerville-Bold.ttf",
    }

    # App Bar
    app_bar = u.application_bar(page)
    # Navigation bar
    nav_bar = u.navigation_bar(page)

    # ---------------- STATE ----------------
    current_xp = {"value": 0}

    # this Column will hold all the reward cards
    rewards_column = ft.Column(
        spacing=15,
        alignment="start",
        horizontal_alignment="center",
        scroll=ft.ScrollMode.AUTO,
    )

    # these Text controls will be updated when XP changes
    level_text = ft.Text(
        "Level 1",
        size=24,
        color="#eeca5c",
        text_align="center",
        font_family="LibreBaskerville",
    )

    xp_text = ft.Text(
        "0",
        color="#cccbff",
        size=20,
        text_align="center",
        font_family="LibreBaskerville",
    )

    # ---------------- HELPERS ----------------

    def compute_level(xp: int) -> int:
        # simple placeholder: 0–499 => 1, 500–999 => 2, etc.
        return max(1, xp // 500 + 1)

    def load_rewards_from_api():
        try:
            res = requests.get(f"{API_BASE}/families/{family_id}/rewards")
            res.raise_for_status()
            return res.json()
        except Exception as e:
            print("Error loading rewards:", e)
            page.snack_bar = ft.SnackBar(
                ft.Text("Error loading rewards."), open=True
            )
            page.update()
            return {"rewards": [], "current_xp": 0}

    def claim_reward(reward_id: str):
        try:
            res = requests.post(
                f"{API_BASE}/families/{family_id}/claim/{reward_id}"
            )
            if res.status_code != 200:
                detail = res.json().get("detail", "Could not claim reward.")
                page.snack_bar = ft.SnackBar(ft.Text(detail), open=True)
                page.update()
                return

            result = res.json()
            # expect {"message": "...", "remaining_xp": int}
            remaining = result.get("remaining_xp", current_xp["value"])
            current_xp["value"] = remaining
            xp_text.value = str(current_xp["value"])
            level_text.value = f"Level {compute_level(current_xp['value'])}"

            page.snack_bar = ft.SnackBar(
                ft.Text(result.get("message", "Reward claimed!")), open=True
            )
            page.update()
        except Exception as e:
            print("Error claiming reward:", e)
            page.snack_bar = ft.SnackBar(
                ft.Text("Error claiming reward."), open=True
            )
            page.update()

    def build_reward_card(reward: dict) -> ft.Control:
        # reward comes from backend Reward model
        reward_id = reward.get("id", "")
        name = reward.get("name", "Reward")
        cost = reward.get("cost", 0)
        image_url = reward.get("image_url") or "images/chest.png"

        can_afford = current_xp["value"] >= cost

        return ft.Container(
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Image(
                                src=image_url,
                                width=300,
                                height=175,
                                border_radius=8,
                                fit=ft.ImageFit.COVER,
                            ),
                            ft.Container(
                                ft.Text(
                                    name,
                                    size=15,
                                    color="#000000",
                                    weight=ft.FontWeight.BOLD,
                                    text_align="center",
                                    font_family="LibreBaskerville",
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
                        spacing=5,
                    ),
                    ft.Column(
                        [
                            ft.Text(
                                f"{cost} XP",
                                size=25,
                                color="#3aeb05" if can_afford else "#f72a2a",
                                weight=ft.FontWeight.BOLD,
                                text_align="center",
                                font_family="LibreBaskerville",
                                style=ft.TextStyle(
                                    shadow=ft.BoxShadow(
                                        blur_radius=2.5,
                                        color="#000000",
                                        blur_style=ft.ShadowBlurStyle.SOLID,
                                    ),
                                ),
                            ),
                            ft.ElevatedButton(
                                "Claim!",
                                bgcolor="#00bf63" if can_afford else "#8f8e8e",
                                color="#ffffff" if can_afford else "#535353",
                                width=200,
                                disabled=not can_afford,
                                on_click=(
                                    lambda e, rid=reward_id: claim_reward(rid)
                                    if can_afford
                                    else None
                                ),
                            ),
                        ],
                        alignment=ft.alignment.center,
                        width=225,
                    ),
                ],
                alignment=ft.alignment.center,
                width=450,
            ),
            padding=5,
        )

    def refresh_rewards():
        data = load_rewards_from_api()
        rewards = data.get("rewards", [])
        xp = data.get("current_xp", 0)

        current_xp["value"] = xp
        level_text.value = f"Level {compute_level(xp)}"
        xp_text.value = str(xp)

        rewards_column.controls = [build_reward_card(r) for r in rewards]
        page.update()

    # ---------------- UI COMPONENTS ----------------

    # Title at the top of the page
    title = ft.Text(
        "Rewards Store",
        size=40,
        weight=ft.FontWeight.BOLD,
        color="indigo",
        text_align="center",
        font_family="LibreBaskerville",
    )

    # User Summary
    user_summary = ft.Container(
        content=ft.Column(
            [
                level_text,
                ft.Text(
                    "Spendable XP:",
                    size=20,
                    color="#cccbff",
                    text_align="center",
                    font_family="LibreBaskerville",
                ),
                xp_text,
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
        gradient=ft.LinearGradient(
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=["#0571d3", "#f9b3ff"],
        ),
    )

    # Create a reward button
    def create_reward(e):
        page.go("/create_reward")

    # Rewards Table (dynamic)
    rewards_table = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Available Rewards:",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color="#ffffff",
                    text_align="center",
                    font_family="LibreBaskerville",
                ),
                rewards_column,  # dynamic list filled by refresh_rewards()
            ],
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.alignment.center,
            horizontal_alignment="center",
            spacing=10,
        ),
        height=475,
        width=500,
        alignment=ft.alignment.center,
        border_radius=10,
        border=ft.border.all(2, "#59226b"),
        gradient=ft.LinearGradient(
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=["#0571d3", "#f9b3ff"],
        ),
        padding=10,
    )

    # Reminder Message
    reminder = ft.Container(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            "Level Up to Unlock More Rewards!",
                            text_align="center",
                            size=25,
                            font_family="LibreBaskerville",
                            weight=ft.FontWeight.BOLD,
                            color="#ffffff",
                        ),
                    ],
                    alignment=ft.alignment.center,
                ),
            ],
        ),
        height=100,
        width=500,
        padding=30,
        alignment=ft.alignment.center,
        border_radius=10,
        border=ft.border.all(2, "#59226b"),
        gradient=ft.LinearGradient(
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=["#0571d3", "#f9b3ff"],
        ),
    )

    # Content for page
    content = ft.Column(
        [
            app_bar,
            ft.Column(
                [
                    title,
                    user_summary,
                    ft.Divider(
                        height=5,
                        thickness=2,
                        color="#59226b",
                        leading_indent=150,
                        trailing_indent=150,
                    ),
                    rewards_table,
                    ft.Container(
                        alignment=ft.alignment.center,
                        padding=10,
                        content=ft.Container(
                            content=ft.Text(
                                "+ Add Reward",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color="#ffffff",
                                font_family="LibreBaskerville",
                                text_align="center",
                            ),
                            width=200,
                            height=50,
                            alignment=ft.alignment.center,
                            bgcolor="#6562DF",
                            border_radius=10,
                            on_click=create_reward,  # navigates on click
                        ),
                    ),
                    reminder,
                ],
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

    # load rewards + XP once UI controls are created
    refresh_rewards()

    # Add the items to the page
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
            src="images/chest.png",
            fit=ft.ImageFit.FIT_WIDTH,
            alignment=ft.alignment.bottom_center,
            opacity=0.8,
        ),
        alignment=ft.alignment.center,
    )


def main(page: ft.Page):
    page.add(StorePage(page))


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
