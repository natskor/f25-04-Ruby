# questnest/pin.py
# PIN screen (compact, works on older Flet). Simple interactions only.

import flet as ft

def main(page: ft.Page):
    page.title = "QuestNest – PIN"

    # ---- state ----
    pin = {"value": ""}

    # ---- UI helpers ----
    def pin_dot(filled: bool) -> ft.Control:
        # empty/filled dot (visual only)
        return ft.Container(
            width=40, height=40,
            border_radius=12,
            bgcolor="#EEF2F7",
            border=ft.border.all(1, "#DADDE6"),
            alignment=ft.alignment.center,
            content=ft.Text("•" if filled else "", size=24, weight=ft.FontWeight.W_700),
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
            border=ft.border.all(1, "#DADDE6"),
            alignment=ft.alignment.center,
            content=ft.Text(label, size=20, weight=ft.FontWeight.W_600),
            on_click=on_click,
        )

    # ---- header ----
    header = ft.Row(
        [
            ft.Container(
                width=36, height=36, border_radius=18,
                bgcolor="#ECF0FF",
                border=ft.border.all(1, "#D0D6FF"),
                alignment=ft.alignment.center,
                content=ft.Text("←", size=16),
            )
        ],
        alignment=ft.MainAxisAlignment.START,
    )

    title = ft.Text("Enter PIN", size=26, weight=ft.FontWeight.BOLD)
    subtitle = ft.Text("Enter your 4-digit PIN", size=12, color="#6B7280")

    # ---- PIN dots panel ----
    row = ft.Row(spacing=12, alignment=ft.MainAxisAlignment.CENTER)
    rebuild_dots()

    pin_panel = ft.Container(
        content=row,
        padding=16,
        border_radius=16,
        bgcolor="#EAF0FF80",  # light translucent panel
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
        # demo feedback (no real auth)
        page.snack_bar = ft.SnackBar(ft.Text(f"PIN entered: {pin['value']}"))
        page.snack_bar.open = True
        page.update()

    continue_btn = ft.ElevatedButton("Continue", width=220, disabled=True, on_click=on_continue)

    footer_hint = ft.Text(
        "Ask your parents if you forgot your PIN",
        size=11, color="#5575FF",
    )

    # ---- assemble ----
    content = ft.Column(
        [
            header,
            ft.Text("🛡️", size=28),
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

    page.add(
        ft.Container(
            content=content,
            expand=True,
            padding=20,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=["#cdffd8", "#94b9ff"],
            ),
        )
    )

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
