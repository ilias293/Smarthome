from tkinter import *

def onclick():
    base = int(entry.get())
    square = base**2
    outcome = f"square: of {base} = {square}"
    label['text'] = outcome

def offclick():
    getal1 = int(entry.get())
    getal2 = int(entry2.get())
    optelsom = getal1 * getal2
    uitkomst = f"de vermenigvuldiging van {getal1} en {getal2} = {optelsom}"
    label2['text'] = uitkomst

root = Tk()

label = Label(master=root, text="Maddox", background="pink", height=2)
label.pack()

label2 = Label(master=root, text="Ayoub", background="red", height=2)
label2.pack()

button = Button(master=root, text="Click Me", command=onclick)
button.pack(pady=10)

button2 = Button(master=root, text="Klik op mij", command=offclick)
button2.pack(pady=10)

entry = Entry(master=root)
entry.pack(padx=10, pady=10)

entry2 = Entry(master=root)
entry2.pack(padx=10, pady=10)

img = PhotoImage(file='fcutrechtfoto.png')
label = Label(master=root, image=img)
label.pack()


root.mainloop()
