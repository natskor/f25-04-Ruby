import flet as ft

def main(page: ft.Page):
    # ---------- page chrome ----------
    page.title = "QuestNest • Child Progress"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.theme_mode = "light"
    page.padding = 0
    page.spacing = 0

    # fonts
    page.fonts = {
        "LibreBaskerville": "/fonts/LibreBaskerville-Regular.ttf",
        "LibreBaskerville-Bold": "/fonts/LibreBaskerville-Bold.ttf",
        "LibreBaskerville-Italic": "/fonts/LibreBaskerville-Italic.ttf",
    }

    # menu bar with icons
    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.MENU, icon_color="#ffffff"),
        center_title=True,
        bgcolor="#404040",
        actions=[
            ft.IconButton(ft.Icons.NOTIFICATIONS_OUTLINED, icon_color="#ffffff"),
            ft.IconButton(ft.Icons.SETTINGS, icon_color="#ffffff"),
            ft.IconButton(ft.Icons.SEARCH, icon_color="#ffffff"),
        ],
        title=ft.Text("QuestNest", color="white", font_family="LibreBaskerville-Bold"),
    )

    # ---------- XP progress card ----------
    xp_title = ft.Text(
        "XP Progress",
        size=24,
        weight=ft.FontWeight.BOLD,
        font_family="LibreBaskerville-Bold",
        color="#404040",
        text_align="center"
    )

    child_name_with_stars = ft.Row(
        [
            ft.Icon(ft.Icons.STAR, color="#ffd700", size=24),
            ft.Text("Kaleb", size=18, color="#404040", font_family="LibreBaskerville"),
            ft.Icon(ft.Icons.STAR, color="#ffd700", size=24),
        ],
        alignment="center",
        spacing=6,
    )

    progress_ring = ft.ProgressRing(
        value=0.8,
        width=120,
        height=120,
        stroke_width=20,
        color="#8c52ff",
        bgcolor="#d3d3f0",
    )

    avatar = ft.Container(
        content=ft.Image(
            src="images/character.png",
            width=80,
            height=80,
            fit=ft.ImageFit.CONTAIN,
        ),
        width=80,
        height=80,
        alignment=ft.alignment.center,
    )

    ring_with_avatar = ft.Stack(
        controls=[
            progress_ring,
            ft.Container(
                content=avatar,
                alignment=ft.alignment.center,
                width=120,
                height=120,
            )
        ],
        width=120,
        height=120,
    )

    stars_row = ft.Row(
        [
            ring_with_avatar,
        ],
        alignment="center",
        vertical_alignment="center",
    )

    xp_breakdown = ft.Column(
        [
            ft.Text("Level 5", size=20, weight=ft.FontWeight.BOLD, font_family="LibreBaskerville"),
            ft.Divider(height=1, thickness=2, color="#555555", opacity=1),
            ft.Text("XP Breakdown", size=16, weight=ft.FontWeight.BOLD, font_family="LibreBaskerville"),
            ft.Text("Current Total: 3255", size=14, color="#333333", font_family="LibreBaskerville"),
            ft.Text("Level-Up Needs: 745", size=14, color="#333333", font_family="LibreBaskerville"),
            ft.Text("All-Time Earnings: 54255", size=14, color="#333333", font_family="LibreBaskerville"),
            ft.Divider(height=1, thickness=2, color="#555555", opacity=1),
        ],
        spacing=3,
        horizontal_alignment="center",
    )

    household_rankings = ft.Column(
        [
            ft.Text("Household Rankings", size=16, weight=ft.FontWeight.BOLD, font_family="LibreBaskerville"),
            ft.Divider(height=1, thickness=2, color="#555555", opacity=1),
            ft.Text("1st  Mom", size=14, color="#333333", font_family="LibreBaskerville"),
            ft.Text("2nd  Kaleb", size=14, color="#333333", font_family="LibreBaskerville"),
            ft.Text("3rd  Scarlett", size=14, color="#333333", font_family="LibreBaskerville"),
            ft.Text("4th  Jackson", size=14, color="#333333", font_family="LibreBaskerville"),
            ft.Text("5th  Dad", size=14, color="#333333", font_family="LibreBaskerville"),
        ],
        spacing=2,
        horizontal_alignment="center",
    )

    progress_card = ft.Container(
        content=ft.Column(
            [
                xp_title,
                stars_row,
                child_name_with_stars,
                ft.Divider(opacity=0),
                xp_breakdown,
                household_rankings,
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=12,
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

    # ---------- page layout ----------
    content = ft.Column(
        [progress_card],
        alignment="center",
        horizontal_alignment="center",
        spacing=25,
        expand=True,
    )

    page.add(
        ft.Container(
            content=content,
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["#94b9ff", "#fff6c4"],
            ),
            alignment=ft.alignment.center,
        )
    )

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")