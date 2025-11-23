from login_page import LoginPage
from register_page import RegisterPage
from Dashboard import DataPage
import customtkinter as ctk
from database import create_db

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x800")
        self.title("Senior Smart Home")

        create_db()  # database aanmaken of verbinden

        # Pagina's initialiseren
        self.login_page = LoginPage(self, self.show_dashboard, self.show_register)
        self.register_page = RegisterPage(self, self.show_login)
        self.dashboard = DataPage(self)

        # Start met loginpagina
        self.login_page.pack(fill="both", expand=True)

    def show_dashboard(self):
        self.login_page.pack_forget()
        self.dashboard.pack(fill="both", expand=True)

    def show_register(self):
        self.login_page.pack_forget()
        self.register_page.pack(fill="both", expand=True)

    def show_login(self):
        self.register_page.pack_forget()
        self.login_page.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
