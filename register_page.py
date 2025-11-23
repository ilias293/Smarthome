import customtkinter as ctk
import tkinter.messagebox as tkmb
from database import register_user

class RegisterPage(ctk.CTkFrame):
    def __init__(self, master, go_to_login):
        super().__init__(master)
        self.go_to_login = go_to_login

        ctk.CTkLabel(self, text="Account Aanmaken", font=("Arial", 28, "bold")).pack(pady=20)

        form = ctk.CTkFrame(self)
        form.pack(pady=20, padx=40)

        self.username = ctk.CTkEntry(form, placeholder_text="Nieuwe gebruikersnaam")
        self.username.pack(pady=10, padx=20)

        self.password = ctk.CTkEntry(form, placeholder_text="Wachtwoord", show="*")
        self.password.pack(pady=10, padx=20)

        self.password2 = ctk.CTkEntry(form, placeholder_text="Herhaal wachtwoord", show="*")
        self.password2.pack(pady=10, padx=20)

        ctk.CTkButton(form, text="Account Registreren", command=self.register).pack(pady=20)

        ctk.CTkButton(
            self, text="⬅ Terug naar Login", fg_color="gray20", command=self.go_to_login
        ).pack(pady=10)

    def register(self):
        user = self.username.get().strip()
        pw1 = self.password.get().strip()
        pw2 = self.password2.get().strip()

        if user == "" or pw1 == "" or pw2 == "":
            tkmb.showwarning("Fout", "Vul alle velden in.")
            return

        if pw1 != pw2:
            tkmb.showwarning("Fout", "Wachtwoorden komen niet overeen.")
            return

        success, msg = register_user(user, pw1)

        if success:
            tkmb.showinfo("Account aangemaakt", msg)
            self.go_to_login()
        else:
            tkmb.showerror("Fout", msg)
