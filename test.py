import tkinter as tk
from threading import Thread
from jarvis_alpha import main,speak,setup_jarvis
from PIL import Image, ImageSequence, ImageTk
import speech_recognition as sr
root = tk.Tk()
root.title("Jarvis")
root.geometry("800x500")  # Adjust window size for proportions
root.configure(bg="#000000")  # Sleek dark background
root.bg="#000000"
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
def handle_command(jarvis):
        recognizer = sr.Recognizer()
        recognizer.dynamic_energy_threshold = True

        while True:
            try:
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    jarvis.say("Listening for your command...")
                    jarvis.runAndWait()
                
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)

                    command = recognizer.recognize_google(audio).lower()
            except sr.UnknownValueError:
                jarvis.say("I couldn't understand that. Please try again.")
                jarvis.runAndWait()
            except sr.WaitTimeoutError:
                jarvis.say("No input detected. Returning to wake-word mode.")
                jarvis.runAndWait()
                return
            except sr.RequestError:
                jarvis.say("There seems to be an issue with the recognition service.")
                jarvis.runAndWait()
                return
            except Exception as e:
                jarvis.say("An unexpected error occurred.")
                jarvis.runAndWait()
                print(f"Error: {e}")
                return
                
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
gif_width = int(root.winfo_screenwidth() * 0.5)
gif_height = int(root.winfo_screenheight() * 0.5)
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



root.mainloop()
