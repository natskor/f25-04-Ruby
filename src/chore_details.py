import flet as ft
import utils as u

def ChoreDetails(page: ft.Page):
    page.title = "Chore Details"
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

    # Navigation back handler
    def go_back(e):
        print("Returning to Individual Dashboard...")
        page.go("/themed_dashboard")
    
    def open_camera(e):
        print("Open camera proof upload...")
        page.snack_bar = ft.SnackBar(ft.Text("Camera feature coming soon!"))
        page.snack_bar.open = True
        page.update()

    # Card with details
    chore_card = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Quest Details",
                    size=26,
                    weight=ft.FontWeight.BOLD,
                    font_family="LibreBaskerville-Bold",
                    text_align="center",
                    color="#473c9c",
                ),
                ft.Container(
                    content=ft.Image(
                        src="images/avatars/dragon.png", 
                        width=150,
                        height=150,
                        fit=ft.ImageFit.COVER,
                    ),
                    alignment=ft.alignment.center,
                ),
                ft.Text(
                    "Task",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    text_align="center",
                    font_family="LibreBaskerville-Bold",
                ),
                ft.Text(
                    "Wash dishes",
                    size=20,
                    text_align="center",
                    font_family="LibreBaskerville",
                ),
                ft.Text(
                    "Earn Individual XP",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    text_align="center",
                    font_family="LibreBaskerville",
                ),
                ft.Text(
                    "+50",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    text_align="center",
                    color="green",
                    font_family="LibreBaskerville-Bold",
                ),
                ft.Text(
                    "Details",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    text_align="center",
                    font_family="LibreBaskerville-Bold",
                ),
                ft.Text(
                    "Wash and put away the dishes by June 15 at 5:00 pm",
                    size=14,
                    text_align="center",
                    font_family="LibreBaskerville",
                ),
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=8,
        ),
        padding=20,
        width=350,
        bgcolor=ft.Colors.WHITE,
        border_radius=20,
        shadow=ft.BoxShadow(blur_radius=10, spread_radius=2, color="#888888"),
    )

    # Bottom navigation (Back + Camera)
    bottom_nav = ft.Row(
        [
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_color="white",
                bgcolor="#6562DF",
                on_click=go_back,
            ),
            ft.IconButton(
                icon=ft.Icons.CAMERA_ALT,
                icon_color="white",
                bgcolor="#6562DF",
                on_click=lambda e: print("Open camera proof upload..."),
            ),
        ],
        alignment="center",
        spacing=40,
    )

    # Layout
    content = ft.Column(
        [
            app_bar,
            ft.Column(
                [
                    chore_card,
                    ft.Container(height=20),
                    bottom_nav,
                ],
                alignment="center",
                horizontal_alignment="center",
                spacing=20,
                expand=True,
            ),
            nav_bar,
        ],
        alignment="spaceBetween",
        horizontal_alignment="center",
        expand=True,
    )

    # Return the container
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
    page.add(ChoreDetails(page))


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
