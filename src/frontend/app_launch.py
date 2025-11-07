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
from verification import verification
from parent_dashboard import parentDashboard
from child_progress import childProgress
from family_calendar import FamilyCalendar
from reward_creation import CreateReward

def main(page: ft.Page):
    page.title = "QuestNest"
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
        
        match page.route:
            case "/" | "/home":
                page.views.append(ft.View("/", [HomePage(page)], padding=0, spacing=0))
            case "/create_account":
                page.views.append(ft.View("/create_account", [SignUp(page)], padding=0, spacing=0))
            case "/login":
                page.views.append(ft.View("/login", [Login(page)], padding=0, spacing=0))
            case "/collab_rewards":
                page.views.append(ft.View("/collab_rewards", [CollabRewards(page)], padding=0, spacing=0))
            case "/settings":
                page.views.append(ft.View("/settings", [SettingsPage(page)], padding=0, spacing=0))
            case "/avatars":
                page.views.append(ft.View("/avatars", [AvatarSelection(page)], padding=0, spacing=0))
            case "/themed_dashboard":
                page.views.append(ft.View("/themed_dashboard", [themedDashboard(page)], padding=0, spacing=0))
            case "/store":
                page.views.append(ft.View("/store", [StorePage(page)], padding=0, spacing=0))
            case "/pin":
                page.views.append(ft.View("/pin", [PinPage(page)], padding=0, spacing=0))
            case "/calendar":
                page.views.append(ft.View("/calendar", [FamilyCalendar(page)], padding=0, spacing=0))
            case "/details":
                page.views.append(ft.View("/details", [ChoreDetails(page)], padding=0, spacing=0))
            case "/create_chore":
                page.views.append(ft.View("/create_chore", [ChoreCreation(page)], padding=0, spacing=0)) 
            case "/verification":
                page.views.append(ft.View("/verification", [verification(page)], padding=0, spacing=0))
            case "/parentDashboard":
                page.views.append(ft.View("/parentDashboard", [parentDashboard(page)], padding=0, spacing=0))
            case "/child_progress":
                page.views.append(ft.View("/child_progress", [childProgress(page)], padding=0, spacing=0))
            case "/create_reward":
                page.views.append(ft.View("/create_reward", [CreateReward(page)], padding=0, spacing=0))
            case _:
                page.views.append(ft.View("/", [HomePage(page)], padding=0, spacing=0))
            
        page.update()
    
    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/")  # Default to home page


# Run the app
ft.app(target=main, assets_dir="assets")