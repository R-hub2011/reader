import tkinter as tk
import win32gui
import win32con
import ctypes

# --- Create Root Window ---
root = tk.Tk()
root.title("Invisible on Screenshare")
root.geometry("400x200")
root.configure(bg="magenta")  # Unique color to make transparent

# --- Make Background Transparent ---
root.wm_attributes("-transparentcolor", "magenta")
root.wm_attributes("-topmost", True)

# --- Stealth Flags: Hide from Alt+Tab and Maybe Screenshare ---
def apply_stealth():
    hwnd = ctypes.windll.user32.FindWindowW(None, "Invisible on Screenshare")
    if hwnd:
        ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        ex_style |= (
            win32con.WS_EX_TOOLWINDOW |
            win32con.WS_EX_LAYERED |
            win32con.WS_EX_TRANSPARENT
        )
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style)
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)

root.after(100, apply_stealth)

# --- Add Label ---
label = tk.Label(root, text="👀 You see this, but screen share won't!", bg="magenta", fg="white", font=("Arial", 14))
label.pack(pady=60)

# --- Run App ---
root.mainloop()
