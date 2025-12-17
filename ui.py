# magizh_buddy_ui.py
# Run: python magizh_buddy_ui.py
# Requirements: pip install flet
# The provided mockup image path (developer note): /mnt/data/ChatGPT Image Dec 5, 2025, 01_15_39 PM.png
# If you have separate asset images, put them in an "assets/" folder and update the paths below.

import os
import flet as ft

# --- Optional integration placeholders (so this UI runs even if Brain/AudioEngine don't exist) ---
try:
    from brain import Brain
except Exception:
    class Brain:
        def __init__(self, api_key=None):
            pass
        def get_random_quote(self):
            return "Be gentle to yourself today."
        def analyze_sentiment(self, text):
            # returns polarity, color
            return 0.0, ft.colors.BLUE_200
        async def get_response(self, text, polarity=0.0):
            return "I hear you. It's okay to feel like that."

try:
    from audio_engine import AudioEngine
except Exception:
    class AudioEngine:
        def __init__(self):
            pass
        def transcribe(self, path):
            return "placeholder transcribed text"
        async def speak(self, text, voice=None, pitch=None, rate=None):
            return None

ASSET_IMAGE = "/mnt/data/ChatGPT Image Dec 5, 2025, 01_15_39 PM.png"
if not os.path.exists(ASSET_IMAGE):
    # fallback to built-in placeholder if the path isn't available
    ASSET_IMAGE = None

