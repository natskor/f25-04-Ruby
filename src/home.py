import flet as ft
from signup_page import SignUp
from login_page import Login
from auth.db import init_db, create_user, find_user_by_email
from auth.security import hash_password, verify_password 

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
    
    def route_change(e):
        page.views.clear()
        
        if page.route == "/":
            page.views.append(home_page)
            
        if page.route == "/create_account":
            page.views.append(   
                ft.View(
                    "/create_account",
                    [SignUp(page)],
                    horizontal_alignment="center",
                    vertical_alignment="center",
                    padding=0,
                    spacing=0,
                )
            )
        
        elif page.route == "/login":
            page.views.append(
                ft.View(
                    "/login",
                    [Login(page)],
                    horizontal_alignment="center",
                    vertical_alignment="center",
                    padding=0,
                    spacing=0,
                )
            )
        page.update()
    
    page.on_route_change = route_change
    page.go("/")

    # home_page = ft.View(
    #     "/",
    #     [
    #         ft.Container(
    #             content = ft.Column(
    #                 [
    #                     title,
    #                     logo,
    #                     ft.Container(height=20),
    #                     create_account_btn,
    #                     login_btn,
    #                 ],
    #                 alignment="center",
    #                 horizontal_alignment="center",
    #                 spacing=20,
    #             ),
    #             expand=True,
    #             gradient=ft.LinearGradient(
    #             begin=ft.alignment.top_left,
    #             end=ft.alignment.bottom_right,
    #             colors=["#cdffd8", "#94b9ff"],
    #         ),    
    #         )
    #     ],
    #     horizontal_alignment="center",
    #     vertical_alignment="center",
    # )
    
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