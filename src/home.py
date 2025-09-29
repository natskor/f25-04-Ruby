import flet as ft

def main(page: ft.Page):
    page.title = "QuestNest"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    #page.theme_mode = "light"
    
    page.fonts = {
        "LibreBaskerville": "/fonts/LibreBaskerville-Regular.ttf",
        "LibreBaskerville-Bold": "/fonts/LibreBaskerville-Bold.ttf",
        "LibreBaskerville-Italic": "/fonts/LibreBaskerville-Italic.ttf",
    }
    
    def create_account(route):
        page.go("/create_account")
        
    def login(route):
        page.go("/login")
        
    def home(route):
        page.views.pop()
        page.update()

    def route_change(route):
        if page.route == "/create_account":
            page.views.append(
                ft.View(
                    "/create_account",
                    [
                        ft.Text(
                            "Placeholder Create Account Page GUI Navigation",
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            font_family="LibreBaskerville",
                        ),
                        ft.ElevatedButton("Back", on_click=home),
                    ],
                    horizontal_alignment="center",
                    vertical_alignment="center",
                )
            )
        
        elif page.route == "/login":
            page.views.append(
                ft.View(
                    "/login",
                    [
                        ft.Text(
                            "Placeholder Login Page GUI Navigation",
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            font_family="LibreBaskerville",
                        ),
                        ft.ElevatedButton("Back", on_click=home),
                    ],
                    horizontal_alignment="center",
                    vertical_alignment="center",
                )
            )
        page.update()
    
    page.on_route_change = route_change

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
        on_click=create_account,
    )

    login_btn = ft.ElevatedButton(
        "Login",
        width=200,
        bgcolor="#6562DF",
        color="white",
        on_click=login,
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