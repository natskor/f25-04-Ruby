import flet as ft

class SignUp(ft.Container):
    """UI-only Sign Up card with navigation callbacks (no backend)."""
    def __init__(
        self,
        page: ft.Page,
        on_signup=None,     # (e, username, email, password) -> None
        on_to_login=None,   # (e) -> None
    ):
        page.fonts = {
            "LibreBaskerville": "/fonts/LibreBaskerville-Regular.ttf",
            "LibreBaskerville-Bold": "/fonts/LibreBaskerville-Bold.ttf",
            "LibreBaskerville-Italic": "/fonts/LibreBaskerville-Italic.ttf",
        }

        username = ft.TextField(
            label="Username",
            width=320,
            prefix_icon=ft.Icons.PERSON_OUTLINE,
            border_radius=12,
        )
        email = ft.TextField(
            label="Email",
            width=320,
            prefix_icon=ft.Icons.EMAIL_OUTLINED,
            border_radius=12,
        )
        password = ft.TextField(
            label="Password",
            password=True,
            can_reveal_password=True,
            width=320,
            prefix_icon=ft.Icons.LOCK_OUTLINE,
            border_radius=12,
        )
        confirm  = ft.TextField(
            label="Confirm password",
            password=True,
            can_reveal_password=True,
            width=320,
            prefix_icon=ft.Icons.LOCK_PERSON_OUTLINED,
            border_radius=12,
        )
        msg = ft.Text("", color="#b91c1c", size=12)

        def _signup(e: ft.ControlEvent):
            if not (username.value and email.value and password.value and confirm.value):
                msg.value = "All fields are required."
                e.page.update(); return
            if password.value != confirm.value:
                msg.value = "Passwords do not match."
                e.page.update(); return
            if on_signup:
                on_signup(e, username.value, email.value, password.value)
            else:
                e.page.snack_bar = ft.SnackBar(ft.Text("(Demo) Account created!"), open=True)
                e.page.update()

        def _to_login(e: ft.ControlEvent):
            if on_to_login:
                on_to_login(e)

        view = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Create your QuestNest account",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color="black",
                        text_align="center",
                        font_family="LibreBaskerville",
                    ),
                    ft.Text(
                        "Join your family, complete quests, and earn rewards!",
                        color="#473c9c",
                        size=14,
                        text_align="center",
                        font_family="LibreBaskerville",
                    ),
                    ft.Divider(opacity=0),
                    username, email, password, confirm, msg,
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Create Account",
                                icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
                                on_click=_signup,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                            ),
                            ft.TextButton("Back to Login", on_click=_to_login),
                        ],
                        alignment="center",
                        spacing=14,
                    ),
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

        super().__init__(content=view)

# ---- Standalone preview (optional) ----
def main(page: ft.Page):
    page.title = "QuestNest • Sign Up"
    page.theme_mode = "light"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.padding = 0
    page.spacing = 0

    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.MENU, icon_color="#ffffff"),
        center_title=True,
        bgcolor="#404040",
        actions=[
            ft.IconButton(ft.Icons.NOTIFICATIONS_OUTLINED, icon_color="#ffffff"),
            ft.IconButton(ft.Icons.SETTINGS, icon_color="#ffffff"),
            ft.IconButton(ft.Icons.SEARCH, icon_color="#ffffff"),
        ],
        title=ft.Text("QuestNest", color="white", font_family="LibreBaskerville-Bold"),
    )

    page.add(
        ft.Container(
            content=SignUp(page),
            expand=True,
            alignment=ft.alignment.center,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=["#cdffd8", "#94b9ff"],
            ),
        )
    )

if __name__ == "__main__":
    ft.app(target=main, assets_dir="src/assets")
