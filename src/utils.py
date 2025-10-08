import flet as ft

# Navigation Bar
def navigation_bar(page: ft.Page):
    def go_dashboard(e):
        page.go("/dashboard")

    def go_store(e):
        page.go("/store")

    def go_calendar(e):
        page.go("/calendar")

    def on_nav_change(e: ft.ControlEvent):
        selected_index = e.control.selected_index

        routes = ["/themed_dashboard", "/store", "/calendar"]
        new_route = routes[selected_index]

        if page.route != new_route:
            page.go(new_route)

    return ft.Container(
        content=ft.NavigationBar(
            selected_index=-1,
            bgcolor="#C2B280",
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME_ROUNDED, label="Home"),
                ft.NavigationBarDestination(icon=ft.Icons.SHOPPING_BAG, label="Store"),
                ft.NavigationBarDestination(icon=ft.Icons.CALENDAR_MONTH_OUTLINED, label="Calendar"),
            ],
            on_change=on_nav_change,
        ),
        expand=False,
    )

# Application Bar
def application_bar(page: ft.Page):
    def go_settings(e):
        page.go("/settings")

    def logout(e):
        page.go("/")
        
    def create_chore(e):
        page.go("/create_chore")
        
    return ft.Container(
        bgcolor="#404040",
        padding=ft.padding.symmetric(horizontal=15, vertical=10),
        content=ft.Row(
            [
                ft.PopupMenuButton(
                    icon=ft.Icons.MENU,
                    icon_color="#ffffff",
                    items=[
                        ft.PopupMenuItem(text="Settings", icon=ft.Icons.SETTINGS, on_click=go_settings),
                        ft.PopupMenuItem(),
                        ft.PopupMenuItem(text="Log Out", icon=ft.Icons.LOGOUT, on_click=logout),
                    ],
                ),
                ft.IconButton(
                    icon=ft.Icons.EDIT_DOCUMENT,
                    icon_color="#ffffff",
                    tooltip="Create Chore",
                    on_click=create_chore,
                ),
            ],
            alignment="spaceBetween",
            vertical_alignment="center",
        ),
    )