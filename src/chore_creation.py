import flet as ft

def main(page: ft.Page):
    page.title = "Chore Creation"
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

    def go_dashboard(e):
        page.go("/dashboard")

    def go_store(e):
        page.go("/store")

    def go_calendar(e):
        page.go("/calendar")
    
    def go_settings(e):
        page.go("/settings")

    def logout(e):
        page.go("/")

    def on_nav_change(e: ft.ControlEvent):
        selected_index = e.control.selected_index
        
        if selected_index == 0:
            go_dashboard(e)
        elif selected_index == 1:
            go_store(e)
        elif selected_index == 2:
            go_calendar(e)

    page.appbar = ft.AppBar(
        leading=ft.PopupMenuButton(
            icon=ft.Icons.MENU,
            icon_color="#ffffff",
            items=[
                ft.PopupMenuItem(text="Settings", icon=ft.Icons.SETTINGS, on_click=go_settings),
                ft.PopupMenuItem(),
                ft.PopupMenuItem(text="Log Out", icon=ft.Icons.LOGOUT, on_click=logout),
            ],
        ),
        center_title=True,
        bgcolor="#404040",
    )
    
    # Navigation bar
    page.navigation_bar = ft.NavigationBar(
        bgcolor="#C2B280",
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME_ROUNDED, label="Home"),
            ft.NavigationBarDestination(icon=ft.Icons.SHOPPING_BAG, label="Store"),
            ft.NavigationBarDestination(icon=ft.Icons.CALENDAR_MONTH_OUTLINED, label="Calendar"),
        ],
        on_change=on_nav_change,
    )
    page.navigation_bar.selected_index = -1
    
    # Title at the top of the page
    title = ft.Text (
        "Create New Task",
        size=40,
        weight=ft.FontWeight.BOLD,
        color="indigo",
        text_align="center",
        font_family="LibreBaskerville",
    )

    
    # Input fields for chore creation
    chore_name = ft.TextField(
        label="Chore Name",
        width=350,
        border_radius=10,
        bgcolor="white",
        color="black",
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
        color="black",
        border_color="#8c52ff",
        focused_border_color="#473c9c",
    )

    reward_points = ft.TextField(
        label="Reward Points (XP)",
        width=150,
        border_radius=10,
        bgcolor="white",
        color="black",
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
        width=150,
        border_radius=10,
    )

    due_date = ft.TextField(
        label="Due Date (YYYY-MM-DD)",
        width=150,
        border_radius=10,
        bgcolor="white",
        color="black",
        border_color="#8c52ff",
        focused_border_color="#473c9c",
    )

    task_type = ft.Dropdown(
        label="Task Type",
        options=[
            ft.dropdown.Option("Individual Task"),
            ft.dropdown.Option("Family Task"),
        ],
        width=150,
        border_radius=10,
    )

    require_proof = ft.Switch(
        label="Require Photo Proof",
        value=False,
        active_color="#8c52ff",
        inactive_track_color="#cccccc",
    )

    # Submit chore handler
    def submit_chore():
        print(f"""
        New chore created:
        - Name: {chore_name.value}
        - Description: {chore_desc.value}
        - Points: {reward_points.value}
        - Assignee: {assignee.value}
        - Due Date: {due_date.value}
        - Task Type: {task_type.value}
        - Require Photo Proof: {require_proof.value}
        """)
        page.snack_bar = ft.SnackBar(ft.Text("Submitted Successfully!"))
        page.snack_bar.open = True
        page.update()


    # Card-style container for form
    chore_card = ft.Container(
        content=ft.Column(
            [
                chore_name,
                chore_desc,
                ft.Row([reward_points, assignee], alignment="center"),
                ft.Row([task_type, due_date], alignment="center"),
                require_proof,
                ft.ElevatedButton(
                    "Submit",
                    width=200,
                    bgcolor="#6562DF",
                    color="white",
                    on_click=lambda e: submit_chore(),
                )
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

    # Layout
    content = ft.Column(
        [
            title,
            chore_card,
        ],
        alignment="center",
        horizontal_alignment="center",
        spacing=25,
        expand=True,
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
