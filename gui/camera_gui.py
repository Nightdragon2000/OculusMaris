import os
import sys
import subprocess
import customtkinter as ctk

from gui.gui_components import (
    create_ctk_button,
    create_section_label,
    create_back_button,
    create_instruction_label,
    slide_in_frame,
    BACKGROUND_COLOR
)

# --------- Paths ---------
CAMERA_SCRIPT = os.path.join(os.path.dirname(__file__),"..", "core", "calibration", "camera.py")


def slide_to_camera_calibration(self):
    # Always recreate frame
    if hasattr(self, "camera_frame") and self.camera_frame.winfo_exists():
        self.camera_frame.destroy()

    self.camera_frame = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR, corner_radius=0)
    self.camera_frame.place(x=700, y=0, relwidth=1, relheight=1)

    # Back Button
    create_back_button(self.camera_frame, lambda: back_to_calibration(self)).place(x=20, y=20)

    # Title
    create_section_label(self.camera_frame, "Camera Calibration", size=22).pack(pady=(60, 20))

    # Instructions
    instructions = (
        "\u2022 Make sure your camera is connected.\n"
        "\u2022 A blue rectangle will appear on screen.\n"
        "\u2022 Adjust it by dragging the corners.\n"
        "\u2022 Press [Enter] to save or [Esc] to cancel."
    )
    create_instruction_label(self.camera_frame, instructions).pack(padx=30, pady=10)

    # Start Button
    create_ctk_button(self.camera_frame, "Start Camera Calibration", run_camera_script).pack(pady=(20, 5))

    # Animate
    slide_in_frame(self, self.calibration_frame, self.camera_frame)


def back_to_calibration(app):
    if hasattr(app, "camera_frame") and app.camera_frame.winfo_exists():
        from_frame = app.camera_frame
        to_frame = app.calibration_frame

        def cleanup():
            from_frame.destroy()
            del app.camera_frame

        from gui.gui_components import slide_out_frame
        slide_out_frame(app, from_frame, to_frame, on_complete=cleanup)



def run_camera_script():
    try:
        subprocess.run([sys.executable, CAMERA_SCRIPT])
    except Exception as e:
        from tkinter import messagebox
        messagebox.showerror("Error", f"Could not run camera calibration:\n{e}")
