import flet as ft

def main(page: ft.Page):
    page.title = "Family Reward - Chore Creation"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.padding = 0
    page.spacing = 0

    page.fonts = {
        "LibreBaskerville": "/fonts/LibreBaskerville-Regular.ttf",
        "LibreBaskerville-Bold": "/fonts/LibreBaskerville-Bold.ttf",
        "LibreBaskerville-Italic": "/fonts/LibreBaskerville-Italic.ttf",
    }

    # AppBar
    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda e: print("Go Back")),
        title=ft.Text("Create a New Chore", size=20, font_family="LibreBaskerville-Bold"),
        center_title=True,
        bgcolor="#404040",
        actions=[
            ft.IconButton(ft.Icons.SAVE, icon_color="white", on_click=lambda e: save_chore())
        ],
    )

    # Input fields for chore creation
    chore_name = ft.TextField(
        label="Chore Name",
        width=350,
        border_radius=10,
        bgcolor="white",
        border_color="#8c52ff",
        focused_border_color="#473c9c",
    )

    chore_desc = ft.TextField(
        label="Description",
        multiline=True,
        min_lines=3,
        max_lines=5,
        width=350,
        border_radius=10,
        bgcolor="white",
        border_color="#8c52ff",
        focused_border_color="#473c9c",
    )

    reward_points = ft.TextField(
        label="Reward Points (XP)",
        width=200,
        border_radius=10,
        bgcolor="white",
        border_color="#8c52ff",
        focused_border_color="#473c9c",
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    assignee = ft.Dropdown(
        label="Assign to",
        options=[
            ft.dropdown.Option("Mom"),
            ft.dropdown.Option("Dad"),
            ft.dropdown.Option("Alice"),
            ft.dropdown.Option("Bob"),
        ],
        width=200,
        border_radius=10,
    )

    due_date = ft.TextField(
        label="Due Date (YYYY-MM-DD)",
        width=200,
        border_radius=10,
        bgcolor="white",
        border_color="#8c52ff",
        focused_border_color="#473c9c",
    )

    # Save chore handler
    def save_chore():
        print(f"New chore created: {chore_name.value}, {reward_points.value} XP, assigned to {assignee.value}")
        page.snack_bar = ft.SnackBar(ft.Text("Chore Saved Successfully!"))
        page.snack_bar.open = True
        page.update()

    # Layout
    content = ft.Column(
        [
            chore_name,
            chore_desc,
            ft.Row([reward_points, assignee], alignment="center"),
            due_date,
            ft.ElevatedButton(
                "Save Chore",
                width=200,
                bgcolor="#6562DF",
                color="white",
                on_click=lambda e: save_chore(),
            )
        ],
        alignment="center",
        horizontal_alignment="center",
        spacing=20,
    )

    page.add(
        ft.Container(
            content=content,
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=["#cdffd8", "#94b9ff"],
            ),
            alignment=ft.alignment.center,
        )
    )

ft.app(target=main, assets_dir="assets")