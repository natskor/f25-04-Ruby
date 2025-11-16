import flet as ft
import utils as u
import requests

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
    
    def submit_reward(e):
        
        if not selected_file["path"]:
            page.snack_bar = ft.SnackBar(ft.Text("Please upload an image first!"))
            page.snack_bar.open = True
            page.update()
            return
    
        requests.post("http://127.0.0.1:8000/rewards_store/rewards",
                      files={"image": open(selected_file, "rb")},
                      data={
                          "id": reward_id.value,
                          "name": reward_title.value,
                          "cost": int(xp_cost.value),
                          "level_unlock": int(level_unlock.value),
                        },
                      )

        page.snack_bar = ft.SnackBar(ft.Text("Reward Created!"))
        page.snack_bar.open = True
        page.update()

        # Return to the store page
        page.go("/store")
        
    reward_card = ft.Container(
        content=ft.Column(
            [
                reward_id,
                reward_title,
                ft.Row([xp_cost, level_unlock], alignment="center"),
                ft.Row([upload_button, selected_file_text], alignment="center", spacing=10),
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
        shadow=ft.BoxShadow(blur_radius=12, spread_radius=2, color="#888888"),
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