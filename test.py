import tkinter as tk
from jarvis import main
# def on_button_click():
#     label.config(text="Hello, " + entry.get())

root = tk.Tk()
root.title("Jarvis")


button = tk.Button(root, text="SClick here to Start Jarvis", command=main)
button.pack()

root.mainloop()
