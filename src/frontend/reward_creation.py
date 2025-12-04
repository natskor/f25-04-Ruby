import flet as ft
import utils as u
import requests

API_BASE = "http://127.0.0.1:8000"  # use http unless you actually have TLS
FAMILY_ID = "demo-family"


def CreateReward(page: ft.Page):
    page.title = "Reward Creation"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.theme_mode = "light"
    page.padding = 0
    page.spacing = 0

    page.fonts = {
        "LibreBaskerville": "/fonts/LibreBaskerville-Regular.ttf",
        "LibreBaskerville-Bold": "/fonts/LibreBaskerville-Bold.ttf",
        "LibreBaskerville-Italic": "/fonts/LibreBaskerville-Italic.ttf",
    }

    # App Bar
    app_bar = u.application_bar(page)
    # Navigation bar
    nav_bar = u.navigation_bar(page)

    title = ft.Text(
        "Create New Reward",
        size=40,
        weight=ft.FontWeight.BOLD,
        color="#473c9c",
        text_align="center",
        font_family="LibreBaskerville-Bold",
    )

    reward_id = ft.TextField(
        label="Reward ID",
        width=350,
        border_radius=10,
        bgcolor="white",
        color="black",
        border_color="#8c52ff",
        focused_border_color="#473c9c",
    )

    reward_title = ft.TextField(
        label="Reward Title",
        width=350,
        border_radius=10,
        bgcolor="white",
        color="black",
        border_color="#8c52ff",
        focused_border_color="#473c9c",
    )

    xp_cost = ft.TextField(
        label="XP Cost",
        width=150,
        border_radius=10,
        bgcolor="white",
        color="black",
        border_color="#8c52ff",
        focused_border_color="#473c9c",
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    level_unlock = ft.TextField(
        label="Unlock Level",
        width=150,
        border_radius=10,
        bgcolor="white",
        color="black",
        border_color="#8c52ff",
        focused_border_color="#473c9c",
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    reward_type = ft.Dropdown(
        label="Reward Type",
        width=350,
        border_radius=10,
        bgcolor="white",
        color="black",
        border_color="#8c52ff",
        focused_border_color="#473c9c",
        options=[
            ft.dropdown.Option("Individual"),
            ft.dropdown.Option("Family"),
        ],
        value="Individual",
    )

    selected_file_text = ft.Text("No image selected", color="#473c9c", size=12)
    selected_file = {"path": None}

    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
            selected_file["path"] = e.files[0].path
            selected_file_text.value = e.files[0].name
            page.update()

    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)

    upload_button = ft.ElevatedButton(
        text="Upload Image",
        width=200,
        bgcolor="#6562DF",
        color="white",
        on_click=lambda _: file_picker.pick_files(allow_multiple=False),
    )

    family_email = page.session.get("email")

    def submit_reward(e):
        # --- Family collab reward branch (existing behavior) ---
        if reward_type.value == "Family":
            if not family_email:
                page.snack_bar = ft.SnackBar(
                    ft.Text("No family email in session."), open=True
                )
                page.update()
                return

            try:
                resp = requests.post(
                    f"{API_BASE}/collabrewards/create",
                    data={
                        "email": family_email,
                        "title": reward_id.value,
                        "description": reward_title.value,
                        "goal_xp": int(xp_cost.value or 0),
                    },
                )
            except Exception as ex:
                print("Error creating family reward:", ex)
                page.snack_bar = ft.SnackBar(
                    ft.Text("Network error creating family reward."), open=True
                )
                page.update()
                return

            if resp.status_code == 200:
                page.snack_bar = ft.SnackBar(ft.Text("Family Reward Created!"))
                page.snack_bar.open = True
                page.go("/collab_rewards")
                page.update()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Error: " + resp.text))
                page.snack_bar.open = True
                page.update()
            return

        # --- Individual reward branch → goes to /families/{family_id}/rewards ---

        # basic validation
        if not reward_id.value.strip() or not reward_title.value.strip():
            page.snack_bar = ft.SnackBar(
                ft.Text("Reward ID and Title are required."), open=True
            )
            page.update()
            return

        if not xp_cost.value.strip().isdigit():
            page.snack_bar = ft.SnackBar(
                ft.Text("XP Cost must be a number."), open=True
            )
            page.update()
            return

        if not level_unlock.value.strip().isdigit():
            page.snack_bar = ft.SnackBar(
                ft.Text("Unlock Level must be a number."), open=True
            )
            page.update()
            return

        # For now we are not wiring the uploaded file into backend yet.
        # Backend expects image_url string, so we send None or a placeholder.
        payload = {
            "id": reward_id.value.strip(),
            "name": reward_title.value.strip(),
            "cost": int(xp_cost.value.strip()),
            "level_unlock": int(level_unlock.value.strip()),
            "image_url": None,          # could later be a URL from storage
            "is_family_rewards": False, # this is an individual reward
        }

        try:
            resp = requests.post(
                f"{API_BASE}/families/{FAMILY_ID}/rewards",
                json=payload,
            )
        except Exception as ex:
            print("Error creating individual reward:", ex)
            page.snack_bar = ft.SnackBar(
                ft.Text("Network error creating reward."), open=True
            )
            page.update()
            return

        if resp.status_code == 200:
            page.snack_bar = ft.SnackBar(ft.Text("Reward Created!"))
            page.snack_bar.open = True
            page.go("/store")  # matches your StorePage route
            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Error: " + resp.text))
            page.snack_bar.open = True
            page.update()

    reward_card = ft.Container(
        content=ft.Column(
            [
                reward_id,
                reward_title,
                ft.Row([xp_cost, level_unlock], alignment="center"),
                reward_type,
                ft.Row(
                    [upload_button, selected_file_text],
                    alignment="center",
                    spacing=10,
                ),
                ft.ElevatedButton(
                    "Submit Reward",
                    width=200,
                    bgcolor="#6562DF",
                    color="white",
                    on_click=submit_reward,
                ),
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=20,
        ),
        padding=25,
        width=400,
        bgcolor=ft.Colors.WHITE,
        border_radius=20,
        shadow=ft.BoxShadow(
            blur_radius=12, spread_radius=2, color="#888888"
        ),
    )

    content = ft.Column(
        [
            app_bar,
            title,
            ft.Column(
                [reward_card],
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
    page.add(CreateReward(page))


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
