import tkinter as tk
from threading import Thread
from jarvis_alpha import main,speak,setup_jarvis
from PIL import Image, ImageSequence, ImageTk
import speech_recognition as sr
import json
root = tk.Tk()
root.title("Jarvis")
root.geometry("800x500")  # Adjust window size for proportions
root.configure(bg="#000000")  # Sleek dark background
stop_flag = False
def get_response(user_text):
    global stop_flag
    try:
        submit_button.config(text="Waiting...", state="disabled")
        
        jarvis = setup_jarvis() 
        response = main(user_text)
        
        retry_count = 0
        max_retries = 10  
        while not response and retry_count < max_retries:
            if stop_flag:  
                output_label.config(text="Jarvis: Stopped.")
                break
            print("waiting")
            retry_count += 1
            
        if not response:
            output_label.config(text="Jarvis: No response received. Please try again.")
        else:
            output_label.config(text=f"Jarvis: {response}")
            if not stop_flag:
                speak(jarvis, response)
    except Exception as e:
        output_label.config(text=f"Error: {e}")
    finally:
        submit_button.config(text="Speak to Jarvis", state="normal")


def stop_response():
    global stop_flag
    stop_flag = True
    output_label.config(text="Jarvis: Stopping...") 
def voice_input():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            output_label.config(text="Speak the commabd")
            output_label.config(text="Jarvis: Listening for your command...")
            
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            
            command = recognizer.recognize_google(audio).lower()
            
            output_label.config(text=f"Recognized: {command}")
            
            thread = Thread(target=get_response, args=(command,))
            thread.start()
    except sr.UnknownValueError:
        output_label.config(text="Jarvis: I couldn't understand that. Please try again.")
    except sr.WaitTimeoutError:
        output_label.config(text="Jarvis: No input detected. Please try again.")
    except sr.RequestError:
        output_label.config(text="Jarvis: Issue with the recognition service.")
    except Exception as e:
        output_label.config(text=f"Jarvis: An unexpected error occurred: {e}")

                
# Add a Stop button below the Submit button
stop_button = tk.Button(
    root,
    text="Stop",
    command=stop_response,
    font=("Helvetica", 12, "bold"),
    bg="#FF5252",
    fg="#FFFFFF",   
    activebackground="#FF1744",
    activeforeground="#FFFFFF",
    bd=0,
    relief="flat"
)
stop_button.place(x=180, y=70, width=100, height=35)

def voice_input_thread():
    """Run the voice input function in a separate thread to avoid freezing the UI."""
    thread = Thread(target=voice_input)
    thread.start()

voice_button = tk.Button(
    root,
    text="🎤",  # Use a microphone emoji for better representation
    command=voice_input_thread,  # Run voice_input in a separate thread
    font=("Helvetica", 14, "bold"),
    bg="#007BFF",  # Blue background color
    fg="#FFFFFF",  # White text color
    activebackground="#0056b3",  # Darker blue for active state
    activeforeground="#FFFFFF",  # White text when active
    bd=0,
    relief="flat"
)

# Set dimensions for a circular appearance
button_size = 50  # Button size (width and height)
voice_button.place(
    x=290, y=70, width=100, height=35
)


# To make it circular, apply rounded corners using the canvas
voice_button.config(borderwidth=0, highlightthickness=0)
voice_button.place(x=290,y=70,width=100,height=35)

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
    root.after(10, update_gif, frame_index)

# Load GIF
gif_path = "Sirifinal.gif"  # Replace with the path to your GIF
image = Image.open(gif_path)

# Resize GIF frames to fit 30% width and height of the page
gif_width = int(root.winfo_screenwidth() * 0.5)
gif_height = int(root.winfo_screenheight() * 0.9)
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
    font=("Helvetica", 17),
    bg="#000000",  # Pure black background
    fg="#E0E0E0",  # Light gray text
    wraplength=500,
    justify="left"
)
output_label.place(x=10, y=120, anchor="nw")  # Positioned in the top-left corner

# unknown option "-yscrollcommand"

frame = tk.Frame(root, bg="#999999")
frame.place(x=1000, y=60, anchor="nw")


chat_hist = tk.Text(
    frame,
    font=("Helvetica", 14),
    bg="#000000",
    fg="#999999",
    wrap="word",
    height=20,
    width=60
)
chat_hist.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a Scrollbar for the Text widget
scrollbar = tk.Scrollbar(frame, command=chat_hist.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the scrollbar with the Text widget
chat_hist.config(yscrollcommand=scrollbar.set)

# Function to display the chat
def display_chat():
    try:
        with open('Data/ChatLog.json', "r") as file:
            chat_log = json.load(file)
            chat_hist.config(state="normal")  # Allow editing to update content
            chat_hist.delete(1.0, tk.END)  # Clear the existing text

            # Format and display chat content
            formatted_chat = ""
            for entry in chat_log:
                role = entry.get("role", "Unknown").capitalize()
                content = entry.get("content", "No content provided")
                formatted_chat += f"{role}: {content}\n\n"

            chat_hist.insert(tk.END, formatted_chat)
            chat_hist.config(state="disabled")  # Disable editing after updating
    except FileNotFoundError:
        chat_hist.config(state="normal")
        chat_hist.delete(1.0, tk.END)
        chat_hist.insert(tk.END, "Error: Chat log file not found.")
        chat_hist.config(state="disabled")
    except json.JSONDecodeError:
        chat_hist.config(state="normal")
        chat_hist.delete(1.0, tk.END)
        chat_hist.insert(tk.END, "Error: Chat log file is not a valid JSON.")
        chat_hist.config(state="disabled")

# Button to display the chat log
chatdisp = tk.Button(
    root,
    text="Previous Chat",
    font=("Helvetica", 17),
    bg="#4C4C4C",
    fg="#FFFFFF",
    command=display_chat
)
chatdisp.place(x=1000, y=500, anchor="nw")  # Adjust position as needed

root.mainloop()