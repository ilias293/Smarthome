from tkinter import *

root = Tk()

label = Label(master=root, text="Maddox", height=2)
label.pack()

button = Button(master=root, text="Click Me")
button.pack(pady=10)

entry = Entry(master=root)
entry.pack(padx=10, pady=10)

root.mainloop()
