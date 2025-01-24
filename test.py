import tkinter as tk
from threading import Thread
from jarvis_alpha import main,speak,setup_jarvis
from PIL import Image, ImageSequence, ImageTk
import speech_recognition as sr
import json
import keyboard
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
            if stop_flag:  # Check if stop flag is set
                output_label.config(text="Jarvis: Stopped.")
                return  # Exit the function
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

def voice_input():
    global stop_flag
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True
    while not stop_flag:  # Continuously listen until stop_flag is set
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                output_label.config(text="Jarvis: Listening for your command...")

                audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
                if stop_flag:  # Break immediately if stop_flag is set
                    output_label.config(text="Jarvis: Listening stopped.")
                    break
                
                command = recognizer.recognize_google(audio).lower()
                output_label.config(text=f"Recognxized: {command}")
                if "volume" in command:
                    if "decrease" in command:
                        # def volume_down():
                            # just a fixed value for increase or decreasse
                        for i in range(10):
                            keyboard.press_and_release("volume down")
                    elif "increase" in command:
                        keyboard.press_and_release("volume-up")
                elif "mute" or "unmute" in command:
                    keyboard.press_and_release("volume-mute")
                thread = Thread(target=get_response, args=(command,))
                thread.start()
        except sr.UnknownValueError:
            if not stop_flag:  # Only show errors if not stopping
                output_label.config(text="Jarvis: I couldn't understand that. Please try again.")
        except sr.WaitTimeoutError:
            if not stop_flag:
                output_label.config(text="Jarvis: No input detected. Please try again.")
        except sr.RequestError:
            output_label.config(text="Jarvis: Issue with the recognition service.")
        except Exception as e:
            output_label.config(text=f"Jarvis: An unexpected error occurred: {e}")

def stop_response():
    global stop_flag
    stop_flag = True  # Set the flag to True to interrupt speaking
    output_label.config(text="Jarvis: Speech stopped.")  # Update UI

def voice_input_thread():
    global stop_flag
    stop_flag = False 
    thread = Thread(target=voice_input)
    thread.start()

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
    text="🎤", 
    command=voice_input_thread, 
    font=("Helvetica", 14, "bold"),
    bg="#007BFF",
    fg="#FFFFFF",
    activebackground="#0056b3",
    activeforeground="#FFFFFF",
    bd=0,
    relief="flat"
)

button_size = 50  # Button size (width and height)
voice_button.place(
    x=290, y=70, width=100, height=35
)


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

def update_gif(frame_index=0):
    global frames
    frame = frames[frame_index]
    gif_label.config(image=frame)
    frame_index = (frame_index + 1) % len(frames)
    root.after(10, update_gif, frame_index)

gif_path = "Sirifinal.gif"  # Replace with the path to your GIF
image = Image.open(gif_path)

gif_width = int(root.winfo_screenwidth() * 0.5)
gif_height = int(root.winfo_screenheight() * 0.9)
frames = [
    ImageTk.PhotoImage(frame.resize((gif_width, gif_height), Image.Resampling.LANCZOS))
    for frame in ImageSequence.Iterator(image)
]

gif_label = tk.Label(root, bg="#000000")
gif_label.place(relx=0.5, rely=0.5, anchor="center")  # Positioned at 70% width and center height
update_gif()

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

scrollbar = tk.Scrollbar(frame, command=chat_hist.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

chat_hist.config(yscrollcommand=scrollbar.set)
def display_chat():
    try:
        with open('Data/ChatLog.json', "r") as file:
            chat_log = json.load(file)
            chat_hist.config(state="normal")  # Allow editing to update content
            chat_hist.delete(1.0, tk.END)  # Clear the existing text

            formatted_chat = ""
            for entry in chat_log:
                role = entry.get("role", "Unknown").capitalize()
                content = entry.get("content", "No content provided")
                formatted_chat += f"{role}: {content}\n"

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