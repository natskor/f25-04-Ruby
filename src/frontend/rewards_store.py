import flet as ft
import utils as u
import requests

def StorePage(page: ft.Page):
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
    
    # App Bar
    app_bar = u.application_bar(page)
    # Navigation bar
    nav_bar = u.navigation_bar(page)
 
    email = page.session.get("email")
    profile = page.session.get("profile_name")
    
    def load_user_stats():
        try:
            xp_data = requests.get(
                f"http://127.0.0.1:8000/progress/xp/{profile}",
                params={"email": email}
            ).json()

            level_data = requests.get(
                f"http://127.0.0.1:8000/progress/level/{profile}",
                params={"email": email}
            ).json()

            return xp_data.get("spendable_xp", 0), xp_data.get("goal_xp", 1000), level_data.get("level", 1)
        except:
            return 0, 1000, 1

    user_spendable_xp, user_goal_xp, user_level = load_user_stats()
    
    def load_rewards():
        response = requests.get("http://127.0.0.1:8000/rewards_store/rewards", params={"email": email, "profile": profile})
        return response.json()
    
    rewards = load_rewards()
    
    if isinstance(rewards, list):
        rewards = [r for r in rewards if isinstance(r, dict)]
    else:
        rewards = []
    
    def claim_reward(reward_id):
        response = requests.post(f"http://127.0.0.1:8000/rewards_store/claim/{reward_id}", data={"email": email, "profile": profile})
        data = response.json()
        page.go("/themed_dashboard")

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
                    f"Level {user_level}",
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
                ft.Text(f"{user_spendable_xp}",
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
    
    # Create a reward button
    def create_reward(e):
        page.go("/create_reward")
        
    reward_cards = []

    for reward in rewards:
        img = reward.get("image")
        title_text = reward["title"]
        cost = reward["cost"]
        level_req = reward["level_unlock"]
        reward_id = reward["id"]

        enough_xp = user_spendable_xp >= cost
        meets_level = user_level >= level_req
        unlocked = enough_xp and meets_level

        card = ft.Row ([
                ft.Column ([
                    ft.Image (
                        src=img,
                        width=300,
                        height=175,
                        border_radius=8,
                        fit=ft.ImageFit.COVER,
                    ),
                    ft.Container (
                        ft.Text(
                            title_text, 
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
                alignment=ft.alignment.center, width=225, spacing=5,),
                ft.Column ([
                    ft.Text (
                        f"{cost} XP", 
                        size=25, 
                        color="#3aeb05" if unlocked else "#f72a2a", 
                        weight=ft.FontWeight.BOLD, 
                        text_align="center", 
                        font_family="LibreBaskerville",
                        style=ft.TextStyle (
                            shadow=ft.BoxShadow (
                                blur_radius=2.5, 
                                color="#000000", 
                                blur_style=ft.ShadowBlurStyle.SOLID,
                                ),
                            ),
                        ),
                    ft.ElevatedButton("Claim!", bgcolor="#00bf63" if unlocked else "#8f8e8e", color="#ffffff", width=200, disabled=not unlocked, on_click=lambda e, rid=reward_id: claim_reward(rid)),
                ], 
                alignment=ft.alignment.center, 
                width=225,
                ),
            ], 
            alignment=ft.alignment.center, 
            width=450,
        )
        reward_cards.append(card)
        reward_cards.append(ft.Divider(height=5, thickness=2, color="#59226b"))
        
    rewards_table = ft.Container(
        content=ft.Column(reward_cards, scroll="auto"),
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
    content = ft.Column(
        [
            app_bar,
            ft.Column(
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
                            on_click=create_reward,   # navigates on click
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
                opacity=.8,
        ),
        alignment=ft.alignment.center,
    )
    
def main(page: ft.Page):
    page.add(StorePage(page))

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")