import os
import sys
import customtkinter as ctk
import subprocess
from tkinter import messagebox

from gui.gui_components import (
    create_ctk_button,
    create_section_label,
    create_back_button,
    create_instruction_label,
    create_note_box,
    slide_in_frame,
    slide_out_frame,
    BACKGROUND_COLOR
)

# ---------- Constants ----------
GEOREF_SCRIPT = os.path.join(os.path.dirname(__file__),"..", "core", "georeference", "app.py")


def slide_to_georeference(self):
    # Destroy previous frame if exists
    if hasattr(self, "georef_frame") and self.georef_frame.winfo_exists():
        self.georef_frame.destroy()

    self.georef_frame = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR, corner_radius=0)
    self.georef_frame.place(x=700, y=0, relwidth=1, relheight=1)

    # Back Button
    create_back_button(self.georef_frame, lambda: back_to_calibration(self)).place(x=20, y=20)

    # Title
    create_section_label(self.georef_frame, "Georeference Image", size=22).pack(pady=(60, 20))

    # Instructions
    instructions = (
        "\u2022 Select an image .\n"
        "\u2022 Click on 4 points and enter real coordinates (lat, lon).\n"
        "\u2022 Click to edit/delete points.\n"
        "\u2022 Right-click drag to move the image.\n"
        "\u2022 Zoom using mouse wheel.\n"
        "\u2022 After 4 points, the GeoTIFF is saved automatically."
    )
    create_instruction_label(self.georef_frame, instructions).pack(padx=30, pady=10)

    # Start Button
    create_ctk_button(self.georef_frame, "Start Georeferencing Tool", run_georeference_script).pack(pady=(20, 10))


    # Animate
    slide_in_frame(self, self.calibration_frame, self.georef_frame)


def back_to_calibration(app):
    if hasattr(app, "georef_frame") and app.georef_frame.winfo_exists():
        from_frame = app.georef_frame
        to_frame = app.calibration_frame

        def cleanup():
            from_frame.destroy()
            del app.georef_frame

        slide_out_frame(app, from_frame, to_frame, on_complete=cleanup)


def run_georeference_script():
    try:
        if not os.path.exists(GEOREF_SCRIPT):
            messagebox.showerror("Error", f"{GEOREF_SCRIPT} does not exist.")
            return

        subprocess.run([sys.executable, GEOREF_SCRIPT])

    except Exception as e:
        messagebox.showerror("Error", f"Could not run georeferencing tool:\n{e}")
