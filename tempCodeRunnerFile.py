import tkinter as tk
from threading import Thread
from jarvis_alpha import main

# Create the main application window
root = tk.Tk()
root.title("Jarvis-Inspired UI")
root.geometry("700x400")
root.configure(bg="white")

# Configure the grid layout
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

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
        input_box.delete(0, tk.END)  # Clear the input box
        thread = Thread(target=get_response, args=(user_text,))
        thread.start()
    else:
        output_label.config(text="Jarvis: Please enter something!")

# Controls frame
controls_frame = tk.Frame(root, bg="#0F0F0F")
controls_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

# Input box
input_box = tk.Entry(
    controls_frame,
    font=("Consolas", 16),
    width=30,
    bd=0,
    bg="#1C1C1C",
    fg="#00FFFF",
    insertbackground="#00FFFF",
    highlightthickness=2,
    highlightbackground="#00FFFF"
)
input_box.pack(pady=20)

# Button
submit_button = tk.Button(
    controls_frame,
    text="Speak to Jarvis",
    command=display_text,
    font=("Consolas", 14),
    bg="#1C1C1C",
    fg="#00FFFF",
    activebackground="white",
    activeforeground="#1C1C1C",
    bd=0,
    padx=10,
    pady=5
)
submit_button.pack(pady=10)

# Output label with pixel-based width
output_label = tk.Label(
    controls_frame,
    text="",
    font=("Consolas", 16),
    bg="#0F0F0F",
    fg="#00FF00",
    width=50,  # Character-based width
    wraplength=600  # Wrap text after 400px,
    
)
output_label.pack(pady=20)

# Run the application
root.mainloop()
