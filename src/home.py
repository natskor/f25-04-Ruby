import flet as ft

def main(page: ft.Page):
    page.title = "QuestNest"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    #page.theme_mode = "light"
    
    page.fonts = {
        "LibreBaskerville": "assets/fonts/LibreBaskerville-Regular.ttf",
        "LibreBaskerville-Bold": "assets/fonts/LibreBaskerville-Bold.ttf",
        "LibreBaskerville-Italic": "assets/fonts/LibreBaskerville-Italic.ttf",
    }
    
    # page.theme = ft.Theme(
    #     font_family="LibreBaskerville",
    # )

    # Title
    title = ft.Text(
        "QuestNest",
        size=40,
        weight=ft.FontWeight.BOLD,
        color= "black",
        text_align="center",
        font_family="LibreBaskerville",
        )

    # Logo
    logo = ft.Container(
        content=ft.Image(
            src="images/logo.png",
            width=500,
            height=500,
            fit=ft.ImageFit.CONTAIN,
        ),
        # expand=True,
        # alignment=ft.alignment.center,
    )


    # Buttons
    create_account_btn = ft.ElevatedButton(
        "Create Account",
        width=200,
        bgcolor="#6562DF",
        color="white",
    )

    login_btn = ft.ElevatedButton(
        "Login",
        width=200,
        bgcolor="#6562DF",
        color="white",
    )


    content = ft.Column(
        [
            title,
            logo,
            ft.Container(height=20),
            create_account_btn,
            login_btn,
        ],
        alignment="center",
        horizontal_alignment="center",
    )

    # Gradient Background
    page.add(
        ft.Container(
            content=content,
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=["#cdffd8", "#94b9ff"],
            ),
        )
    )

ft.app(target=main, assets_dir="assets")