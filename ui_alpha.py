import pyttsx3 
def setup_jarvis():
        jarvis = pyttsx3.init()
        voices = jarvis.getProperty("voices")
        jarvis.setProperty("voice", voices[0].id)  # Select a voice
        jarvis.setProperty("rate", 200)
        return jarvis

jar = setup_jarvis()
print("said")
jar.say("okki am here ")
jar.stop()
jar.say("ok no this is not")
jar.runAndWait()  