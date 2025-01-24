ef stop_response():
    global stop_flag
    stop_flag = True
    output_label.config(text="Jarvis: Stopping...") 
def voice_input():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True
    while True:
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
