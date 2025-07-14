import os
import sys
import subprocess
import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
from serial.tools import list_ports
import webbrowser

from gui.monitor_selector import select_monitor
from gui.gui_components import (
    PRIMARY_COLOR, HOVER_COLOR, SECONDARY_COLOR, SECONDARY_HOVER,
    TEXT_COLOR, BACKGROUND_COLOR,
    slide_in_frame, slide_out_frame,
    create_section_label, create_ctk_button,
    create_help_button
)


DISPLAY_SCRIPT = os.path.join(os.path.dirname(__file__), "..","core", "interactive", "display.py")
AIS_SCRIPT = os.path.join(os.path.dirname(__file__),"..", "core", "ais", "ais_receiver.py")

LOGO_IMAGE = os.path.join(os.path.dirname(__file__),"..", "assets", "logos", "logo.png")
ICON_PATH = os.path.join(os.path.dirname(__file__),"..", "assets", "logos", "logo.ico")


class StartWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Oculus Maris")
        self.center_window(550, 500)
        self.resizable(False, False)
        self.configure(fg_color=BACKGROUND_COLOR)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.logo_img = self.load_logo(LOGO_IMAGE)
        self.set_window_icon(ICON_PATH)

        self.main_frame = None
        self.calibration_frame = None
        self.build_main_frame()

    def center_window(self, width, height):
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = int((screen_w - width) / 2)
        y = int((screen_h - height) / 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def set_window_icon(self, path):
        try:
            self.iconbitmap(default=path)
        except Exception as e:
            print(f"Failed to set window icon: {e}")

    def load_logo(self, path):
        img = Image.open(path)
        return ctk.CTkImage(light_image=img, size=(187,131))

    def build_main_frame(self):
        if self.calibration_frame:
            self.calibration_frame.place_forget()

        self.main_frame = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR, corner_radius=0)
        self.main_frame.place(x=0, y=0, relwidth=1, relheight=1)

        ctk.CTkLabel(self.main_frame, image=self.logo_img, text="").pack(pady=(0, 0))
        create_section_label(self.main_frame, "Oculus Maris").pack(pady=(0, 5))

        ctk.CTkLabel(self.main_frame,
                     text="An Experimental System for Real-Time Geospatial Interaction",
                     font=ctk.CTkFont(size=14),
                     text_color=TEXT_COLOR,
                     wraplength=600,
                     justify="center").pack(pady=(0, 30))

        btn_frame = ctk.CTkFrame(self.main_frame, fg_color=BACKGROUND_COLOR)
        btn_frame.pack(pady=10)

        create_ctk_button(btn_frame, "Run Main Application", self.run_main_app).pack(side="left", padx=15)
        create_ctk_button(btn_frame, "Setup & Calibration", self.slide_to_calibration).pack(side="left", padx=15)

        create_help_button(self.main_frame, self.show_help).pack(pady=(25, 5))

        ctk.CTkLabel(self.main_frame,
                     text="Developed by Afroditi Kalantzi ",
                     font=ctk.CTkFont(size=11, slant="italic"),
                     text_color=TEXT_COLOR).pack(pady=(30, 0))

        github_link = ctk.CTkLabel(self.main_frame,
                                   text="See More on GitHub",
                                   text_color=PRIMARY_COLOR,
                                   cursor="hand2",
                                   font=ctk.CTkFont(size=11, underline=True))
        github_link.pack(pady=(0, 0))
        github_link.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/Nightdragon2000"))

    def slide_to_calibration(self):
        from gui.calibration_gui import slide_to_calibration
        slide_to_calibration(self)

    def slide_back_to_main(self):
        slide_out_frame(self, self.calibration_frame, self.main_frame)

    def is_ais_receiver_connected(self):
        ports = list_ports.comports()
        return any("AIS" in (port.description or "") or "USB" in (port.description or "") for port in ports)


    def run_main_app(self):
        def show_info_popup(title, message):
            popup = ctk.CTkToplevel(self)
            popup.title(title)
            popup.configure(fg_color=BACKGROUND_COLOR)
            popup.geometry("400x180")
            try:
                popup.iconbitmap(ICON_PATH)
            except:
                pass

            popup.grab_set()
            popup.update_idletasks()
            x = (popup.winfo_screenwidth() // 2) - 200
            y = (popup.winfo_screenheight() // 2) - 90
            popup.geometry(f"+{x}+{y}")

            ctk.CTkLabel(popup,
                        text=message,
                        font=ctk.CTkFont(size=15),
                        text_color=TEXT_COLOR,
                        wraplength=360,
                        justify="center").pack(padx=20, pady=(30, 10))

            popup.after(2000, popup.destroy)
            popup.wait_window()

        def show_yesno_popup(title, message):
            result = {"value": False}

            popup = ctk.CTkToplevel(self)
            popup.title(title)
            popup.configure(fg_color=BACKGROUND_COLOR)
            popup.geometry("420x200")
            try:
                popup.iconbitmap(ICON_PATH)
            except:
                pass

            popup.grab_set()
            popup.update_idletasks()
            x = (popup.winfo_screenwidth() // 2) - 210
            y = (popup.winfo_screenheight() // 2) - 100
            popup.geometry(f"+{x}+{y}")

            ctk.CTkLabel(popup,
                        text=message,
                        font=ctk.CTkFont(size=15),
                        text_color=TEXT_COLOR,
                        wraplength=380,
                        justify="center").pack(padx=20, pady=(30, 20))

            btn_frame = ctk.CTkFrame(popup, fg_color=BACKGROUND_COLOR)
            btn_frame.pack(pady=10)

            def choose(val):
                result["value"] = val
                popup.destroy()

            ctk.CTkButton(btn_frame,
                        text="Yes",
                        command=lambda: choose(True),
                        fg_color=PRIMARY_COLOR,
                        hover_color=HOVER_COLOR,
                        width=120,
                        corner_radius=10).pack(side="left", padx=15)

            ctk.CTkButton(btn_frame,
                        text="No",
                        command=lambda: choose(False),
                        fg_color=SECONDARY_COLOR,
                        hover_color=SECONDARY_HOVER,
                        text_color=PRIMARY_COLOR,
                        width=120,
                        corner_radius=10).pack(side="left", padx=15)

            popup.wait_window()
            return result["value"]

        def on_monitor_selected(monitor_index):
            

            env = os.environ.copy()
            env["SDL_VIDEO_FULLSCREEN_DISPLAY"] = str(monitor_index)

            self.decode_proc = None

            if self.is_ais_receiver_connected():
                try:
                    show_info_popup("Running with AIS", "Launching full system...")
                    self.decode_proc = subprocess.Popen([sys.executable, AIS_SCRIPT],
                                                    creationflags=subprocess.CREATE_NEW_CONSOLE)
                    self.main_proc = subprocess.Popen([sys.executable, DISPLAY_SCRIPT], env=env)
                except Exception as e:
                    show_info_popup("Launch Error", str(e))
                    return
            else:
                if not show_yesno_popup("AIS Not Found", "No AIS receiver found. Continue anyway?"):
                    return
                try:
                    self.main_proc = subprocess.Popen([sys.executable, DISPLAY_SCRIPT], env=env)
                except Exception as e:
                    show_info_popup("Launch Error", str(e))
                    return

            self.destroy()
            self.main_proc.wait()
            if self.decode_proc:
                self.decode_proc.terminate()
                self.decode_proc.wait()

        select_monitor(on_monitor_selected)



    def setup_database(self):
        from gui.database_gui import slide_to_database
        slide_to_database(self)

    def camera_calibration(self):
        from gui.camera_gui import slide_to_camera_calibration
        slide_to_camera_calibration(self)

    def projector_calibration(self):
        from gui.projector_gui import slide_to_projector_calibration
        slide_to_projector_calibration(self)

    def georeference_image(self):
        from gui.georeference_gui import slide_to_georeference
        slide_to_georeference(self)

    def show_help(self):
        help_win = ctk.CTkToplevel(self)
        help_win.title("Help")
        help_win.configure(fg_color=BACKGROUND_COLOR)
        help_win.geometry("500x420")
        help_win.resizable(False, False)

        # Set icon
        try:
            help_win.iconbitmap(ICON_PATH)
        except Exception as e:
            print("Failed to set icon:", e)

        # Center the window
        help_win.update_idletasks()
        screen_w = help_win.winfo_screenwidth()
        screen_h = help_win.winfo_screenheight()
        x = int((screen_w - 500) / 2)
        y = int((screen_h - 420) / 2)
        help_win.geometry(f"+{x}+{y}")

        # Make it modal
        help_win.grab_set()

        # Title label
        ctk.CTkLabel(
            help_win,
            text="System Guide",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=PRIMARY_COLOR,
            wraplength=460,
            justify="center"
        ).pack(pady=(20, 20), padx=20)

        # Updated instruction text
        help_text = (
            "Setup & Calibration:\n\n"
            "\u2022 Set up PostgreSQL or MySQL database\n"
            "\u2022 Calibrate projection and camera alignment\n"
            "\u2022 Insert real-world coordinates into the digital map\n\n"
            "Main Application Features:\n\n"
            "\u2022 Visualizes AIS maritime traffic on a 3D maquette\n"
            "\u2022 Enables gesture-based selection using hand tracking\n"
            "\u2022 To select a ship: hover your finger over its position for 2 seconds\n"
            "\u2022 Pinch (index + thumb) to deselect a ship\n"
            "\u2022 Displays ship name, destination, ETA, and navigation status\n"
            "\u2022 Recommended: Enable AIS receiver for live ship data\n\n"
            "\u2022 Press ESC anytime to close the app"
    )

        ctk.CTkLabel(
            help_win,
            text=help_text,
            font=ctk.CTkFont(size=14),
            text_color=TEXT_COLOR,
            wraplength=460,
            justify="left"
        ).pack(padx=30, pady=(0, 20))

        # OK Button
        ctk.CTkButton(
            help_win,
            text="OK",
            command=help_win.destroy,
            font=ctk.CTkFont(size=13),
            fg_color=SECONDARY_COLOR,
            hover_color=SECONDARY_HOVER,
            text_color=PRIMARY_COLOR,
            corner_radius=8,
            width=100,
            height=35
        ).pack(pady=(0, 20))

   

def launch_start_window():
    app = StartWindow()
    app.mainloop()
