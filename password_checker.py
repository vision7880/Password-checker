import tkinter as tk
from tkinter import ttk
import re
import math

# Estimate how long to crack the password
def estimate_crack_time(password):
    charset_size = 0
    if re.search(r'[a-z]', password): charset_size += 26
    if re.search(r'[A-Z]', password): charset_size += 26
    if re.search(r'\d', password): charset_size += 10
    if re.search(r'[\W_]', password): charset_size += 33

    entropy = len(password) * math.log2(charset_size) if charset_size else 0
    total_combinations = 2 ** entropy
    guesses_per_sec = 1e9
    seconds = total_combinations / guesses_per_sec

    if seconds < 1:
        return "less than a second"
    elif seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        return f"{int(seconds // 60)} minutes"
    elif seconds < 86400:
        return f"{int(seconds // 3600)} hours"
    elif seconds < 31536000:
        return f"{int(seconds // 86400)} days"
    else:
        years = seconds / 31536000
        return f"{years:.2f} years"

# Calculate strength
def check_strength(password):
    score = sum([
        len(password) >= 8,
        bool(re.search(r'[a-z]', password)),
        bool(re.search(r'[A-Z]', password)),
        bool(re.search(r'\d', password)),
        bool(re.search(r'[\W_]', password)),
    ]) * 20

    if score <= 40:
        strength, color = "Weak", "red"
    elif 60 <= score < 100:
        strength, color = "Moderate", "orange"
    else:
        strength, color = "Strong", "green"

    crack_time = estimate_crack_time(password)
    return strength, score, color, crack_time

# Update GUI in real time
def update_feedback(*args):
    pwd = password_var.get()
    strength, score, color, crack_time = check_strength(pwd)

    strength_label.config(text=f"Strength: {strength}", foreground=color)
    score_label.config(text=f"{score}%")
    crack_time_label.config(text=f"Crack Time: {crack_time}")
    strength_bar["value"] = score

# Toggle password visibility
def toggle_password():
    if show_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")

# Toggle dark mode
def toggle_dark_mode():
    dark = dark_mode.get()
    bg = "#2e2e2e" if dark else "#f0f0f0"
    fg = "white" if dark else "black"
    for widget in root.winfo_children():
        widget.configure(bg=bg)
        try:
            widget.configure(fg=fg)
        except: pass
    root.configure(bg=bg)

# GUI Setup
root = tk.Tk()
root.title("🔐 Password Strength Checker")
root.geometry("400x300")
root.resizable(False, False)

# Style
style = ttk.Style()
style.configure("TProgressbar", thickness=20)

# Variables
password_var = tk.StringVar()
password_var.trace("w", update_feedback)
show_var = tk.BooleanVar()
dark_mode = tk.BooleanVar()

# Widgets
tk.Label(root, text="Enter Password:", font=("Arial", 12)).pack(pady=10)
password_entry = ttk.Entry(root, textvariable=password_var, show="*", width=30, font=("Arial", 12))
password_entry.pack()

show_check = tk.Checkbutton(root, text="Show Password", variable=show_var, command=toggle_password)
show_check.pack()

strength_label = tk.Label(root, text="Strength: ", font=("Arial", 12))
strength_label.pack(pady=5)

score_label = tk.Label(root, text="0%", font=("Arial", 10))
score_label.pack()

strength_bar = ttk.Progressbar(root, length=250, maximum=100)
strength_bar.pack(pady=5)

crack_time_label = tk.Label(root, text="Crack Time: ", font=("Arial", 10))
crack_time_label.pack()

dark_mode_toggle = tk.Checkbutton(root, text="🌙 Dark Mode", variable=dark_mode, command=toggle_dark_mode)
dark_mode_toggle.pack(pady=10)

# Start
update_feedback()
root.mainloop()
