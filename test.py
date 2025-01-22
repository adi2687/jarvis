import tkinter as tk
from threading import Thread
from jarvis_alpha import main
from PIL import Image, ImageSequence, ImageTk
import  pyttsx3 
import speech_recognition as sr
# Create the main application window
root = tk.Tk()
root.title("Jarvis")
root.geometry("800x500")  # Adjust window size for proportions
root.configure(bg="#000000")  # Sleek dark background
def setup_jarvis():
    jarvis=pyttsx3.init()
    voices=jarvis.getProperty("voices")
    jarvis.setProperty('voice',voices[1].id)
    jarvis.setProperty('rate',240)
    return jarvis
def speak(jarvis,text):
    print(text)
    jarvis.say(text)
    jarvis.runAndWait()
# Function to handle the Jarvis response
def get_response(user_text):
    try:
        
        response = main(user_text)
        output_label.config(text=f"Jarvis: {response}")
    except Exception as e:
        output_label.config(text=f"Error: {e}")

# Function to run in a thread
def display_text():
    user_text = input_box.get()
    if user_text.strip():
        input_box.delete(0, tk.END)         
        thread = Thread(target=get_response, args=(user_text,))
        thread.start()
    else:
        output_label.config(text="Jarvis: Please enter something!")

# Function to animate the GIF
def update_gif(frame_index=0):
    global frames
    frame = frames[frame_index]
    gif_label.config(image=frame)
    frame_index = (frame_index + 1) % len(frames)
    root.after(40, update_gif, frame_index)

# Load GIF
gif_path = "Graphics/jarvis1.gif"  # Replace with the path to your GIF
image = Image.open(gif_path)

# Resize GIF frames to fit 30% width and height of the page
gif_width = int(root.winfo_screenwidth() * 0.3)
gif_height = int(root.winfo_screenheight() * 0.3)
frames = [
    ImageTk.PhotoImage(frame.resize((gif_width, gif_height), Image.Resampling.LANCZOS))
    for frame in ImageSequence.Iterator(image)
]

# GIF display in the center-right
gif_label = tk.Label(root, bg="#000000")
gif_label.place(relx=0.5, rely=0.5, anchor="center")  # Positioned at 70% width and center height
update_gif()

# Input box
input_box = tk.Entry(
    root,
    font=("Helvetica", 14),
    bd=0,
    bg="#1E1E1E",
    fg="#00E676",
    insertbackground="#00E676",  # Cursor color
    highlightthickness=1,
    highlightbackground="#00E676"
)
input_box.place(x=20, y=20, width=300, height=35)  # Top-left corner

# Button below the input box
submit_button = tk.Button(
    root,
    text="Speak to Jarvis",
    command=display_text,
    font=("Helvetica", 12, "bold"),
    bg="#00E676",
    fg="#000000",
    activebackground="#000000",
    activeforeground="#00E676",
    bd=0,
    relief="flat"
)
submit_button.place(x=20, y=70, width=150, height=35)

# Output text label
output_label = tk.Label(
    root,
    text="",
    font=("Helvetica", 12),
    bg="#000000",  # Pure black background
    fg="#E0E0E0",  # Light gray text
    wraplength=500,
    justify="left"
)
output_label.place(x=10, y=120, anchor="nw")  # Positioned in the top-left corner

root.mainloop()
