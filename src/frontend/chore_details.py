import flet as ft
import utils as u
import requests

# Define API Base URL (probably move to a config file later)
API_BASE_URL = "http://127.0.0.1:8000"

def ChoreDetails(page: ft.Page):
    page.title = "Chore Details"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.theme_mode = "light"
    page.padding = 0
    page.spacing = 0

    email = page.session.get("email")
    # Retrieve the chore_id selected from the previous page
    chore_id = page.session.get("selected_chore_id")
    
    # Default data placeholder
    chore_data = {
        "title": "Loading...",
        "description": "Fetching details...",
        "reward_points": 0,
        "due_date": "",
        "task_type": "Task",
        "assigned_to": "Unknown"
    }

    # Default avatar path
    assignee_avatar = "images/Avatars/dragon.png"

    # Fetch real data from the Backend API
    if chore_id:
        try:
            # 1. Fetch Chore Details
            resp = requests.get(f"{API_BASE_URL}/chores/{chore_id}", params={"email": email})
            if resp.status_code == 200:
                chore_data = resp.json()
                
                # 2. Fetch Avatar for the Assignee
                try:
                    avatar_resp = requests.get(f"{API_BASE_URL}/avatar/list/{email}")
                    if avatar_resp.status_code == 200:
                        profiles = avatar_resp.json()
                        # specific search for the assigned user's avatar
                        for p in profiles:
                            if p["profile"] == chore_data.get("assigned_to"):
                                raw_avatar = p.get("avatar")
                                
                                # Robust path construction logic
                                if raw_avatar:
                                    # If the DB stores "wizard", convert to "images/Avatars/wizard.png"
                                    # If the DB already stores a path, use it, but fix casing if needed
                                    
                                    # Strip extension if present to normalize
                                    clean_name = raw_avatar.split('.')[0]
                                    
                                    # Clean up if it was stored with path prefixes incorrectly
                                    if "/" in clean_name:
                                        clean_name = clean_name.split("/")[-1]
                                        
                                    assignee_avatar = f"images/Avatars/{clean_name}.png"
                                break
                except Exception as ex:
                    print(f"Error fetching avatars: {ex}")

            else:
                print(f"Error fetching chore: {resp.text}")
                page.snack_bar = ft.SnackBar(ft.Text("Could not load chore details."))
                page.snack_bar.open = True
        except Exception as e:
            print(f"Connection error: {e}")
            page.snack_bar = ft.SnackBar(ft.Text("Connection error. Check backend."))
            page.snack_bar.open = True
    else:
        # If accessed directly without selecting a chore
        print("No chore_id found in session.")

    # Fonts
    page.fonts = {
        "LibreBaskerville": "/fonts/LibreBaskerville-Regular.ttf",
        "LibreBaskerville-Bold": "/fonts/LibreBaskerville-Bold.ttf",
        "LibreBaskerville-Italic": "/fonts/LibreBaskerville-Italic.ttf",
    }

    app_bar = u.application_bar(page)
    nav_bar = u.navigation_bar(page)

    # Handler to go back to the previous view
    def go_back(e):
        print("Returning to Individual Dashboard...")
        page.go("/themed_dashboard")
        
    uploaded_image_path = {"path": None}
    
    # Handler for camera/file picker result
    def open_camera(e: ft.FilePickerResultEvent):
        if e.files:
            file = e.files[0]
            uploaded_image_path["path"] = file.path
            print("Completed Chore Proof Image Uploaded:", file.path)

            submit_btn.visible = True
            
            page.snack_bar = ft.SnackBar(ft.Text(f"Uploaded: {file.name}"))
            page.snack_bar.open = True
            page.update()

    file_picker = ft.FilePicker(on_result=open_camera)
    page.overlay.append(file_picker)
    
    def submit_proof(e):
        # needs to be stored somewhere (media.py)
        page.go("/themed_dashboard")


    submit_btn = ft.ElevatedButton(
        "Submit Proof",
        width=250,
        bgcolor="#28a745",
        color="white",
        visible=False,
        on_click=submit_proof
    )

    # Build the UI Card with Dynamic Data
    chore_card = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Quest Details",
                    size=26,
                    weight=ft.FontWeight.BOLD,
                    font_family="LibreBaskerville-Bold",
                    text_align="center",
                    color="#473c9c",
                ),
                ft.Container(
                    # Use the dynamically fetched avatar path
                    content=ft.Image(
                        src=assignee_avatar, 
                        width=150,
                        height=150,
                        fit=ft.ImageFit.CONTAIN, # Changed to CONTAIN to prevent cutting off
                    ),
                    alignment=ft.alignment.center,
                ),
                # Display the Assignee's Name
                ft.Text(
                    f"Hero: {chore_data.get('assigned_to', 'Unknown')}",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    text_align="center",
                    color="#4A4F5A",
                    font_family="LibreBaskerville",
                ),
                ft.Text(
                    chore_data.get("task_type", "Task"), # Dynamic Task Type
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    text_align="center",
                    font_family="LibreBaskerville-Bold",
                ),
                ft.Text(
                    chore_data["title"], # Dynamic Title
                    size=20,
                    text_align="center",
                    font_family="LibreBaskerville",
                ),
                ft.Text(
                    "Earn Individual XP",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    text_align="center",
                    font_family="LibreBaskerville",
                ),
                ft.Text(
                    f"+{chore_data['reward_points']}", # Dynamic XP Points
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    text_align="center",
                    color="green",
                    font_family="LibreBaskerville-Bold",
                ),
                ft.Text(
                    "Details",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    text_align="center",
                    font_family="LibreBaskerville-Bold",
                ),
                ft.Text(
                    # Combine Description and Due Date
                    f"{chore_data['description']}\nDue: {chore_data.get('due_date', 'No date')}",
                    size=14,
                    text_align="center",
                    font_family="LibreBaskerville",
                ),
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=8,
        ),
        padding=20,
        width=350,
        bgcolor=ft.Colors.WHITE,
        border_radius=20,
        shadow=ft.BoxShadow(blur_radius=10, spread_radius=2, color="#888888"),
    )

    # Bottom Navigation Buttons (Back + Camera)
    bottom_nav = ft.Row(
        [
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_color="white",
                bgcolor="#6562DF",
                on_click=go_back,
            ),
            ft.IconButton(
                icon=ft.Icons.CAMERA_ALT,
                icon_color="white",
                bgcolor="#6562DF",
                on_click=lambda e: file_picker.pick_files(
                    allow_multiple=False,
                    file_type=ft.FilePickerFileType.IMAGE),
            ),
        ],
        alignment="center",
        spacing=40,
    )

    # Main Layout
    content = ft.Column(
        [
            app_bar,
            ft.Column(
                [
                    chore_card,
                    ft.Container(height=20),
                    bottom_nav,
                    submit_btn,
                ],
                alignment="center",
                horizontal_alignment="center",
                spacing=20,
                expand=True,
            ),
            nav_bar,
        ],
        alignment="spaceBetween",
        horizontal_alignment="center",
        expand=True,
    )

    # Return the full container
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
    # For testing: manually set a chore ID here if needed
    # page.session.set("selected_chore_id", "TEST_ID_123")
    page.add(ChoreDetails(page))

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")