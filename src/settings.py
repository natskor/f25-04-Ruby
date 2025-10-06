import flet as ft

def SettingsPage(page: ft.Page):
    page.title = "QuestNest • Settings"
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
    
    #this doesnt work yet lol
    def go_back(e):
        page.views.pop
        page.go(page.views[-1].route)
        
    header = ft.Row(
        [
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_size=20,
                icon_color="#1a1a1a",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=18),
                    bgcolor={ft.ControlState.DEFAULT: "#ECF0FF"},
                ),
                on_click=go_back,
            ),
        ],
        alignment=ft.MainAxisAlignment.START,
    )

    title = ft.Text(
        "Settings",
        size=36,
        weight=ft.FontWeight.BOLD,
        color="black",
        text_align="center",
        font_family="LibreBaskerville-Bold",
    )

    # Example content
    toggle_theme = ft.Switch(label="Dark Mode", value=False)
    notifications = ft.Switch(label="Enable Notifications", value=True)

    content = ft.Column(
        [header, title, toggle_theme, notifications],
        alignment="center",
        horizontal_alignment="center",
        spacing=20,
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
    page.add(SettingsPage(page))

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")