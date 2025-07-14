import os
import sys
import customtkinter as ctk
import subprocess
from tkinter import messagebox

from gui.monitor_selector import select_monitor
from gui.gui_components import (
    create_ctk_button,
    create_section_label,
    create_back_button,
    create_instruction_label,
    slide_in_frame,
    slide_out_frame,
    BACKGROUND_COLOR
)

# ---------- Constants ----------
PROJECTOR_SCRIPT = os.path.join(os.path.dirname(__file__),"..", "core", "calibration", "projector.py")


def slide_to_projector_calibration(self):
    # Destroy previous frame if exists
    if hasattr(self, "projector_frame") and self.projector_frame.winfo_exists():
        self.projector_frame.destroy()

    self.projector_frame = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR, corner_radius=0)
    self.projector_frame.place(x=700, y=0, relwidth=1, relheight=1)

    # Back Button
    create_back_button(self.projector_frame, lambda: back_to_calibration(self)).place(x=20, y=20)

    # Title
    create_section_label(self.projector_frame, "Projector Calibration", size=22).pack(pady=(60, 20))

    # Instructions
    instructions = (
        "\u2022 Select a GeoTIFF image when prompted.\n"
        "\u2022 The image will be projected full-screen.\n"
        "\u2022 Use mouse wheel to zoom in/out.\n"
        "\u2022 Drag the image to reposition.\n"
        "\u2022 Press [Enter] to save position/size.\n"
        "\u2022 Press [Esc] to cancel calibration."
    )
    create_instruction_label(self.projector_frame, instructions).pack(padx=30, pady=10)

    # Start Button
    create_ctk_button(self.projector_frame, "Start Projector Calibration", run_projector_script).pack(pady=(20, 5))

    # Animate
    slide_in_frame(self, self.calibration_frame, self.projector_frame)


def back_to_calibration(app):
    if hasattr(app, "projector_frame") and app.projector_frame.winfo_exists():
        from_frame = app.projector_frame
        to_frame = app.calibration_frame

        def cleanup():
            from_frame.destroy()
            del app.projector_frame

        slide_out_frame(app, from_frame, to_frame, on_complete=cleanup)


def run_projector_script():
    def on_monitor_selected(monitor_index):
        try:
            if not os.path.exists(PROJECTOR_SCRIPT):
                raise FileNotFoundError(f"{PROJECTOR_SCRIPT} does not exist.")

            env = os.environ.copy()
            env["SDL_VIDEO_FULLSCREEN_DISPLAY"] = str(monitor_index)

            subprocess.run([sys.executable, PROJECTOR_SCRIPT], env=env)

        except Exception as e:
            messagebox.showerror("Error", f"Could not run projector calibration:\n{e}")

    select_monitor(on_monitor_selected)