import customtkinter as ctk
from tkinter import StringVar
from screeninfo import get_monitors
from gui.gui_components import (
    create_section_label,
    create_ctk_button,
    create_dropdown,
    BACKGROUND_COLOR
)


def select_monitor(callback):
    # Get monitor info
    try:
        monitors = get_monitors()
    except Exception:
        monitors = []

    if not monitors:
        monitors = [type("Monitor", (), {"width": 800, "height": 600})()]

    monitor_names = [
        f"Monitor {i + 1} ({m.width}×{m.height})"
        for i, m in enumerate(monitors)
    ]

    # --- Modal Window ---
    root = ctk.CTkToplevel()
    root.title("Select Display Monitor")
    root.geometry("440x260")
    root.resizable(False, False)
    root.configure(fg_color=BACKGROUND_COLOR)
    root.attributes("-topmost", True)
    root.attributes("-alpha", 0.0)

    # Fade In Animation
    def fade_in(alpha=0.0):
        alpha += 0.05
        if alpha <= 1.0:
            root.attributes("-alpha", alpha)
            root.after(15, lambda: fade_in(alpha))
    fade_in()

    # --- Title ---
    create_section_label(root, "Choose a Monitor", size=20).pack(pady=(30, 15))

    # --- Dropdown inside border frame ---
    monitor_var = StringVar(value=monitor_names[0])
    dropdown_wrapper = ctk.CTkFrame(root, fg_color="#bbbbbb", corner_radius=6)
    dropdown_wrapper.pack(pady=(0, 10))

    dropdown = create_dropdown(
        dropdown_wrapper,
        values=monitor_names,
        variable=monitor_var
    )
    dropdown.pack(padx=1, pady=1)
    dropdown.set(monitor_names[0])

    # --- Separator Line ---
    ctk.CTkFrame(root, height=1, fg_color="#dddddd").pack(fill="x", padx=30, pady=(10, 15))

    # --- Confirm Button ---
    def confirm_and_close():
        fade_out_and_submit(monitor_names.index(monitor_var.get()))

    def fade_out_and_submit(value):
        def fade(alpha=1.0):
            alpha -= 0.05
            if alpha > 0.0:
                root.attributes("-alpha", alpha)
                root.after(15, lambda: fade(alpha))
            else:
                root.destroy()
                callback(value)
        fade()

    create_ctk_button(root, "Confirm", confirm_and_close).pack(pady=(5, 15))
    root.grab_set()  # Modal behavior
