import keyboard
def mute():
        keyboard.press_and_release("volume mute")
def unmute():
        keyboard.press_and_release("volume mute")
def volume_up():
        keyboard.press_and_release("volume up")
    
def volume_down():
    keyboard.press_and_release("volume down") 
inp=int(input("Enter the voome to decrease"))
for i in range(inp):
        volume_down()
# unmute()