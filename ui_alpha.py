import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence
import threading
import pyttsx3
from jarvis_beta import main
# Setup Jarvis TTS
def setup_jarvis():
    jarvis = pyttsx3.init()
    voices = jarvis.getProperty("voices")
    jarvis.setProperty('voice', voices[0].id)
    jarvis.setProperty('rate', 190)
    return jarvis


jarvis = setup_jarvis()


def speak(text):
    jarvis.say(text)
    jarvis.runAndWait()


# Tkinter GUI
class JarvisUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jarvis - Your Assistant")
        self.root.geometry("500x500")
        self.root.resizable(False, False)

        # Input Section
        self.label = tk.Label(root, text="Ask Jarvis:", font=("Arial", 14))
        self.label.pack(pady=10)

        self.entry = tk.Entry(root, font=("Arial", 14), width=30)
        self.entry.pack(pady=10)

        self.ask_button = tk.Button(root, text="Ask", font=("Arial", 12), command=self.ask_jarvis)
        self.ask_button.pack(pady=10)

        # Response Section
        self.response_label = tk.Label(root, text="", font=("Arial", 12), fg="blue")
        self.response_label.pack(pady=10)

        # GIF Section
        self.gif_label = tk.Label(root)
        self.gif_label.pack(pady=20)

        self.show_gif_button = tk.Button(root, text="Show GIF", font=("Arial", 12), command=self.toggle_gif)
        self.show_gif_button.pack(pady=10)

        # GIF Variables
        self.gif_thread = None
        self.is_gif_playing = False
        self.gif_frames = []
        self.gif_index = 0
        self.load_gif("Graphics/jarvis.gif")

    def load_gif(self, path):
        try:
            gif = Image.open(path)
            self.gif_frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(gif)]
        except Exception as e:
            messagebox.showerror("Error", f"Could not load GIF: {e}")

    def play_gif(self):
        while self.is_gif_playing and self.gif_frames:
            self.gif_label.config(image=self.gif_frames[self.gif_index])
            self.gif_index = (self.gif_index + 1) % len(self.gif_frames)
            self.gif_label.update()
            self.gif_label.after(100)  # Adjust speed as needed

    def toggle_gif(self):
        if self.is_gif_playing:
            self.is_gif_playing = False
            self.show_gif_button.config(text="Show GIF")
            self.gif_label.config(image="")
        else:
            self.is_gif_playing = True
            self.show_gif_button.config(text="Hide GIF")
            self.gif_thread = threading.Thread(target=self.play_gif, daemon=True)
            self.gif_thread.start()

    def ask_jarvis(self):
        user_input = self.entry.get().strip()
        if not user_input:
            messagebox.showwarning("Warning", "Please enter a valid input.")
            return
        if user_input.lower() in ["exit", "quit", "stop"]:
            self.root.quit()
        else:
            self.response_label.config(text=f"Jarvis: {user_input}")
            threading.Thread(target=speak, args=(user_input,), daemon=True).start()


# Run the Application
if __name__ == "__main__":
    root = tk.Tk()
    app = JarvisUI(root)
    root.mainloop()
