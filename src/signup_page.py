import flet as ft

def SignUp(page: ft.Page):
    # ---------- Page chrome ----------
    page.title = "QuestNest • Sign Up"
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

    # ---------- Card contents ----------
    title = ft.Text(
        "Create your QuestNest account",
        size=28,
        weight=ft.FontWeight.BOLD,
        color="black",
        text_align="center",
        font_family="LibreBaskerville",
    )

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
    confirm = ft.TextField(
        label="Confirm password",
        password=True,
        can_reveal_password=True,
        width=320,
        prefix_icon=ft.Icons.LOCK_PERSON_OUTLINED,
        border_radius=12,
    )
    msg = ft.Text("", color="#b91c1c", size=12)

    def on_signup(e: ft.ControlEvent):
        msg.value = ""
        if not (username.value and email.value and password.value and confirm.value):
            msg.value = "All fields are required."
        elif password.value != confirm.value:
            msg.value = "Passwords do not match."
        else:
            # UI demo only
            page.snack_bar = ft.SnackBar(ft.Text("(Demo) Account created!"), open=True)
        page.update()

    signup_btn = ft.ElevatedButton(
        "Create Account",
        icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
        on_click=on_signup,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
    )

    to_login = ft.TextButton(
        "Back to Login",
        icon=ft.Icons.LOGIN,
        # on_click=lambda e: page.go("/login")  # wire later
    )

    signup_card = ft.Container(
        content=ft.Column(
            [
                title,
                ft.Text("Join your family, complete quests, and earn rewards!",
                        color="#473c9c", size=14, text_align="center",
                        font_family="LibreBaskerville"),
                ft.Divider(opacity=0),
                username, email, password, confirm,
                msg,
                ft.Row([signup_btn], alignment="center"),
                ft.Text("", size=4),
                ft.Row([ft.Text("Already have an account?", color="#404040"), to_login], alignment="center"),
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

    # ---------- Page layout ----------
    content = ft.Column(
        [signup_card],
        alignment="center",
        horizontal_alignment="center",
        spacing=25,
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

    # page.add(
    #     ft.Container(
    #         content=content,
    #         expand=True,
    #         gradient=ft.LinearGradient(
    #             begin=ft.alignment.top_left,
    #             end=ft.alignment.bottom_right,
    #             colors=["#cdffd8", "#94b9ff"],
    #         ),
    #         alignment=ft.alignment.center,
    #     )
    # )
    
def main(page: ft.Page):
    page.add(SignUp(page))

if __name__ == "__main__":
    # Run with your assets:
    #   python -m flet src/signup_page.py -w or python -m src.signup_page
    ft.app(target=main, assets_dir="assets")
