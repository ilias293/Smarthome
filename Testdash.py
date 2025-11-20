
import customtkinter as ctk
import tkinter.messagebox as tkmb
from customtkinter import CTkFont

# GUI theme instellen
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry("400x400")
app.title("Inlogdashboard van Senior Smart Home")


def login():
    gebruikersnaam = "Puck"
    wachtwoord = "12345"

    if user_entry.get() == gebruikersnaam and user_pass.get() == wachtwoord:
        tkmb.showinfo("Succesvol ingelogd", "u bent ingelogd")

        # Nieuwe window
        new_window = ctk.CTkToplevel(app)
        new_window.title("New Window")
        new_window.geometry("350x150")

        ctk.CTkLabel(new_window, text="Welkom bij Senior Smart Home !!").pack()

    elif user_entry.get() == gebruikersnaam and user_pass.get() != wachtwoord:
        tkmb.showwarning("Onjuist wachtwoord", "Controleer je wachtwoord")

    elif user_entry.get() != gebruikersnaam and user_pass.get() == wachtwoord:
        tkmb.showwarning("Onjuiste gebruikersnaam", "Controleer je gebruikersnaam")

    else:
        tkmb.showerror("Login mislukt", "Onjuiste gebruikersnaam of wachtwoord")


# Titel label
titel_font = CTkFont(size=28, weight="bold")
label = ctk.CTkLabel(app, text="Senior Smart Home", font = titel_font)
label.pack(pady=20)

# Frame
frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=40, fill='both', expand=True)

# Login tekst
label = ctk.CTkLabel(master=frame, text='Inloggen bij Senior Smart Home')
label.pack(pady=12, padx=10)

# Gebruikersnaam
user_entry = ctk.CTkEntry(master=frame, placeholder_text="Gebruikersname")
user_entry.pack(pady=12, padx=10)

# Wachtwoord
user_pass = ctk.CTkEntry(master=frame, placeholder_text="WACHTWOORD", show="*")
user_pass.pack(pady=12, padx=10)

# Login knop
button = ctk.CTkButton(master=frame, text='Login', command=login)
button.pack(pady=12, padx=10)

# Checkbox
checkbox = ctk.CTkCheckBox(master=frame, text='Remember Me')
checkbox.pack(pady=12, padx=10)

app.mainloop()
