import customtkinter as ctk
from gui.gui_components import (
    slide_in_frame,
    create_ctk_button,
    create_section_label,
    create_back_button,
    create_note_box,
    BACKGROUND_COLOR
)

def slide_to_calibration(self):
    self.calibration_frame = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR, corner_radius=0)
    self.calibration_frame.place(x=700, y=0, relwidth=1, relheight=1)

    # Back Button
    create_back_button(self.calibration_frame, self.slide_back_to_main).place(x=20, y=20)

    # Title
    create_section_label(self.calibration_frame, "Setup & Calibration", size=22).pack(pady=(60, 20))

    # Option Buttons
    options = [
        ("Setup Database", self.setup_database),
        ("Georeference Image", self.georeference_image),
        ("Camera Calibration", self.camera_calibration),
        ("Projector Calibration", self.projector_calibration),
    ]
    for text, command in options:
        create_ctk_button(self.calibration_frame, text, command, width=240, height=40, font_size=15).pack(pady=8)

    # Tip/Note Box
    tip = (
        "Tip: \n\n If this is your first time running the program,\n"
        "please complete all the above steps in order."
    )
    create_note_box(self.calibration_frame, tip).pack(pady=(30, 10), fill="none")

    # Animate
    slide_in_frame(self, self.main_frame, self.calibration_frame)
