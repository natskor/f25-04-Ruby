import flet as ft 

def Login(page: ft.Page):
    #------------Page chrome----------
    page.title = "QuestNest Login"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.theme_mode = "light"
    page.padding = 0
    page.spacing = 0

    #Fonts from /assets/fonts
    page.fonts = {
        "LibreBaskerville": "/fonts/LibreBaskerville-Regular.ttf",
        "LibreBaskerville-Bold": "/fonts/LibreBaskerville-Bold.ttf",
        "LibreBaskerville-Italic": "/fonts/LibreBaskerville-Italic.ttf",
    }

       # ---------- Card contents ----------
    title = ft.Text(
        "Welcome Back!",
        size=32,
        weight=ft.FontWeight.BOLD,
        color="black",
        text_align="center",
        font_family="LibreBaskerville",
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
    error_msg = ft.Text("", color="#b91c1c", size=12)

    def on_login(e: ft.ControlEvent):
        error_msg.value = ""
        if not email.value or not password.value:
            error_msg.value = "Please enter your email and password."
        else:
            # UI demo only
            page.snack_bar = ft.SnackBar(ft.Text("(Demo) Logged in!"), open=True)
        page.update()

    login_btn = ft.ElevatedButton(
        "Log In",
        icon=ft.Icons.LOGIN,
        on_click=on_login,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
    )

    # “Don’t have an account?” row (we’ll link later)
    to_signup = ft.TextButton(
        "Create an account",
        icon=ft.Icons.PERSON_ADD_OUTLINED,
        on_click=lambda e: page.go("/create_account")  # wire later
    )

    login_card = ft.Container(
        content=ft.Column(
            [
                title,
                ft.Text("Sign in to continue your quests.", color="#473c9c", size=14, text_align="center",
                        font_family="LibreBaskerville"),
                ft.Divider(opacity=0),
                email,
                password,
                error_msg,
                ft.Row([login_btn], alignment="center"),
                ft.Text("", size=4),
                ft.Row([ft.Text("New here?", color="#404040"), to_signup], alignment="center"),
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
        [login_card],
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

def main(page: ft.Page):
    page.add(Login(page))

if __name__ == "__main__":
    # Make sure you run with assets available:
    #   python -m flet src/login_page.py -w or python -m src.login_page
    ft.app(target=main, assets_dir="assets")