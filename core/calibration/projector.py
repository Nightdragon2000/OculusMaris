import os
import sys
import json
import ctypes
from ctypes import wintypes
import numpy as np
import pygame
import rasterio
import customtkinter as ctk

# ------- Paths & Setup -------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from gui.gui_components import (
    PRIMARY_COLOR, SECONDARY_COLOR, SECONDARY_HOVER
)

COORDINATES_PATH = os.path.join(PROJECT_ROOT, "data", "json", "coordinates.json")
IMAGE_PATH = os.path.join(PROJECT_ROOT, "data", "images", "georeferenced", "georeferenced_map.tif")


# ------- Popup Windows -------
def show_success(title, msg):
    root = ctk.CTk()
    root.withdraw()
    popup = ctk.CTkToplevel(root)
    popup.title(title)
    popup.geometry("350x150")
    popup.configure(fg_color="white")
    popup.grab_set()

    label = ctk.CTkLabel(popup, text=msg,
                         font=ctk.CTkFont(size=14, weight="bold"),
                         text_color=PRIMARY_COLOR,
                         wraplength=300,
                         justify="center")
    label.pack(padx=20, pady=30)

    popup.update_idletasks()
    x = (popup.winfo_screenwidth() - 350) // 2
    y = (popup.winfo_screenheight() - 150) // 2
    popup.geometry(f"+{x}+{y}")
    popup.after(2500, popup.destroy)
    root.wait_window(popup)
    root.destroy()


def show_error(title, msg):
    root = ctk.CTk()
    root.withdraw()
    popup = ctk.CTkToplevel(root)
    popup.title(title)
    popup.geometry("370x180")
    popup.configure(fg_color="white")
    popup.grab_set()

    label = ctk.CTkLabel(popup, text=msg,
                         font=ctk.CTkFont(size=14, weight="bold"),
                         text_color="red",
                         wraplength=320,
                         justify="center")
    label.pack(padx=20, pady=25)

    button = ctk.CTkButton(popup, text="OK",
                           command=popup.destroy,
                           font=ctk.CTkFont(size=13),
                           fg_color=SECONDARY_COLOR,
                           hover_color=SECONDARY_HOVER,
                           text_color=PRIMARY_COLOR,
                           width=100, height=30,
                           corner_radius=6)
    button.pack(pady=(0, 15))

    popup.update_idletasks()
    x = (popup.winfo_screenwidth() - 370) // 2
    y = (popup.winfo_screenheight() - 180) // 2
    popup.geometry(f"+{x}+{y}")
    popup.after(2500, popup.destroy)
    root.wait_window(popup)
    root.destroy()


# ------- Save Coordinates -------
def save_coordinates_to_json(projector_coordinatess=None):
    data = {}
    if os.path.exists(COORDINATES_PATH):
        try:
            with open(COORDINATES_PATH, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print("Warning: JSON file is empty or corrupted.")

    if projector_coordinatess:
        data['projector'] = projector_coordinatess

    with open(COORDINATES_PATH, 'w') as f:
        json.dump(data, f, indent=2)
    print("Projector coordinates saved.")


# ------- Move Window to Monitor -------
def move_window_to_monitor(monitor_index):
    hwnd = pygame.display.get_wm_info()['window']
    user32 = ctypes.windll.user32

    monitors = []

    def _monitor_enum(hMonitor, hdcMonitor, lprcMonitor, dwData):
        r = lprcMonitor.contents
        monitors.append((r.left, r.top, r.right - r.left, r.bottom - r.top))
        return 1

    MONITORENUMPROC = ctypes.WINFUNCTYPE(
        ctypes.c_int, wintypes.HMONITOR, wintypes.HDC,
        ctypes.POINTER(wintypes.RECT), ctypes.c_double
    )
    user32.EnumDisplayMonitors(0, 0, MONITORENUMPROC(_monitor_enum), 0)

    if not monitors:
        return
    if monitor_index < 0 or monitor_index >= len(monitors):
        monitor_index = 0

    left, top, width, height = monitors[monitor_index]
    user32.MoveWindow(hwnd, left, top, width, height, True)


# ------- Calibration Logic -------
def projector_calibration():
    try:
        with rasterio.open(IMAGE_PATH) as src:
            raw = src.read()
    except Exception as e:
        show_error("Error", f"Failed to load georeferenced image:\n{e}")
        return

    image_data = np.transpose(raw[:3], (1, 2, 0)).astype(np.uint8)
    image_data = np.flipud(np.rot90(image_data, 3))
    image_data = np.fliplr(image_data)
    image_data = np.flipud(image_data)

    pygame.init()
    monitor_index = int(os.environ.get("SDL_VIDEO_FULLSCREEN_DISPLAY", "0"))
    os.environ["SDL_VIDEO_FULLSCREEN_DISPLAY"] = str(monitor_index)

    screen_width, screen_height = pygame.display.get_desktop_sizes()[monitor_index]
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)

    if sys.platform.startswith("win"):
        move_window_to_monitor(monitor_index)

    original = pygame.surfarray.make_surface(image_data)
    image_surface = original.copy()
    image_x = image_y = 0
    scale_factor = 1.0
    min_scale, max_scale = 0.1, 5.0
    scroll_step = 0.005
    dragging = False
    offset_x = offset_y = 0
    save = False

    def scale_image(surf, scale):
        w, h = surf.get_width(), surf.get_height()
        return pygame.transform.scale(surf, (int(w * scale), int(h * scale)))

    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
                save = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN:
                    running = False
                    save = True
                elif ev.key == pygame.K_ESCAPE:
                    running = False
                    save = False

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                dragging = True
                mx, my = ev.pos
                offset_x = image_x - mx
                offset_y = image_y - my
            elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                dragging = False
            elif ev.type == pygame.MOUSEMOTION and dragging:
                mx, my = ev.pos
                image_x = mx + offset_x
                image_y = my + offset_y

            if ev.type == pygame.MOUSEWHEEL:
                scale_factor = min(max_scale, max(min_scale, scale_factor + scroll_step * ev.y))
                image_surface = scale_image(original, scale_factor)

            if ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 4:
                    scale_factor = min(max_scale, scale_factor + scroll_step)
                    image_surface = scale_image(original, scale_factor)
                elif ev.button == 5:
                    scale_factor = max(min_scale, scale_factor - scroll_step)
                    image_surface = scale_image(original, scale_factor)

        screen.fill((0, 0, 0))
        screen.blit(image_surface, (image_x, image_y))
        pygame.display.flip()

    pygame.quit()

    if save:
        tl = (image_x, image_y)
        br = (image_x + image_surface.get_width(), image_y + image_surface.get_height())
        save_coordinates_to_json(projector_coordinatess={"tl_corner": tl, "br_corner": br})
        show_success("Success", "Projector calibration saved.")



# ------- Entry Point -------
if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    projector_calibration()
