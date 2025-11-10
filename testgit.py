from tkinter import *

def onclick():
    base = int(entry.get())
    square = base**2
    outcome = f"square: of {base} = {square}"
    label['text'] = outcome

root = Tk()

label = Label(master=root, text="Maddox", height=2)
label.pack()

button = Button(master=root, text="Click Me", command=onclick)
button.pack(pady=10)

entry = Entry(master=root)
entry.pack(padx=10, pady=10)

root.mainloop()
