import flet as ft

def main(page: ft.Page):
    page.title = "Rewards Store"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    
    page.fonts = {
    "LibreBaskerville": "assets/fonts/LibreBaskerville-Regular.ttf",
    "LibreBaskerville-Bold": "assets/fonts/LibreBaskerville-Bold.ttf"
    }

    #currently not displaying font accurately, will look @ later
    #page.theme = ft.Theme(font_family="LibreBaskerville")
    #page.add(ft.Text("Test Text #1", size=40"))

ft.app(main, assets_dir="assets/fonts")