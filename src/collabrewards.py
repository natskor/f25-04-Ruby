import flet as ft
# from settings import SettingsPage
# from home import HomePage
# from rewards_store import StorePage


def CollabRewards(page: ft.Page):
    page.title = "Family Reward"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.theme_mode = "light"
    
    # To remove the white space border around the gradient background
    page.padding=0
    page.spacing=0
    
    page.fonts = {
        "LibreBaskerville": "/fonts/LibreBaskerville-Regular.ttf",
        "LibreBaskerville-Bold": "/fonts/LibreBaskerville-Bold.ttf",
        "LibreBaskerville-Italic": "/fonts/LibreBaskerville-Italic.ttf",
    }
    
    def go_dashboard(e):
        page.go("/dashboard")

    def go_store(e):
        page.go("/store")

    def go_calendar(e):
        page.go("/calendar")

    def go_settings(e):
        page.go("/settings")

    def logout(e):
        page.go("/")
    
    def on_nav_change(e: ft.ControlEvent):
        selected_index = e.control.selected_index
        
        if selected_index == 0:
            go_dashboard(e)
        elif selected_index == 1:
            go_store(e)
        elif selected_index == 2:
            go_calendar(e)

    page.appbar = ft.AppBar(
        leading=ft.PopupMenuButton(
            icon=ft.Icons.MENU,
            icon_color="#ffffff",
            items=[
                ft.PopupMenuItem(text="Settings", icon=ft.Icons.SETTINGS, on_click=go_settings),
                ft.PopupMenuItem(),
                ft.PopupMenuItem(text="Log Out", icon=ft.Icons.LOGOUT, on_click=logout),
            ],
        ),
        center_title=True,
        bgcolor="#404040",
    )
    
    # Navigation bar
    page.navigation_bar = ft.NavigationBar(
        bgcolor="#C2B280",
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME_ROUNDED, label="Home"),
            ft.NavigationBarDestination(icon=ft.Icons.SHOPPING_BAG, label="Store"),
            ft.NavigationBarDestination(icon=ft.Icons.CALENDAR_MONTH_OUTLINED, label="Calendar"),
        ],
        on_change=on_nav_change,
    )
    page.navigation_bar.selected_index = -1
    
    # Title
    title = ft.Text(
        "Family Reward",
        size=40,
        weight=ft.FontWeight.BOLD,
        color= "black",
        text_align="center",
        font_family="LibreBaskerville",
        )


    # Reward container
    reward_card = ft.Container(
        content=ft.Column(
            [
                ft.Text("Trip to Busch Gardens\nWilliamsburg",
                        size=18, 
                        weight=ft.FontWeight.BOLD, 
                        text_align="center", 
                        font_family="LibreBaskerville"),
                ft.Text("Limited Time Reward Expires in:\n14 Days", 
                        text_align="center",
                        size=14, 
                        color="#473c9c", 
                        font_family="LibreBaskerville"),
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=5,
        ),
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=15,
        shadow=ft.BoxShadow(blur_radius=10, color="#999999"),
        width=350,
        gradient=ft.RadialGradient(
            center=ft.alignment.center,
            radius=1.5,
            colors=["#f6f6f6", "#d8d5d5"],
        ),
    )

    # Family Progress Ring
    family_progress = ft.Container(
        content=ft.Column(
            [
                ft.ProgressRing(value=0.6, 
                                color="#8c52ff", 
                                width=125, 
                                height=125,
                                stroke_width=25, 
                                bgcolor="#74a8ce",),            
                ft.Icon(ft.Icons.FAMILY_RESTROOM, 
                        color="#473c9c", 
                        size=60),
                ft.Text("Family Progress", 
                        size=18, 
                        weight=ft.FontWeight.BOLD, 
                        font_family="LibreBaskerville"),
                ft.Text("9000 XP / 15000 XP", 
                        size=14, 
                        color="#473c9c", 
                        font_family="LibreBaskerville"),
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=10,
        ),
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=20,
        shadow=ft.BoxShadow(blur_radius=10, color="#999999"),
        width=350,
        gradient=ft.RadialGradient(
            center=ft.alignment.center,
            radius=1.5,
            colors=["#f6f6f6", "#d8d5d5"],
        ),
    )

    # Individual Progress Bar for family reward contribution
    your_progress = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.STAR, color="#df961a", size=45),
                ft.Column(
                    [
                        ft.Container(
                            content=ft.ProgressBar(
                                value=0.6,
                                width=180,
                                bar_height=25,
                                height=30,
                                border_radius=ft.border_radius.all(10),
                                color="#473c9c",
                                bgcolor="#9d9d9d",
                            ),
                            height=25,
                            border_radius=15,
                            alignment=ft.alignment.center,   
                        ),
                        ft.Text(
                            "Your Progress",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            font_family="LibreBaskerville-Bold",
                            text_align="center",
                        ),
                        ft.Text(
                            "3000 XP / 5000 XP",
                            size=14,
                            color="#473c9c",
                            font_family="LibreBaskerville",
                            text_align="center",
                        ),
                    ],
                    alignment="center",
                    horizontal_alignment="center",
                    spacing=5,
                ),
                ft.Icon(ft.Icons.STAR, color="#df961a", size=45),
            ],
            alignment="spaceBetween",
            vertical_alignment="center",
        ),
        padding=20,
        border_radius=20,
        shadow=ft.BoxShadow(blur_radius=10, color="#999999"),
        width=350,
        gradient=ft.RadialGradient(
            center=ft.alignment.center,
            radius=1.5,
            colors=["#f6f6f6", "#d8d5d5"],
        ),
    )

    content = ft.Column(
        [
            title,
            reward_card,
            family_progress,
            your_progress,
        ],
        alignment="center",
        horizontal_alignment="center",
        spacing=25,
        expand=True,
    )
    # page.on_route_change = route_change
    
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
    page.add(CollabRewards(page))

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")