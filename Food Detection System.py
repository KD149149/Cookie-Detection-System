# Developer Details
# Developer Name: Kajal Dadas
# Email: [kajaldadas149@gmail.com](mailto:kajaldadas149@gmail.com)
# For development support, customization, or industrial deployment inquiries, please reach out via email.

import cv2
import numpy as np
import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
import pandas as pd
import datetime
import os
import math

# =========================
# Global State
# =========================
cookie_id = 0
total_count = 0
ok_count = 0
faulty_count = 0
report_rows = []
seen_centers = []

cap = None
video_writer = None

# =========================
# Output Setup
# =========================
BASE_DIR = "output"
DATE_DIR = datetime.datetime.now().strftime("%Y-%m-%d")
OUTPUT_DIR = os.path.join(BASE_DIR, DATE_DIR)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# Utility
# =========================
def already_seen(cx, cy, threshold=40):
    for (x, y) in seen_centers:
        if abs(cx - x) < threshold and abs(cy - y) < threshold:
            return True
    return False

# =========================
# Detection (High-Speed)
# =========================
def detect_cookies(frame):
    global cookie_id, total_count, ok_count, faulty_count

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (9, 9), 1.5)

    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=40,
        param1=100,
        param2=30,
        minRadius=15,
        maxRadius=40
    )

    if circles is None:
        return

    circles = np.uint16(np.around(circles))

    for x, y, r in circles[0]:
        if already_seen(x, y):
            cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
            continue

        mask = np.zeros(gray.shape, dtype=np.uint8)
        cv2.circle(mask, (x, y), r, 255, -1)

        detected_area = cv2.countNonZero(mask & gray)
        ideal_area = math.pi * r * r
        area_ratio = detected_area / ideal_area

        cookie_id += 1
        total_count += 1
        seen_centers.append((x, y))

        if area_ratio >= 0.75:
            status = "OK"
            color = (0, 255, 0)
            ok_count += 1
        else:
            status = "FAULTY"
            color = (0, 0, 255)
            faulty_count += 1

        cv2.circle(frame, (x, y), r, color, 2)
        cv2.putText(
            frame,
            f"ID-{cookie_id}",
            (x - 15, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            color,
            2
        )

        report_rows.append({
            "ID": cookie_id,
            "Status": status,
            "Area_Ratio": round(area_ratio, 2),
            "Time": datetime.datetime.now().strftime("%H:%M:%S")
        })

# =========================
# Frame Loop
# =========================
def update_frame():
    ret, frame = cap.read()
    if not ret:
        return

    frame = cv2.resize(frame, (640, 480))
    detect_cookies(frame)
    video_writer.write(frame)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(rgb)
    imgtk = ImageTk.PhotoImage(img)

    video_label.configure(image=imgtk)
    video_label.image = imgtk

    stats_label.config(
        text=f"""
Total Cookies : {total_count}
Perfect       : {ok_count}
Faulty        : {faulty_count}
"""
    )

    root.after(5, update_frame)  # faster loop

# =========================
# Report
# =========================
def generate_report():
    if not report_rows:
        return

    df = pd.DataFrame(report_rows)
    file = f"cookie_report_{datetime.datetime.now().strftime('%H%M%S')}.xlsx"
    df.to_excel(os.path.join(OUTPUT_DIR, file), index=False)

# =========================
# Camera Selection (ONE POPUP)
# =========================
def select_camera():
    global cap, video_writer

    choice = simpledialog.askinteger(
        "Camera Selection",
        "Select Input:\n1 - Live Camera\n2 - IP Camera"
    )

    if choice == 1:
        cap = cv2.VideoCapture(0)
    elif choice == 2:
        ip = simpledialog.askstring("IP Camera", "Enter Camera URL")
        cap = cv2.VideoCapture(ip)
    else:
        return

    video_path = os.path.join(
        OUTPUT_DIR,
        f"recording_{datetime.datetime.now().strftime('%H%M%S')}.mp4"
    )
    video_writer = cv2.VideoWriter(
        video_path,
        cv2.VideoWriter_fourcc(*'mp4v'),
        25,
        (640, 480)
    )

    update_frame()

# =========================
# UI
# =========================
root = tk.Tk()
root.title("High-Speed Cookie Inspection")

video_label = tk.Label(root)
video_label.pack(side=tk.LEFT, padx=10, pady=10)

stats_label = tk.Label(root, font=("Arial", 14), justify="left")
stats_label.pack(side=tk.RIGHT, padx=10)

select_camera()
root.mainloop()

if cap:
    cap.release()
if video_writer:
    video_writer.release()
generate_report()
cv2.destroyAllWindows()
