import flet as ft
import requests

BACKEND_URL = "http://127.0.0.1:8000"

def ProfileSelection(page: ft.Page):
    page.title = "QuestNest – Family Profiles"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.padding = 0
    page.spacing = 0
    
    page.fonts = {
        "LibreBaskerville": "/fonts/LibreBaskerville-Regular.ttf",
        "LibreBaskerville-Bold": "/fonts/LibreBaskerville-Bold.ttf",
        "LibreBaskerville-Italic": "/fonts/LibreBaskerville-Italic.ttf",
    }
    
    try:
        resp = requests.get(f"{BACKEND_URL}/avatar/list", timeout=5)
        if resp.status_code == 200:
            PROFILES = resp.json()
        else:
            PROFILES = []
    except Exception:
        PROFILES = []

    # hardcoded fallback if request fails
    if not PROFILES:
        PROFILES = [
            {"name": "Mom", "avatar_id": "images/avatars/mermaid.png"},
            {"name": "Dad", "avatar_id": "images/avatars/wizard.png"},
            {"name": "Alice", "avatar_id": "images/avatars/unicorn.png"},
            {"name": "Bob", "avatar_id": "images/avatars/dragon.png"},
        ]

    selected_idx = {"value": None}

    def make_profile_tile(profile: dict, idx: int) -> ft.Container:
        is_selected = selected_idx["value"] == idx
        border_color = "#6B8AF6" if is_selected else "#DADDE6"

        img = ft.Container(
            width=90,
            height=90,
            border_radius=45,
            alignment=ft.alignment.center,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            border=ft.border.all(2, "#8ba7ff"),
            content=ft.Image(
                src=profile.get("avatar_id"),
                width=80,
                height=65,
                fit=ft.ImageFit.COVER,
            ),
        )

        label = ft.Text(
            profile.get("name"),
            size=16,
            color="#4A4F5A",
            font_family="LibreBaskerville",
        )

        c = ft.Container(
            content=ft.Column(
                [img, label],
                spacing=4,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=8,
            border=ft.border.all(2 if is_selected else 1, border_color),
            border_radius=12,
            width=160,
            height=130,
        )

        def on_click(e):
            selected_idx["value"] = idx
            refresh_tiles()
            continue_btn.disabled = False
            page.update()

        c.on_click = on_click
        return c

    tiles = [make_profile_tile(profile, i) for i, profile in enumerate(PROFILES)]

    def refresh_tiles():
        for i, c in enumerate(tiles):
            sel = (selected_idx["value"] == i)
            c.border = ft.border.all(
                2 if sel else 1,
                "#6B8AF6" if sel else "#DADDE6",
            )

    # group into rows of 2 for grid layout
    rows: list[ft.Row] = []
    for i in range(0, len(tiles), 2):
        pair = tiles[i:i+2]
        if len(pair) == 1:
            pair.append(ft.Container(width=160, height=130, opacity=0))
        rows.append(ft.Row(pair, alignment=ft.MainAxisAlignment.SPACE_EVENLY))

    # Continue button to enter the app
    continue_btn = ft.ElevatedButton(
        "Continue",
        disabled=True,
        width=200,
        bgcolor="#6562DF",
        color="white",
        on_click=lambda e: page.go("/pin"),
    )

    # Add Profile button (like Home page style)
    add_profile_btn = ft.IconButton(
        icon=ft.Icons.ADD_CIRCLE,
        icon_color="#6562DF",
        tooltip="Add New Profile",
        on_click=lambda e: page.go("/avatars"),
    )


    content = ft.Column(
        [
            ft.Text(
                "Select your Profile",
                size=40,
                color="#423c36",
                font_family="LibreBaskerville-Bold",
                weight=ft.FontWeight.BOLD,
            ),
            add_profile_btn,
            ft.Column(rows, spacing=12, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Container(height=10),
            ft.Row([continue_btn], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=30),
        ],
        spacing=16,
        alignment="center",
        horizontal_alignment="center",
    )

    return ft.Container(
        content=content,
        expand=True,
        padding=20,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#cdffd8", "#94b9ff"],
        ),
    )

def main(page: ft.Page):
    page.add(ProfileSelection(page))

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")