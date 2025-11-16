# PIN screen 

import flet as ft
import requests

BACKEND_URL = "http://127.0.0.1:8000"

def PinPage(page: ft.Page):
    page.title = "QuestNest – PIN"
    
     #Fonts from /assets/fonts
    page.fonts = {
        "LibreBaskerville": "/fonts/LibreBaskerville-Regular.ttf",
        "LibreBaskerville-Bold": "/fonts/LibreBaskerville-Bold.ttf",
        "LibreBaskerville-Italic": "/fonts/LibreBaskerville-Italic.ttf",
    }

    # ---- state ----
    pin = {"value": ""}
    error_msg = ft.Text("", color="red", size=12)

   # Try to get username from previous page
    username = None
    try:
        username = page.session.get("profile_name")
    except AttributeError:
        pass

    if not username:
        # fallback for testing/ensuring app does not break
        username = "TestUser"


    def pin_dot(filled: bool) -> ft.Control:
        # empty/filled dot (visual only)
        return ft.Container(
            width=40, height=40,
            border_radius=12,
            bgcolor="#EEF2F7",
            border=ft.border.all(1, "#2D3C68"),
            alignment=ft.alignment.center,
            content=ft.Text("•" if filled else "", size=24, color="#1a1a1a", weight=ft.FontWeight.W_700),
        )

    def rebuild_dots():
        row.controls = [
            pin_dot(len(pin["value"]) >= 1),
            pin_dot(len(pin["value"]) >= 2),
            pin_dot(len(pin["value"]) >= 3),
            pin_dot(len(pin["value"]) >= 4),
        ]

    def key_button(label: str, on_click) -> ft.Control:
        return ft.Container(
            width=64, height=64,
            border_radius=32,
            bgcolor="#F4F6FA",
            border=ft.border.all(1, "#2D3C68"),
            alignment=ft.alignment.center,
            content=ft.Text(label, size=20, color="#1A1A1A", weight=ft.FontWeight.W_600),
            on_click=on_click,
        )

    def go_back(e):    
        page.go("/avatars")  # Navigate to avatars page on back
        
    # ---- header ----
    header = ft.Row(
    [
        ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            icon_size=20,
            icon_color="#1a1a1a",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=18),
                bgcolor={ft.ControlState.DEFAULT: "#ECF0FF"},
            ),
            on_click=go_back,
        )
    ],
    alignment=ft.MainAxisAlignment.START,
)

    title = ft.Text("Enter PIN", size=26, color="#425986" ,weight=ft.FontWeight.BOLD, font_family="LibreBaskerville")
    subtitle = ft.Text("Enter your 4-digit PIN", size=16, color="#6B7280", font_family="LibreBaskerville")

    # ---- PIN dots panel ----
    row = ft.Row(spacing=12, alignment=ft.MainAxisAlignment.CENTER)
    rebuild_dots()

    pin_panel = ft.Container(
        content=row,
        width=300,
        padding=16,
        border_radius=16,
        bgcolor="#f6f6f6",  # light translucent panel
    )

    # ---- keypad handlers ----
    def press_digit(d: str):
        if len(pin["value"]) < 4:
            pin["value"] += d
            rebuild_dots()
            continue_btn.disabled = len(pin["value"]) != 4
            page.update()

    def press_backspace(e=None):
        if pin["value"]:
            pin["value"] = pin["value"][:-1]
            rebuild_dots()
            continue_btn.disabled = len(pin["value"]) != 4
            page.update()

    def press_clear(e=None):
        pin["value"] = ""
        rebuild_dots()
        continue_btn.disabled = True
        page.update()

    # ---- keypad layout (3x4) ----
    row1 = ft.Row(
        [key_button("1", lambda e: press_digit("1")),
         key_button("2", lambda e: press_digit("2")),
         key_button("3", lambda e: press_digit("3"))],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    )
    row2 = ft.Row(
        [key_button("4", lambda e: press_digit("4")),
         key_button("5", lambda e: press_digit("5")),
         key_button("6", lambda e: press_digit("6"))],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    )
    row3 = ft.Row(
        [key_button("7", lambda e: press_digit("7")),
         key_button("8", lambda e: press_digit("8")),
         key_button("9", lambda e: press_digit("9"))],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    )
    row4 = ft.Row(
        [key_button("C", press_clear),
         key_button("0", lambda e: press_digit("0")),
         key_button("⌫", press_backspace)],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    )

    # ---- footer / continue ----
    def on_continue(e):
        if len(pin["value"]) != 4:
            error_msg.value = "Please enter a 4-digit PIN."
            page.update()
            return

        try:
            resp = requests.post(
                f"{BACKEND_URL}/pin/verify",
                json={"username": username, "pin": pin["value"]},
                timeout=5,
            )
        except Exception:
            error_msg.value = "Could not reach server. Is the backend running?"
            page.update()
            return

        if resp.status_code == 200:
            error_msg.value = ""
            page.go("/themed_dashboard")
        else:
            detail = ""
            try:
                detail = resp.json().get("detail", "")
            except Exception:
                pass
            error_msg.value = f"PIN verification failed. {detail or f'Status {resp.status_code}'}"
            page.update()
        
    continue_btn = ft.ElevatedButton("Continue", width=220, disabled=True, 
                                     on_click=on_continue,  )

    footer_hint = ft.Text(
        "Ask your parents if you forgot your PIN",
        size=12, color="#2D3C68",
    )

    # ---- assemble ----
    content = ft.Column(
        [
            header,
            ft.Text("🛡️", size=38),
            title, subtitle,
            pin_panel,
            ft.Container(height=8),
            row1, row2, row3, row4,
            ft.Container(height=10),
            ft.Row([continue_btn], alignment=ft.MainAxisAlignment.CENTER),
            footer_hint,
        ],
        spacing=12,
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
            colors=["#cdffd8", "#94b9ff"],
        ),
    )
    

def main(page: ft.Page):
    page.add(PinPage(page))
    
if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
