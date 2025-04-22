import customtkinter as ctk
import google.generativeai as genai
import os
import threading
import time
from dotenv import load_dotenv
from PIL import ImageGrab
import pytesseract
import keyboard
import win32gui
import win32con
import ctypes

# --- Tesseract Configuration ---
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update path if needed

# --- Load API Key ---
load_dotenv()
API_KEY = os.environ['GOOGLE_API_KEY'] # Replace with os.getenv('GOOGLE_API_KEY') if using .env

if not API_KEY:
    print("Error: GOOGLE_API_KEY not found. Make sure it's set in your .env file.")
    exit()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- UI Setup ---
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
app = ctk.CTk()
app.title("Local AI Coding Helper")
app.geometry("800x600")

# --- Optional: Frameless Overlay (commented by default) ---
# app.overrideredirect(True)

# --- Make Window a Tool Window (Stealth Mode) ---
hwnd = ctypes.windll.user32.FindWindowW(None, "Local AI Coding Helper")
if hwnd:
    ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    ex_style |= win32con.WS_EX_TOOLWINDOW   # Hide from Alt+Tab, sometimes screen share
    ex_style &= ~win32con.WS_EX_APPWINDOW   # Hide from taskbar
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style)
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)

# --- Transparency & Overlay Settings ---
app.wm_attributes("-topmost", True)
app.wm_attributes("-alpha", 0.60)
app.wm_attributes("-transparentcolor", "white")
app.configure(bg="white")

# --- UI Frames ---
input_frame = ctk.CTkFrame(app)
input_frame.pack(pady=10, padx=10, fill="x")
input_label = ctk.CTkLabel(input_frame, text="Enter Coding Problem / Question:")
input_label.pack(pady=5)
input_textbox = ctk.CTkTextbox(input_frame, height=150, width=760)
input_textbox.pack(pady=5, padx=5)

button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=5)

output_frame = ctk.CTkFrame(app)
output_frame.pack(pady=10, padx=10, fill="both", expand=True)
output_label = ctk.CTkLabel(output_frame, text="AI Response:")
output_label.pack(pady=5)
output_textbox = ctk.CTkTextbox(output_frame, width=760)
output_textbox.pack(pady=5, padx=5, fill="both", expand=True)
output_textbox.configure(state="disabled")

# --- Update Output ---
def update_output(text):
    app.after(0, lambda: _update_output_on_main_thread(text))

def _update_output_on_main_thread(text):
    output_textbox.configure(state="normal")
    output_textbox.delete("1.0", "end")
    output_textbox.insert("1.0", text)
    output_textbox.configure(state="disabled")

# --- Gemini API Call ---
def call_gemini_api(problem):
    try:
        update_output("Generating response... Please wait.")
        prompt = f"""
        You are an expert coding assistant. Please solve the following coding problem.
        Provide a clear code solution (preferably in Python, unless otherwise specified in the problem)
        and a step-by-step explanation of the logic.

        Problem:
        {problem}

        Solution and Explanation:
        """
        response = model.generate_content(prompt)
        update_output(response.text)
    except Exception as e:
        update_output(f"An error occurred: {e}")

# --- Handle AI Request ---
def on_button_click():
    problem_text = input_textbox.get("1.0", "end-1c").strip()
    if not problem_text:
        update_output("Please enter a problem first.")
        return

    ai_button.configure(state="disabled", text="Processing...")

    def task_wrapper(problem):
        call_gemini_api(problem)
        app.after(0, lambda: ai_button.configure(state="normal", text="Get AI Help"))

    thread = threading.Thread(target=task_wrapper, args=(problem_text,))
    thread.daemon = True
    thread.start()

# --- Screenshot & OCR Integration ---
def take_screenshot_and_extract_text():
    update_output("Taking screenshot and extracting text...")
    app.withdraw()  # Hide before capture
    time.sleep(0.5)

    img = ImageGrab.grab()
    app.deiconify()  # Show again

    extracted_text = pytesseract.image_to_string(img)

    if extracted_text.strip():
        input_textbox.delete("1.0", "end")
        input_textbox.insert("1.0", extracted_text)
        update_output("Text extracted from screenshot. Ready to generate solution.")
    else:
        update_output("No readable text detected in screenshot.")

# --- Toggle App Visibility ---
def toggle_visibility():
    if app.winfo_viewable():
        app.withdraw()
    else:
        app.deiconify()

# --- Keyboard Shortcuts ---
keyboard.add_hotkey("ctrl+enter", on_button_click)
keyboard.add_hotkey("ctrl+h", take_screenshot_and_extract_text)
keyboard.add_hotkey("ctrl+g", lambda: input_textbox.delete("1.0", "end"))
keyboard.add_hotkey("alt+f4", app.quit)
keyboard.add_hotkey("ctrl+b", lambda: toggle_visibility())

# --- Connect AI Button ---
ai_button = ctk.CTkButton(button_frame, text="Get AI Help", command=on_button_click)
ai_button.pack()

# --- Shortcut Info ---
shortcuts_text = """
🔧 Keyboard Shortcuts:
• Take Screenshot: Ctrl + H
• Generate Solution: Ctrl + Enter
• Hide/Show Window: Ctrl + B
• Clear Input (Reset): Ctrl + G
• Quit App: Alt + F4
"""

shortcut_frame = ctk.CTkFrame(app)
shortcut_frame.pack(pady=5, padx=10, fill="x")
shortcut_label = ctk.CTkLabel(shortcut_frame, text=shortcuts_text, justify="left", anchor="w")
shortcut_label.pack(padx=10, pady=5, fill="x")

# --- Run the App ---
app.mainloop()
