import flet as ft
from home import HomePage
from signup_page import SignUp
from login_page import Login
from collabrewards import CollabRewards
from settings import SettingsPage
from Avatar_page import AvatarSelection
from rewards_store import StorePage
from Pin_page import PinPage
from themed_dashboard import themedDashboard
from chore_details import ChoreDetails
from chore_creation import ChoreCreation


def main(page: ft.Page):
    #page.title = "QuestNest"
    #page.theme_mode = "light"
    page.padding = 0
    page.spacing = 0
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    # Global fonts
    page.fonts = {
        "LibreBaskerville": "/fonts/LibreBaskerville-Regular.ttf",
        "LibreBaskerville-Bold": "/fonts/LibreBaskerville-Bold.ttf",
        "LibreBaskerville-Italic": "/fonts/LibreBaskerville-Italic.ttf",
    }
    
    def route_change(e):
        page.views.clear()
        
        if page.route in ["/", "/home"]:
            page.views.append(ft.View("/", [HomePage(page)]))
        elif page.route == "/create_account":
            page.views.append(ft.View("/create_account", [SignUp(page)]))
        elif page.route == "/login":
            page.views.append(ft.View("/login", [Login(page)]))
        elif page.route == "/collab_rewards":
            page.views.append(ft.View("/collab_rewards", [CollabRewards(page)]))
        elif page.route == "/settings":
            page.views.append(ft.View("/settings", [SettingsPage(page)]))
        elif page.route == "/avatars":
            page.views.append(ft.View("/avatars", [AvatarSelection(page)]))
        elif page.route == "/themed_dashboard":
            page.views.append(ft.View("/themed_dashboard", [themedDashboard(page)]))
        elif page.route == "/store":
            page.views.append(ft.View("/store", [StorePage(page)]))
        elif page.route == "/pin":
            page.views.append(ft.View("/pin", [PinPage(page)]))
        elif page.route == "/calendar":
            page.views.append(ft.View("/calendar", [Calendar(page)]))
        elif page.route == "/details":
            page.views.append(ft.View("/details", [ChoreDetails(page)]))
        elif page.route == "/create_chore":
            page.views.append(ft.View("/create_chore", [ChoreCreation(page)])) 
            
            
        page.update()
    
    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/pin")  # Default to home page


# Run the app
ft.app(target=main, assets_dir="assets")