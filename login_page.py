import customtkinter as ctk
import tkinter.messagebox as tkmb
from customtkinter import CTkFont
from database import validate_login

class LoginPage(ctk.CTkFrame):
    def __init__(self, master, go_to_dashboard, go_to_register):
        super().__init__(master)
        self.master = master
        self.go_to_dashboard = go_to_dashboard
        self.go_to_register = go_to_register
        self.password_visible = False

        # Achtergrondkleur
        self.configure(fg_color="#E0E0F8")

        # Logo / afbeelding
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(pady=30)
        try:
            # Plaats een logo.png in de map 'assets'
            from PIL import Image
            logo_image = ctk.CTkImage(Image.open("assets/logo.png"), size=(120, 120))
            ctk.CTkLabel(logo_frame, image=logo_image, text="").pack()
        except:
            ctk.CTkLabel(logo_frame, text="🏠", font=("Arial", 50)).pack()

        # Titel
        title_font = CTkFont(size=36, weight="bold")
        ctk.CTkLabel(self, text="Senior Smart Home", font=title_font,
                     text_color="#4C2A85").pack(pady=10)

        # Card frame
        card = ctk.CTkFrame(self, corner_radius=20, fg_color="white",
                            border_width=1, border_color="#D1D1D1")
        card.pack(pady=20, padx=50, fill="x")

        ctk.CTkLabel(card, text="Inloggen", font=("Arial", 22, "bold"),
                     text_color="#4C2A85").pack(pady=20)

        # Gebruikersnaam
        self.username = ctk.CTkEntry(card, placeholder_text="Gebruikersnaam",
                                     height=40, border_width=1, corner_radius=10)
        self.username.pack(pady=10, padx=20, fill="x")

        # Wachtwoord + oog toggle
        pw_frame = ctk.CTkFrame(card, fg_color="transparent")
        pw_frame.pack(pady=10, padx=20, fill="x")

        self.password = ctk.CTkEntry(pw_frame, placeholder_text="Wachtwoord",
                                     show="*", height=40, border_width=1, corner_radius=10)
        self.password.pack(side="left", fill="x", expand=True)

        self.toggle_btn = ctk.CTkButton(
            pw_frame, text="👁", width=40, fg_color="#4C2A85",
            hover_color="#3B216A", command=self.toggle_password
        )
        self.toggle_btn.pack(side="right", padx=5)

        # Login knop
        self.login_btn = ctk.CTkButton(card, text="Inloggen", height=45,
                                       fg_color="#4C2A85", hover_color="#3B216A",
                                       corner_radius=12, command=self.login)
        self.login_btn.pack(pady=20, padx=20, fill="x")

        # OF regel
        ctk.CTkLabel(card, text="─ OF ─", text_color="#A0A0A0").pack(pady=5)

        # Registreren knop
        self.register_btn = ctk.CTkButton(card, text="Account Aanmaken", height=40,
                                          fg_color="transparent", text_color="#4C2A85",
                                          hover_color="#E0E0E0", corner_radius=12,
                                          command=self.go_to_register)
        self.register_btn.pack(pady=10, padx=20, fill="x")

        # Enter key activeert login
        self.username.bind("<Return>", lambda e: self.login())
        self.password.bind("<Return>", lambda e: self.login())

    def toggle_password(self):
        self.password_visible = not self.password_visible
        self.password.configure(show="" if self.password_visible else "*")

    def login(self):
        user = self.username.get().strip()
        pw = self.password.get().strip()

        if user == "" or pw == "":
            tkmb.showwarning("Leeg veld", "Vul een gebruikersnaam en wachtwoord in.")
            return

        if validate_login(user, pw):
            tkmb.showinfo("Succesvol", "U bent ingelogd!")
            self.go_to_dashboard()
        else:
            tkmb.showerror("Mislukt", "Gebruikersnaam of wachtwoord onjuist.")
