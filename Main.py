import customtkinter as ctk
from Dashboard import Dashboard

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1200x800")
app.title("Senior Smart Home")

dashboard = Dashboard(app)
dashboard.pack(fill="both", expand=True)

app.mainloop()
