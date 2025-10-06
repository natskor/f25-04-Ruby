import flet as ft
from auth.db import create_user
from auth.security import hash_password

class SignUp(ft.Container):
    """Sign Up card with real DB create; routes to /login on success."""
    def __init__(self, page: ft.Page):
        page.fonts = {
            "LibreBaskerville": "/fonts/LibreBaskerville-Regular.ttf",
            "LibreBaskerville-Bold": "/fonts/LibreBaskerville-Bold.ttf",
            "LibreBaskerville-Italic": "/fonts/LibreBaskerville-Italic.ttf",
        }

        username = ft.TextField(label="Username", width=320, prefix_icon=ft.Icons.PERSON_OUTLINE, border_radius=12)
        email = ft.TextField(label="Email", width=320, prefix_icon=ft.Icons.EMAIL_OUTLINED, border_radius=12)
        password = ft.TextField(label="Password", password=True, can_reveal_password=True,
                                width=320, prefix_icon=ft.Icons.LOCK_OUTLINE, border_radius=12)
        confirm  = ft.TextField(label="Confirm password", password=True, can_reveal_password=True,
                                width=320, prefix_icon=ft.Icons.LOCK_PERSON_OUTLINED, border_radius=12)
        msg = ft.Text("", color="#b91c1c", size=12)

        def _signup(e: ft.ControlEvent):
            msg.value = ""
            if not (username.value and email.value and password.value and confirm.value):
                msg.value = "All fields are required."
                page.update(); return
            if len(username.value.strip()) < 3:
                msg.value = "Username must be at least 3 characters."
                page.update(); return
            if password.value != confirm.value:
                msg.value = "Passwords do not match."
                page.update(); return
            if len(password.value) < 6:
                msg.value = "Password must be at least 6 characters."
                page.update(); return

            err = create_user(username.value, email.value, hash_password(password.value))
            if err:
                msg.value = err
                page.update()
                return

            page.snack_bar = ft.SnackBar(ft.Text("Account created! Please log in."), open=True)
            page.go("/login")

        view = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Create your QuestNest account", size=28, weight=ft.FontWeight.BOLD,
                            color="black", text_align="center", font_family="LibreBaskerville"),
                    ft.Text("Join your family, complete quests, and earn rewards!",
                            color="#473c9c", size=14, text_align="center", font_family="LibreBaskerville"),
                    ft.Divider(opacity=0),
                    username, email, password, confirm, msg,
                    ft.Row(
                        [
                            ft.ElevatedButton("Create Account", icon=ft.Icons.CHECK_CIRCLE_OUTLINE, on_click=_signup,
                                              style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))),
                            ft.TextButton("Back to Login", on_click=lambda e: page.go("/login")),
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

