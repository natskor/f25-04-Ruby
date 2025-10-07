import flet as ft

AVATARS = [
    "images/avatars/dragon.png",
    "images/avatars/pegasus.png",
    "images/avatars/unicorn.png",
    "images/avatars/wizard.png",
    "images/avatars/mermaid.png",
    "images/avatars/fairy.png",
]

def AvatarSelection(page: ft.Page):
    page.title = "QuestNest – Avatar"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.padding = 0
    page.spacing = 0
    
    page.fonts = {
        "LibreBaskerville": "/fonts/LibreBaskerville-Regular.ttf",
        "LibreBaskerville-Bold": "/fonts/LibreBaskerville-Bold.ttf",
        "LibreBaskerville-Italic": "/fonts/LibreBaskerville-Italic.ttf",
    }


    selected_idx = {"value": None}
    tiles: list[ft.Container] = []

    def make_tile(path: str, idx: int) -> ft.Container:
        is_selected = selected_idx["value"] == idx
        border_color = "#6B8AF6" if is_selected else "#DADDE6"

       
        img = ft.Container(
            width=90,
            height=90,
            border_radius=45,                     
            alignment=ft.alignment.center,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            border=ft.border.all(2, "#8ba7ff"),               
            content=ft.Image(
                src=path,
                width=80,
                height=65,
                fit=ft.ImageFit.COVER,         
            ),
        )

        label = ft.Text(
            path.split("/")[-1].split(".")[0].title(),
            size=16,
            color="#4A4F5A",
            font_family="LibreBaskerville",
        )

        c = ft.Container(
            content=ft.Column(
                [img, label],
                spacing=4,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=8,
            border=ft.border.all(2 if is_selected else 1, border_color),
            border_radius=12,
            width=160,
            height=130,
        )

        def on_click(e):
            selected_idx["value"] = idx
            refresh_tiles()
            continue_btn.disabled = False
            page.update()

        c.on_click = on_click
        return c

    tiles = [make_tile(path, i) for i, path in enumerate(AVATARS)]

    def refresh_tiles():
        for i, c in enumerate(tiles):
            sel = (selected_idx["value"] == i)
            c.border = ft.border.all(
                2 if sel else 1,
                "#6B8AF6" if sel else "#DADDE6",
            )

    # group into rows of 2 
    rows: list[ft.Row] = []
    for i in range(0, len(tiles), 2):
        pair = tiles[i:i+2]
        if len(pair) == 1:
            pair.append(ft.Container(width=160, height=130, opacity=0))
        rows.append(ft.Row(pair, alignment=ft.MainAxisAlignment.SPACE_EVENLY))

    continue_btn = ft.ElevatedButton("Continue", disabled=True, width=200, on_click=lambda e: page.go("/pin"))

    content = ft.Column(
        [
            ft.Text("Choose Your Avatar!", size=40, color="#423c36", font_family="LibreBaskerville-Bold", weight=ft.FontWeight.BOLD),
            ft.Column(rows, spacing=12, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Container(height=10),
            ft.Row([continue_btn], alignment=ft.MainAxisAlignment.CENTER),
        ],
        spacing=16,
        alignment="center",
        horizontal_alignment="center",
    )

    
    return ft.Container(
        content=content,
        expand=True,
        padding=20,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#cdffd8", "#94b9ff"],  # page background
        ),
    )

    

def main(page: ft.Page):
    page.add(AvatarSelection(page))

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
