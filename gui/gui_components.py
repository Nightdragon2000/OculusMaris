import customtkinter as ctk

# ---------- Unified Color Palette ----------
PRIMARY_COLOR = "#007C84"
HOVER_COLOR = "#005F63"
SECONDARY_COLOR = "#f0f0f0"
SECONDARY_HOVER = "#d8f4f3"
TEXT_COLOR = "#444444"
INFO_BG = "#d9edf7"
INFO_TEXT = "#31708f"
GITHUB_DARK = "#24292e"
GITHUB_HOVER = "#444c56"
BACKGROUND_COLOR = "white"

# ---------- CTk: Back Button ----------
def create_back_button(parent, command, width=80, height=30):
    return ctk.CTkButton(parent,
                         text="← Back",
                         font=ctk.CTkFont(size=13),
                         command=command,
                         fg_color=SECONDARY_COLOR,
                         hover_color=SECONDARY_HOVER,
                         text_color=PRIMARY_COLOR,
                         corner_radius=8,
                         width=width,
                         height=height)

# ---------- CTk: Primary Button ----------
def create_ctk_button(parent, text, command, width=200, height=45, font_size=16):
    return ctk.CTkButton(parent,
                         text=text,
                         font=ctk.CTkFont(size=font_size),
                         command=command,
                         fg_color=PRIMARY_COLOR,
                         hover_color=HOVER_COLOR,
                         corner_radius=12,
                         width=width,
                         height=height)

# ---------- CTk: Small CTA Button ----------
def create_small_cta_button(parent, text, command, width=140, height=28, font_size=12):
    return ctk.CTkButton(parent,
                         text=text,
                         font=ctk.CTkFont(size=font_size, weight="bold"),
                         command=command,
                         fg_color=GITHUB_DARK,
                         hover_color=GITHUB_HOVER,
                         text_color="white",
                         corner_radius=6,
                         width=width,
                         height=height)

# ---------- CTk: Help Button ----------
def create_help_button(parent, command, text="Need Help?"):
    return ctk.CTkButton(parent,
                         text=text,
                         font=ctk.CTkFont(size=13),
                         fg_color=SECONDARY_COLOR,
                         text_color=PRIMARY_COLOR,
                         hover_color=SECONDARY_HOVER,
                         corner_radius=10,
                         command=command,
                         width=120)

# ---------- CTk: Note Box  ----------
def create_note_box(parent, message, wrap=480):
    box = ctk.CTkFrame(parent, fg_color=INFO_BG, corner_radius=10)
    label = ctk.CTkLabel(box,
                         text=message,
                         font=ctk.CTkFont(size=11, slant="italic"),
                         text_color=INFO_TEXT,
                         wraplength=wrap,
                         justify="center")
    label.pack(padx=20, pady=15)
    return box

# ---------- CTk: Clean Instruction Label ----------
def create_instruction_label(parent, message, wrap=480):
    return ctk.CTkLabel(parent,
                        text=message,
                        font=ctk.CTkFont(size=15),
                        text_color=TEXT_COLOR,
                        wraplength=wrap,
                        justify="left",
                        anchor="w")

# ---------- CTk: Styled Dropdown (OptionMenu) ----------
def create_dropdown(parent, values, variable, command=None, width=260, height=36):
    return ctk.CTkOptionMenu(
        parent,
        values=values,
        variable=variable,
        command=command,
        width=width,
        height=height,
        fg_color="#ffffff",
        button_color=PRIMARY_COLOR,
        button_hover_color=HOVER_COLOR,
        dropdown_fg_color="#ffffff",
        dropdown_hover_color="#e6f2f3",
        dropdown_text_color="#222222",
        text_color="#000000",
        font=ctk.CTkFont(size=14),
        dropdown_font=ctk.CTkFont(size=13),
        corner_radius=4
    )


# ---------- CTk: Section Title ----------
def create_section_label(parent, text, size=26):
    return ctk.CTkLabel(parent,
                        text=text,
                        font=ctk.CTkFont(size=size, weight="bold"),
                        text_color=PRIMARY_COLOR)

# ---------- CTk: Slide In ----------
def slide_in_frame(app, from_frame, to_frame, duration=10, step=20):
    from_x = 0
    to_x = app.winfo_width()
    to_frame.place(x=to_x, y=0, relwidth=1, relheight=1)

    def slide(x):
        from_frame.place(x=x, y=0)
        to_frame.place(x=x + app.winfo_width(), y=0)
        if x > -app.winfo_width():
            app.after(duration, lambda: slide(x - step))
        else:
            from_frame.place_forget()
            to_frame.place(x=0, y=0, relwidth=1, relheight=1)

    slide(from_x)

# ---------- CTk: Slide Out ----------
def slide_out_frame(app, from_frame, to_frame, duration=10, step=20, on_complete=None):
    from_x = 0
    to_x = -app.winfo_width()
    to_frame.place(x=to_x, y=0, relwidth=1, relheight=1)

    def slide(x):
        try:
            from_frame.place(x=x, y=0)
            to_frame.place(x=x - app.winfo_width(), y=0)
            if x < app.winfo_width():
                app.after(duration, lambda: slide(x + step))
            else:
                from_frame.place_forget()
                to_frame.place(x=0, y=0, relwidth=1, relheight=1)
                if on_complete:
                    on_complete()
        except Exception:
            pass  # in case frame is destroyed early

    slide(from_x)
