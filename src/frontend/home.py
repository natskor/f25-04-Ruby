import flet as ft
from signup_page import SignUp
from login_page import Login

def HomePage(page: ft.Page):
    page.title = "QuestNest"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    #page.theme_mode = "light"
    page.padding= 0
    page.spacing= 0
    
    page.fonts = {
        "LibreBaskerville": "/fonts/LibreBaskerville-Regular.ttf",
        "LibreBaskerville-Bold": "/fonts/LibreBaskerville-Bold.ttf",
        "LibreBaskerville-Italic": "/fonts/LibreBaskerville-Italic.ttf",
    }
    
    def create_account(e):
        page.go("/create_account")
        
    def login(e):
        page.go("/login")

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
    page.add(HomePage(page))

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")