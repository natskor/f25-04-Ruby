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
    
    #this doesnt work yet lol it only goes to dash so something isnt right in the if block
    def go_back(e):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)
        else:
            page.go("/themed_dashboard")
        
    back_button = ft.Container(
        content=ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            icon_size=22,
            icon_color="#1a1a1a",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=18),
                bgcolor={ft.ControlState.DEFAULT: "#ECF0FF"},
            ),
            on_click=go_back,
        ),
        alignment=ft.alignment.top_left,
        padding=ft.padding.only(left=15, top=15),
        expand=False,
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
    toggle_theme = ft.Switch(label="Themed Mode", value=True,)
    notifications = ft.Switch(label="Enable Notifications", value=False)
    
    settings_card = ft.Container(
        content=ft.Column(
            [
                toggle_theme,
                notifications,
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=20,
        ),
        width=350,
        padding=25,
        bgcolor=ft.Colors.WHITE,
        border_radius=20,
        shadow=ft.BoxShadow(blur_radius=12, color="#999999"),
    )

    content = ft.Column(
        [
            back_button,
            ft.Container(content=title, padding=ft.padding.only(top=10, bottom=20)),
            settings_card,
        ],
        alignment="start",
        horizontal_alignment="center",
        spacing=15,
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
    page.add(SettingsPage(page))

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")