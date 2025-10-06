import flet as ft
from auth.db import find_user_by_email
from auth.security import verify_password

class Login(ft.Container):
    """Login card with real verification; routes to /home on success."""
    def __init__(self, page: ft.Page):
        page.fonts = {
            "LibreBaskerville": "/fonts/LibreBaskerville-Regular.ttf",
            "LibreBaskerville-Bold": "/fonts/LibreBaskerville-Bold.ttf",
            "LibreBaskerville-Italic": "/fonts/LibreBaskerville-Italic.ttf",
        }

        email = ft.TextField(label="Email", width=320, prefix_icon=ft.Icons.EMAIL_OUTLINED, border_radius=12)
        password = ft.TextField(label="Password", password=True, can_reveal_password=True,
                                width=320, prefix_icon=ft.Icons.LOCK_OUTLINE, border_radius=12)
        msg = ft.Text("", color="#b91c1c", size=12)

        def _login(e: ft.ControlEvent):
            msg.value = ""
            if not email.value or not password.value:
                msg.value = "Please enter your email and password."
                page.update(); return

            user = find_user_by_email(email.value)
            if not user or not verify_password(password.value, user["password_hash"]):
                msg.value = "Invalid email or password."
                page.update(); return

            # set session and go home
            page.session.set("user_id", user["id"])
            page.session.set("username", user["username"])
            page.go("/home")

        view = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Welcome back", size=32, weight=ft.FontWeight.BOLD,
                            color="black", text_align="center", font_family="LibreBaskerville"),
                    ft.Text("Sign in to continue your quests.", color="#473c9c", size=14,
                            text_align="center", font_family="LibreBaskerville"),
                    ft.Divider(opacity=0),
                    email, password, msg,
                    ft.Row(
                        [
                            ft.ElevatedButton("Log In", icon=ft.Icons.LOGIN, on_click=_login,
                                              style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))),
                            ft.TextButton("Create an account", on_click=lambda e: page.go("/create_account")),
                        ],
                        alignment="center", spacing=14,
                    ),
                ],
                alignment="center", horizontal_alignment="center", spacing=12,
            ),
            padding=20, bgcolor=ft.Colors.WHITE, border_radius=20,
            shadow=ft.BoxShadow(blur_radius=10, color="#999999"), width=380,
            gradient=ft.RadialGradient(center=ft.alignment.center, radius=1.5, colors=["#f6f6f6", "#d8d5d5"]),
        )
        super().__init__(content=view)
