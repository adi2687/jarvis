import requests
from AppOpener import close , open as appopen
def close(app , sess=requests.session()):
    close(app , match_closest=True,output=True,throw_error=True)
close("whatsapp")