# --- App UI ---
def main(page: ft.Page):
    page.title = "MagizhBuddy — UI Mockup"
    page.window_width = 420
    page.window_height = 820
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.bgcolor = ft.colors.WHITE

    # Gradient wrapper to match the mockup soft blues
    page.background = ft.Container(
        expand=True,
        padding=0,
        # subtle vertical gradient
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#F1F8FF", "#E8F9FF"]
        )
    )

    # App state
    current_voice = "en-IN-NeerjaNeural"
    current_language = "English"

    brain = Brain(api_key=os.getenv("GEMINI_API_KEY", None))
    audio_engine = AudioEngine()

    # --- Reusable styles & helpers ---
    CARD_RADIUS = 26
    def rounded_card(content, width=360, height=None, bgcolor="#E9F7FF"):
        return ft.Container(
            content=content,
            width=width,
            height=height,
            padding=20,
            border_radius=ft.border_radius.all(CARD_RADIUS),
            bgcolor=bgcolor,
            alignment=ft.alignment.top_center,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT)
        )

    # --- Screens (6 screens to reflect your mockup) ---
    screens = [None]*6
    # Screen 0: Welcome
    welcome_stack = ft.Column(
        [
            ft.Container(height=18),
            ft.Text("welcome to", size=20, weight=ft.FontWeight.MEDIUM, color="#264653"),
            ft.Text("MagizhBuddy", size=34, weight=ft.FontWeight.BOLD, color="#1b4965"),
            ft.Container(height=18),
            # Hero image (use provided mockup image as a placeholder)
            ft.Container(
                content=ft.Image(src=ASSET_IMAGE or "https://picsum.photos/400/400", fit=ft.ImageFit.CONTAIN),
                width=320,
                height=320,
                border_radius=ft.border_radius.all(180),
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                bgcolor="#FFFFFF"
            ),
            ft.Container(height=24),
            ft.Text(
                "A friendly companion to listen and bring a little cheer. Tap Buddy to begin.",
                size=14, text_align=ft.TextAlign.CENTER, color="#2E3A59"
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    screens[0] = rounded_card(welcome_stack, width=380, bgcolor="#EAF6FF")

    # Screen 1: Chat input (bear + input box)
    chat_messages = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=12, width=360, height=360)
    chat_input = ft.TextField(
        hint_text="Type a message",
        expand=True,
        suffix=ft.IconButton(icon=ft.icons.MIC, on_click=lambda e: page.snack_bar.open_dialog("Mic pressed")),
        border_radius=20
    )

    def send_chat_msg(e):
        if chat_input.value:
            chat_messages.controls.append(
                ft.Row([ft.Container(content=ft.Text(chat_input.value), padding=10, border_radius=12, bgcolor="#DFF3FF")],
                       alignment=ft.MainAxisAlignment.END)
            )
            chat_input.value = ""
            page.update()

    send_btn = ft.FilledButton("Send", on_click=send_chat_msg)
    chat_column = ft.Column(
        [
            ft.Container(
                content=ft.Image(src=ASSET_IMAGE or "https://picsum.photos/200/200", fit=ft.ImageFit.CONTAIN),
                width=160, height=160, border_radius=ft.border_radius.all(90), bgcolor="#FFFFFF"
            ),
            ft.Container(height=6),
            ft.Text("Hi, I feel sad", size=18, color="#143A52", weight=ft.FontWeight.MEDIUM),
            ft.Container(height=12),
            chat_messages,
            ft.Row([chat_input, send_btn], spacing=8)
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    screens[1] = rounded_card(chat_column, width=380, bgcolor="#E6F3FF")

    # Screen 2: Mood check-in (emoji buttons)
    def on_mood_click(e, mood):
        page.snack_bar = ft.SnackBar(ft.Text(f"Thanks for sharing — you selected: {mood}"))
        page.snack_bar.open = True
        page.update()

    mood_row = ft.Row([
        ft.Container(ft.Text("😟", size=28), width=68, height=68, alignment=ft.alignment.center,
                     border_radius=ft.border_radius.all(34), bgcolor="#FFFFFF", on_click=lambda e: on_mood_click(e, "Sad")),
        ft.Container(ft.Text("🙂", size=28), width=68, height=68, alignment=ft.alignment.center,
                     border_radius=ft.border_radius.all(34), bgcolor="#FFFFFF", on_click=lambda e: on_mood_click(e, "Okay")),
        ft.Container(ft.Text("😊", size=28), width=68, height=68, alignment=ft.alignment.center,
                     border_radius=ft.border_radius.all(34), bgcolor="#FFFFFF", on_click=lambda e: on_mood_click(e, "Happy")),
        ft.Container(ft.Text("😁", size=28), width=68, height=68, alignment=ft.alignment.center,
                     border_radius=ft.border_radius.all(34), bgcolor="#FFFFFF", on_click=lambda e: on_mood_click(e, "Excited")),
    ], alignment=ft.MainAxisAlignment.SPACE_AROUND)

    mood_col = ft.Column([
        ft.Text("How are you feeling today", size=20, weight=ft.FontWeight.BOLD, color="#16425B"),
        ft.Container(height=16),
        mood_row,
        ft.Container(height=18),
        ft.Container(
            content=ft.Image(src=ASSET_IMAGE or "https://picsum.photos/160/160", fit=ft.ImageFit.CONTAIN),
            width=140, height=140, border_radius=ft.border_radius.all(80), bgcolor="#FFFFFF"
        )
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    screens[2] = rounded_card(mood_col, width=380, bgcolor="#EAF8FF")

    # Screen 3: Voice / Speak screen
    def on_speak(e):
        page.snack_bar = ft.SnackBar(ft.Text("Speak recording started (demo)"))
        page.snack_bar.open = True
        page.update()

    speak_col = ft.Column([
        ft.Text("Speak", size=24, weight=ft.FontWeight.BOLD, color="#16324A"),
        ft.Container(height=10),
        ft.Container(
            content=ft.Icon(ft.icons.MIC, size=48, color="#FFFFFF"),
            width=120, height=120, border_radius=ft.border_radius.all(60), bgcolor="#1CA3D8", alignment=ft.alignment.center,
            on_click=on_speak
        ),
        ft.Container(height=18),
        ft.Text("Tap to speak and I'll listen. I won't store your voice.", size=14, text_align=ft.TextAlign.CENTER, color="#2E3A59")
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    screens[3] = rounded_card(speak_col, width=380, bgcolor="#DFF8FF")

    # Screen 4: Chat response / encouragement
    response_bubble = ft.Container(
        content=ft.Text("Oh no, that's rough!\nJust remember, when life gives you lemons, you might be dyslexic.",
                        size=14),
        padding=16, border_radius=ft.border_radius.only(20,20,0,20), bgcolor="#FFFFFF", width=320
    )
    resp_col = ft.Column([
        ft.Container(
            content=ft.Image(src=ASSET_IMAGE or "https://picsum.photos/200/200", fit=ft.ImageFit.CONTAIN),
            width=160, height=160, border_radius=ft.border_radius.all(90), bgcolor="#FFFFFF"
        ),
        ft.Container(height=10),
        ft.Text("I had a tough day", size=18, weight=ft.FontWeight.MEDIUM, color="#143A52"),
        ft.Container(height=10),
        response_bubble
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    screens[4] = rounded_card(resp_col, width=380, bgcolor="#EAF1FF")

    # Screen 5: Settings
    def nav_item(title, icon):
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, size=20),
                ft.Container(width=12),
                ft.Text(title, size=16)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=12,
            border_radius=ft.border_radius.all(14),
            bgcolor="#FFFFFF"
        )
    settings_col = ft.Column([
        ft.Text("Settings", size=24, weight=ft.FontWeight.BOLD, color="#16324A"),
        ft.Container(height=18),
        nav_item("Profile", ft.icons.PERSON),
        ft.Container(height=10),
        nav_item("Chat", ft.icons.CHAT_BUBBLE),
        ft.Container(height=10),
        nav_item("Notifications", ft.icons.NOTIFICATIONS),
        ft.Container(height=10),
        nav_item("About", ft.icons.INFO)
    ], horizontal_alignment=ft.CrossAxisAlignment.START)
    screens[5] = rounded_card(settings_col, width=380, bgcolor="#EAF9FF")

    # Container that will hold the currently visible screen
    screen_container = ft.Container(content=screens[0], alignment=ft.alignment.center)

    # Top segmented navigation (6 items to match mockup's 6 screens)
    nav_buttons = []
    nav_labels = ["Welcome", "Buddy", "Mood", "Speak", "Response", "Settings"]
    nav_icons = [ft.icons.HOME, ft.icons.CHAT_BUBBLE, ft.icons.SENTIMENT_SATISFIED, ft.icons.MIC, ft.icons.REPLY, ft.icons.SETTINGS]

    def on_nav_click(e, idx):
        screen_container.content = screens[idx]
        # small animate: reassign the container to trigger UI update
        screen_container.update()
        page.update()

    nav_row = ft.Row(spacing=8, alignment=ft.MainAxisAlignment.SPACE_AROUND)
    for i, (label, icon) in enumerate(zip(nav_labels, nav_icons)):
        btn = ft.Column([
            ft.IconButton(icon=icon, tooltip=label, icon_color="#16425B", on_click=lambda e, idx=i: on_nav_click(e, idx)),
            ft.Text(label, size=10, color="#194d6a")
        ], alignment=ft.MainAxisAlignment.CENTER)
        nav_buttons.append(btn)
        nav_row.controls.append(btn)

    # Page layout: top nav, big center card, bottom spacer
    main_col = ft.Column([
        ft.Container(height=18),
        nav_row,
        ft.Container(height=8),
        screen_container,
        ft.Container(height=18)
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    page.add(ft.Container(content=main_col, alignment=ft.alignment.center, expand=True))

    # small helper to show snack bar for demo
    def open_demo_snack(msg):
        page.snack_bar = ft.SnackBar(ft.Text(msg))
        page.snack_bar.open = True
        page.update()

    # keep the window centered & nice
    page.update()


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
