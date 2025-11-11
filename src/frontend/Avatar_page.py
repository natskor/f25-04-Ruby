import flet as ft
import requests

BACKEND_URL = "http://127.0.0.1:8000"

AVATARS = [
    "images/avatars/dragon.png",
    "images/avatars/pegasus.png",
    "images/avatars/unicorn.png",
    "images/avatars/wizard.png",
    "images/avatars/mermaid.png",
    "images/avatars/fairy.png",
]

def AvatarSelection(page: ft.Page):
    page.title = "QuestNest – Avatar"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.padding = 0
    page.spacing = 0
    
    page.fonts = {
        "LibreBaskerville": "/fonts/LibreBaskerville-Regular.ttf",
        "LibreBaskerville-Bold": "/fonts/LibreBaskerville-Bold.ttf",
        "LibreBaskerville-Italic": "/fonts/LibreBaskerville-Italic.ttf",
    }
    
    profile_name = ft.TextField(
        label="Profile Name",
        hint_text="Enter a name for this profile",
        width=300,
        border_radius=10,
        bgcolor="#ffffff",
        color="black",
        border_color="#8c52ff",
        focused_border_color="#473c9c",
        text_align=ft.TextAlign.CENTER,
        text_size=16,
    )

    error_msg = ft.Text("", color="red", size=12)

    selected_idx = {"value": None}
    tiles: list[ft.Container] = []
    continue_btn_ref = {"btn": None}  # avoid nonlocal issues 

    def make_tile(path: str, idx: int) -> ft.Container:
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
                src=path,
                width=80,
                height=65,
                fit=ft.ImageFit.COVER,         
            ),
        )

        label = ft.Text(
            path.split("/")[-1].split(".")[0].title(),
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
            if continue_btn_ref["btn"] is not None:
                continue_btn_ref["btn"].disabled = False
            error_msg.value = ""
            page.update()

        c.on_click = on_click
        return c

    tiles = [make_tile(path, i) for i, path in enumerate(AVATARS)]

    def refresh_tiles():
        for i, c in enumerate(tiles):
            sel = (selected_idx["value"] == i)
            c.border = ft.border.all(
                2 if sel else 1,
                "#6B8AF6" if sel else "#DADDE6",
            )

    # group into rows of 2 
    rows: list[ft.Row] = []
    for i in range(0, len(tiles), 2):
        pair = tiles[i:i+2]
        if len(pair) == 1:
            pair.append(ft.Container(width=160, height=130, opacity=0))
        rows.append(ft.Row(pair, alignment=ft.MainAxisAlignment.SPACE_EVENLY))

    def on_continue(e):
        # must have avatar
        if selected_idx["value"] is None:
            error_msg.value = "Please choose an avatar."
            page.update()
            return

        # must have profile name
        username = profile_name.value.strip()
        if not username:
            error_msg.value = "Please enter a profile name."
            page.update()
            return

        avatar_path = AVATARS[selected_idx["value"]]

        try:
            resp = requests.post(
                f"{BACKEND_URL}/avatar",
                json={"username": username, "avatar_id": avatar_path},
                timeout=5,
            )
        except Exception:
            error_msg.value = "Could not reach server. Is the backend running?"
            page.update()
            return

        if resp.status_code == 200:
            # remember for CreatePIN page
            # (this assumes you're using page.go routing elsewhere)
            try:
                page.session.set("profile_name", username)
                page.session.set("avatar_id", avatar_path)
            except AttributeError:
                # if session isn't available in your Flet version, you can
                # swap this later for your team's shared state approach
                pass

            error_msg.value = ""
            page.go("/create_pin")
        else:
            # show backend error
            detail = ""
            try:
                detail = resp.json().get("detail", "")
            except Exception:
                pass
            error_msg.value = f"Avatar save failed. {detail or f'Status {resp.status_code}'}"

        page.update()

    continue_btn = ft.ElevatedButton(
        "Continue",
        disabled=True,
        width=200,
        on_click=on_continue,
    )
    continue_btn_ref["btn"] = continue_btn

    # --- page content ---

    content = ft.Column(
        [
            ft.Text(
                "Choose Your Avatar!",
                size=40,
                color="#423c36",
                font_family="LibreBaskerville-Bold",
                weight=ft.FontWeight.BOLD,
            ),
            profile_name,
            error_msg,
            ft.Column(
                rows,
                spacing=12,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Container(height=10),
            ft.Row([continue_btn], alignment=ft.MainAxisAlignment.CENTER),
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
            colors=["#cdffd8", "#94b9ff"],  # same pretty background
        ),
    )


def main(page: ft.Page):
    page.add(AvatarSelection(page))


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")