import flet as ft

def main(page: ft.Page):
    # ---------- page chrome ----------
    page.title = "QuestNest • Task Verification"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.theme_mode = "light"
    page.padding = 0
    page.spacing = 0

    # fonts 
    page.fonts = {
        "LibreBaskerville": "/fonts/LibreBaskerville-Regular.ttf",
        "LibreBaskerville-Bold": "/fonts/LibreBaskerville-Bold.ttf",
        "LibreBaskerville-Italic": "/fonts/LibreBaskerville-Italic.ttf",
    }

    # menu bar with icons
    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.MENU, icon_color="#ffffff"),
        center_title=True,
        bgcolor="#404040",
        actions=[
            ft.IconButton(ft.Icons.NOTIFICATIONS_OUTLINED, icon_color="#ffffff"),
            ft.IconButton(ft.Icons.SETTINGS, icon_color="#ffffff"),
            ft.IconButton(ft.Icons.SEARCH, icon_color="#ffffff"),
        ],
        # title=ft.Text("QuestNest", color="white", font_family="LibreBaskerville-Bold"),
    )

    # ---------- verification card ----------
    task_title = ft.Text(
        "Task",
        size=24,
        weight=ft.FontWeight.BOLD,
        color="black",
        text_align="center",
        font_family="LibreBaskerville-Bold",
    )
    task_name = ft.Text(
        "Clean Room",
        size=20,
        color="#404040",
        text_align="center",
        font_family="LibreBaskerville",
    )
    subtitle = ft.Text(
        "Did Kaleb Complete the Chore?",
        size=16,
        italic=True,
        color="#404040",
        text_align="center",
        font_family="LibreBaskerville",
    )

    task_image = ft.Image(
        src="images/room.png",  
        width=250,
        height=160,
        fit=ft.ImageFit.COVER,
        border_radius=10,
    )

    feedback = ft.TextField(
        label="Feedback",
        multiline=True,
        min_lines=2,
        max_lines=4,
        width=300,
        border_radius=12,
        hint_text="Describe how the task could be improved or send a positive message",
    )

    def verify(e: ft.ControlEvent):
        page.snack_bar = ft.SnackBar(ft.Text("(Demo) Task verified! "), open=True)
        page.update()

    def reject(e: ft.ControlEvent):
        page.snack_bar = ft.SnackBar(ft.Text("(Demo) Task rejected "), open=True)
        page.update()

    buttons = ft.Row(
        [
            ft.IconButton(ft.Icons.CHECK, icon_color="white", bgcolor="#228b22",
                          icon_size=35, on_click=verify, style=ft.ButtonStyle(shape=ft.CircleBorder())),
            ft.IconButton(ft.Icons.CLOSE, icon_color="white", bgcolor="#8b0000",
                          icon_size=35, on_click=reject, style=ft.ButtonStyle(shape=ft.CircleBorder())),
        ],
        alignment="spaceEvenly",
        vertical_alignment="center",
    )

    verification_card = ft.Container(
        content=ft.Column(
            [
                task_title,
                task_name,
                subtitle,
                task_image,
                feedback,
                ft.Divider(opacity=0),
                ft.Text("Verify Task as Completed?", size=14, color="#404040"),
                buttons,
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=12,
        ),
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=20,
        shadow=ft.BoxShadow(blur_radius=10, color="#999999"),
        width=380,
        gradient=ft.RadialGradient(
            center=ft.alignment.center,
            radius=1.5,
            colors=["#f6f6f6", "#d8d5d5"],
        ),
    )

    # ---------- page layout ----------
    content = ft.Column(
        [verification_card],
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

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
