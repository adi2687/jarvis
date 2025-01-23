import requests
from AppOpener import close , open as appopen

def Open(app , sess=requests.session()):

    appopen(app , match_closest=True , output=True , throw_error=True) 

while True:
    inputmain=input("Enter the app")
    
    if inputmain:Open(inputmain)
    else:break
    