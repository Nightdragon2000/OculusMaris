import os
import json
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

from core.database.db_setup import setup_database, save_credentials
from gui.gui_components import (
    create_back_button,
    create_section_label,
    create_instruction_label,
    create_ctk_button,
    create_dropdown,
    slide_in_frame,
    slide_out_frame,
    BACKGROUND_COLOR
)

# ---------- Constants ----------
EYE_OPEN_ICON = os.path.join(os.path.dirname(__file__),"..", "assets", "icons", "eye.png")
EYE_CLOSED_ICON = os.path.join(os.path.dirname(__file__),"..", "assets", "icons", "closed_eye.png")


def slide_to_database(self):
    if hasattr(self, "database_frame") and self.database_frame.winfo_exists():
        self.database_frame.destroy()

    self.database_frame = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR, corner_radius=0)
    self.database_frame.place(x=700, y=0, relwidth=1, relheight=1)

    create_back_button(self.database_frame, lambda: back_to_calibration(self)).place(x=20, y=20)
    create_section_label(self.database_frame, "Database Setup", size=22).pack(pady=(60, 10))
    create_instruction_label(self.database_frame, "Please enter the connection details below:").pack(pady=(0, 15))

    engine_wrapper = ctk.CTkFrame(self.database_frame, fg_color="#bbbbbb", corner_radius=6)
    engine_wrapper.pack(pady=(0, 20))

    self.engine_var = ctk.StringVar(value="postgresql")
    engine_dropdown = create_dropdown(
        engine_wrapper,
        values=["postgresql", "mysql"],
        variable=self.engine_var,
        command=lambda _: set_default_fields()
    )
    engine_dropdown.pack(padx=1, pady=1)
    engine_dropdown.set("postgresql")

    form = ctk.CTkFrame(self.database_frame, fg_color=BACKGROUND_COLOR)
    form.pack(pady=(10, 20))

    self.host_entry = create_field(form, "Host:", "localhost")
    self.port_entry = create_field(form, "Port:", "5432")
    self.user_entry = create_field(form, "Username:", "postgres")
    self.pass_entry = create_password_field(form)

    create_ctk_button(self.database_frame, "Create Database and Table", lambda: connect_and_setup(self)).pack(pady=30)

    slide_in_frame(self, self.calibration_frame, self.database_frame)

    def set_default_fields():
        if self.engine_var.get() == "postgresql":
            self.port_entry.delete(0, "end")
            self.port_entry.insert(0, "5432")
            self.user_entry.delete(0, "end")
            self.user_entry.insert(0, "postgres")
        elif self.engine_var.get() == "mysql":
            self.port_entry.delete(0, "end")
            self.port_entry.insert(0, "3306")
            self.user_entry.delete(0, "end")
            self.user_entry.insert(0, "root")


def create_field(parent, label_text, default="", show=None):
    row = ctk.CTkFrame(parent, fg_color=BACKGROUND_COLOR)
    row.pack(fill="x", padx=20, pady=1)

    label = ctk.CTkLabel(row, text=label_text, font=ctk.CTkFont(size=13), width=95, anchor="w")
    label.pack(side="left", padx=(0, 1))

    entry = ctk.CTkEntry(row, width=170, show=show)
    entry.insert(0, default)
    entry.pack(side="left")

    return entry


def create_password_field(parent):
    row = ctk.CTkFrame(parent, fg_color=BACKGROUND_COLOR)
    row.pack(fill="x", padx=20, pady=1)

    label = ctk.CTkLabel(row, text="Password:", font=ctk.CTkFont(size=13), width=95, anchor="w")
    label.pack(side="left", padx=(0, 1))

    entry_var = ctk.StringVar()
    entry = ctk.CTkEntry(row, width=130, textvariable=entry_var, show="*")
    entry.pack(side="left")

    # Load icons as CTkImage
    eye_open_icon = ctk.CTkImage(Image.open(EYE_OPEN_ICON), size=(20, 20))
    eye_closed_icon = ctk.CTkImage(Image.open(EYE_CLOSED_ICON), size=(20, 20))

    def toggle_visibility():
        if entry.cget("show") == "":
            entry.configure(show="*")
            eye_button.configure(image=eye_closed_icon)
        else:
            entry.configure(show="")
            eye_button.configure(image=eye_open_icon)

    eye_button = ctk.CTkButton(
        row,
        width=24,
        height=24,
        image=eye_closed_icon,
        text="",
        command=toggle_visibility,
        fg_color=BACKGROUND_COLOR,
        hover_color=BACKGROUND_COLOR,
        border_width=0
    )
    eye_button.pack(side="left", padx=(5, 0))

    return entry


def connect_and_setup(app):
    config = {
        "engine": app.engine_var.get(),
        "host": app.host_entry.get(),
        "port": app.port_entry.get(),
        "user": app.user_entry.get(),
        "password": app.pass_entry.get(),
        "database": "maritime_tracker"
    }

    success, message = setup_database(config)

    if success:
        save_credentials(config)
        messagebox.showinfo("Success", message)
    else:
        err = message.lower()
        if "no password" in err:
            messagebox.showerror("Missing Password", "Please enter your database password.")
        elif "authentication" in err or "access denied" in err:
            messagebox.showerror("Authentication Error", "Incorrect username or password.")
        elif "could not connect" in err:
            messagebox.showerror("Connection Error", "Cannot connect to the server.")
        else:
            messagebox.showerror("Error", f"Unexpected error:\n{message}")


def back_to_calibration(app):
    if hasattr(app, "database_frame") and app.database_frame.winfo_exists():
        from_frame = app.database_frame
        to_frame = app.calibration_frame

        def cleanup():
            from_frame.destroy()
            del app.database_frame

        slide_out_frame(app, from_frame, to_frame, on_complete=cleanup)
