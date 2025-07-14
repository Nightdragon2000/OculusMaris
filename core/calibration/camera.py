import os
import sys
import json
import cv2
import customtkinter as ctk

# ------- Paths & Setup -------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from gui.gui_components import (
    PRIMARY_COLOR, SECONDARY_COLOR, SECONDARY_HOVER
)

COORDINATES_PATH = os.path.join(PROJECT_ROOT, "data", "json", "coordinates.json")

# ------- Rectangle State -------
rectangle_top_left_corner = (100, 100)
rectangle_bottom_right_corner = (300, 300)
dragging_corner = None
offset_x, offset_y = 0, 0

# ------- Popups -------
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
    screen_w = popup.winfo_screenwidth()
    screen_h = popup.winfo_screenheight()
    x = (screen_w - 350) // 2
    y = (screen_h - 150) // 2
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
    screen_w = popup.winfo_screenwidth()
    screen_h = popup.winfo_screenheight()
    x = (screen_w - 370) // 2
    y = (screen_h - 180) // 2
    popup.geometry(f"+{x}+{y}")
    popup.after(2500, popup.destroy)
    root.wait_window(popup)
    root.destroy()

# ------- JSON Save -------
def save_coordinates(camera_coordinates=None):
    data = {}
    if os.path.exists(COORDINATES_PATH):
        try:
            with open(COORDINATES_PATH, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print("Warning: coordinates.json is empty or invalid.")

    if camera_coordinates:
        data["camera"] = camera_coordinates

    with open(COORDINATES_PATH, 'w') as f:
        json.dump(data, f, indent=4)
    print("Camera coordinates saved.")

# ------- Mouse Interaction -------
def select_rectangle(event, x, y, flags, param):
    global rectangle_top_left_corner, rectangle_bottom_right_corner
    global dragging_corner, offset_x, offset_y

    if event == cv2.EVENT_LBUTTONDOWN:
        if abs(x - rectangle_top_left_corner[0]) < 10 and abs(y - rectangle_top_left_corner[1]) < 10:
            dragging_corner = "start"
        elif abs(x - rectangle_bottom_right_corner[0]) < 10 and abs(y - rectangle_bottom_right_corner[1]) < 10:
            dragging_corner = "end"
        elif rectangle_top_left_corner[0] < x < rectangle_bottom_right_corner[0] and \
             rectangle_top_left_corner[1] < y < rectangle_bottom_right_corner[1]:
            dragging_corner = "move"
            offset_x = x - rectangle_top_left_corner[0]
            offset_y = y - rectangle_top_left_corner[1]
        else:
            dragging_corner = None

    elif event == cv2.EVENT_MOUSEMOVE:
        if dragging_corner == "start":
            rectangle_top_left_corner = (x, y)
        elif dragging_corner == "end":
            rectangle_bottom_right_corner = (x, y)
        elif dragging_corner == "move":
            width = rectangle_bottom_right_corner[0] - rectangle_top_left_corner[0]
            height = rectangle_bottom_right_corner[1] - rectangle_top_left_corner[1]
            rectangle_top_left_corner = (x - offset_x, y - offset_y)
            rectangle_bottom_right_corner = (
                rectangle_top_left_corner[0] + width,
                rectangle_top_left_corner[1] + height
            )

    elif event == cv2.EVENT_LBUTTONUP:
        dragging_corner = None

# ------- Main Logic -------
def camera_calibration():
    global rectangle_top_left_corner, rectangle_bottom_right_corner

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        show_error("Error", "No camera detected.")
        return

    cv2.namedWindow("Camera Calibration")
    cv2.setMouseCallback("Camera Calibration", select_rectangle)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        cv2.rectangle(frame, rectangle_top_left_corner, rectangle_bottom_right_corner, (255, 0, 0), 2)
        cv2.circle(frame, rectangle_top_left_corner, 5, (0, 0, 255), -1)
        cv2.circle(frame, rectangle_bottom_right_corner, 5, (0, 0, 255), -1)

        cv2.imshow("Camera Calibration", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 13:  # ENTER
            tl = rectangle_top_left_corner
            br = rectangle_bottom_right_corner
            tl_corrected = (min(tl[0], br[0]), min(tl[1], br[1]))
            br_corrected = (max(tl[0], br[0]), max(tl[1], br[1]))
            camera_coordinates = {"tl_corner": tl_corrected, "br_corner": br_corrected}
            save_coordinates(camera_coordinates)
            show_success("Success", "Camera calibration saved.")
            break
        elif key == 27:  # ESC
            break

    cap.release()
    cv2.destroyAllWindows()

# ------- Entry Point -------
if __name__ == "__main__":
    camera_calibration()
