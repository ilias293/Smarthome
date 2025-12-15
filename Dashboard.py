import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from weather import get_utc_temperature
from data import temperature_data


COLOR_BG = "#0F172A"
COLOR_CARD = "#1E293B"
COLOR_TEXT = "#FFFFFF"
COLOR_ON = "#22C55E"
COLOR_OFF = "#EF4444"

class Dashboard(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_BG)

        # Titel
        ctk.CTkLabel(
            self,
            text="Senior Smart Home Dashboard",
            font=("Arial", 26, "bold"),
            text_color=COLOR_TEXT
        ).pack(pady=20)

        self.create_device_buttons()
        self.create_temperature_card()
        self.create_chart()

    def create_device_buttons(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(pady=10)

        self.light_on = False

        self.light_btn = ctk.CTkButton(
            frame,
            text="Licht uit",
            fg_color=COLOR_OFF,
            command=self.toggle_light
        )
        self.light_btn.pack(pady=5)

    def toggle_light(self):
        self.light_on = not self.light_on
        if self.light_on:
            self.light_btn.configure(text="Licht aan", fg_color=COLOR_ON)
        else:
            self.light_btn.configure(text="Licht uit", fg_color=COLOR_OFF)

    def create_temperature_card(self):
        card = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=10)
        card.pack(pady=20)

        temp = get_utc_temperature()
        text = f"Actuele temperatuur Utrecht: {temp}°C" if temp else "Temperatuur niet beschikbaar"

        self.temp_label = ctk.CTkLabel(
            card,
            text=text,
            font=("Arial", 18),
            text_color=COLOR_TEXT
        )
        self.temp_label.pack(padx=20, pady=20)

    def create_chart(self):
        fig, ax = plt.subplots()
        ax.bar(temperature_data.keys(), temperature_data.values())
        ax.set_title("Temperatuur per kamer")

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)
