import os
import customtkinter as ctk
from PIL import Image
import threading
import winsound

from gui.gui_components import PRIMARY_COLOR

LOGO_IMAGE = os.path.join(os.path.dirname(__file__),"..", "assets", "logos", "logo_with_text.png")

class SplashScreen(ctk.CTk):
    def __init__(self, on_close_callback):
        super().__init__()

        self.on_close_callback = on_close_callback
        self.opacity = 0.0
        self.progress_value = 0.0

        self.width = 500
        self.height = 450
        self.geometry_centered(self.width, self.height)
        self.overrideredirect(True)
        self.configure(fg_color="white")
        self.attributes("-alpha", self.opacity)

        self.build_ui()
        self.fade_in()

        threading.Thread(target=self.play_sound, daemon=True).start()
        self.animate_progress()

    def build_ui(self):
        # Logo
        try:
            img = Image.open(LOGO_IMAGE)
            self.logo_img = ctk.CTkImage(light_image=img, size=(300, 300))
            ctk.CTkLabel(self, image=self.logo_img, text="").pack(pady=(20, 5))
        except:
            pass

        # Version label 
        ctk.CTkLabel(self,
                     text="Version 2.0",
                     font=ctk.CTkFont(size=13),
                     text_color=PRIMARY_COLOR).pack()

        # Progress bar
        self.progressbar = ctk.CTkProgressBar(self, width=200)
        self.progressbar.pack(pady=(20, 0))
        self.progressbar.set(0)

    def geometry_centered(self, w, h):
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = int((screen_w - w) / 2)
        y = int((screen_h - h) / 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def animate_progress(self):
        if self.progress_value < 1.0:
            self.progress_value += 0.02
            self.progressbar.set(self.progress_value)
            self.after(70, self.animate_progress)
        else:
            self.after(300, self.fade_out)  # small delay before fading

    def fade_in(self):
        if self.opacity < 1.0:
            self.opacity += 0.05
            self.attributes("-alpha", self.opacity)
            self.after(30, self.fade_in)

    def fade_out(self):
        if self.opacity > 0:
            self.opacity -= 0.05
            self.attributes("-alpha", self.opacity)
            self.after(30, self.fade_out)
        else:
            self.destroy()
            self.on_close_callback()

    def play_sound(self):
        try:
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
        except:
            pass
