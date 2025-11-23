import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from weather import get_utc_temperature
from data import electricity_data, water_data, activity_data, temperature_data
from PIL import Image

# Kleurenpalet
COLOR_BG = "#1A1F3B"        # Hele dashboard achtergrond
COLOR_CARD = "#2C3666"      # Grafiek / statuscard achtergrond
COLOR_HEADER = "#4C6EB1"    # Header / highlights
COLOR_TEXT = "#FFFFFF"       # Witte tekst
COLOR_ON = "#3CB371"         # Knop aan
COLOR_OFF = "#D9534F"        # Knop uit
COLOR_HOVER_ON = "#5FD686"   # Hover aan
COLOR_HOVER_OFF = "#E57370"  # Hover uit
COLOR_HOVER_CARD = "#3A4170" # Hover card lichtblauw

class DataPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_BG)

        # Header
        ctk.CTkLabel(self, text="Senior Smart Home Dashboard",
                     font=("Arial", 26, "bold"), text_color=COLOR_HEADER).pack(pady=10)

        # Container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # Sidebar
        self.sidebar = ctk.CTkFrame(container, width=220, fg_color=COLOR_BG)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        # Main frame
        self.main_frame = ctk.CTkFrame(container, fg_color="transparent")
        self.main_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Live temperatuur kaart
        self.temp_card = ctk.CTkFrame(self.main_frame, fg_color=COLOR_CARD, corner_radius=15)
        self.temp_card.pack(pady=10, padx=10, fill="x")
        self.temp_label = ctk.CTkLabel(self.temp_card, text="Actuele temperatuur: --°C", font=("Arial", 20), text_color=COLOR_TEXT)
        self.temp_label.pack(pady=20)
        self.update_temperature()

        # FC Utrecht logo
        logo_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        logo_frame.place(relx=0.95, rely=0.0, anchor="ne")
        try:
            logo_image = ctk.CTkImage(Image.open("fcutrechtfoto.png"), size=(35, 35))
            ctk.CTkLabel(logo_frame, image=logo_image, text="").pack()
        except:
            ctk.CTkLabel(logo_frame, text="Maddox stinkt", font=("Arial", 30), text_color=COLOR_TEXT).pack()

        # Statuscards apparaten
        self.devices = {
            "Licht": {"status": False, "btn": None, "label": None, "icon": "💡"},
            "Gordijnen": {"status": False, "btn": None, "label": None, "icon": "🪟"},
            "Verwarming": {"status": False, "btn": None, "label": None, "icon": "🔥"},
            "Alarm": {"status": False, "btn": None, "label": None, "icon": "🚨"},
        }

        for name, info in self.devices.items():
            card = ctk.CTkFrame(self.sidebar, fg_color=COLOR_CARD, corner_radius=10)
            card.pack(pady=5, padx=5, fill="x")

            # Hover effect card
            card.bind("<Enter>", lambda e, c=card: c.configure(fg_color=COLOR_HOVER_CARD))
            card.bind("<Leave>", lambda e, c=card: c.configure(fg_color=COLOR_CARD))

            lbl = ctk.CTkLabel(card, text=f"{info['icon']} {name}: Uit", text_color=COLOR_TEXT, font=("Arial", 14))
            lbl.pack(padx=5, pady=5)
            info["label"] = lbl

            btn = ctk.CTkButton(card, text="Toggle", fg_color=COLOR_OFF, text_color=COLOR_TEXT,
                                command=lambda n=name: self.toggle_device(n))
            btn.pack(padx=5, pady=5, fill="x")
            info["btn"] = btn

            btn.bind("<Enter>", lambda e, n=name: self.on_hover(n, True))
            btn.bind("<Leave>", lambda e, n=name: self.on_hover(n, False))

        # Grafieken
        self.create_charts()
        self.update_electricity_chart()  # start realtime update

    # ---------------- Grafieken ----------------
    def create_charts(self):
        plt.rcParams["axes.facecolor"] = COLOR_CARD
        plt.rcParams["figure.facecolor"] = COLOR_CARD
        plt.rcParams["axes.edgecolor"] = COLOR_TEXT
        plt.rcParams["axes.labelcolor"] = COLOR_TEXT
        plt.rcParams["xtick.color"] = COLOR_TEXT
        plt.rcParams["ytick.color"] = COLOR_TEXT
        plt.rcParams["text.color"] = COLOR_TEXT

        charts_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        charts_frame.pack(fill="both", expand=True, padx=10, pady=10)

        upper = ctk.CTkFrame(charts_frame, fg_color="transparent")
        upper.pack(fill="both", expand=True, padx=5, pady=5)

        lower = ctk.CTkFrame(charts_frame, fg_color="transparent")
        lower.pack(fill="both", expand=True, padx=5, pady=5)

        # Temperatuur per kamer
        self.fig1, self.ax1 = plt.subplots()
        self.ax1.bar(temperature_data.keys(), temperature_data.values(), color=COLOR_HEADER)
        self.ax1.set_title("Temperatuur per kamer (°C)")
        self.canvas1 = FigureCanvasTkAgg(self.fig1, upper)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Elektriciteitsverbruik
        self.fig2, self.ax2 = plt.subplots()
        self.ax2.plot(list(electricity_data.keys()), list(electricity_data.values()), marker='o', color="#5C7FBF")
        self.ax2.set_title("Elektriciteitsverbruik per dag (kWh)")
        self.canvas2 = FigureCanvasTkAgg(self.fig2, upper)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Waterverbruik
        fig3, ax3 = plt.subplots()
        ax3.plot(list(water_data.keys()), list(water_data.values()), marker='o', color="#7FA8D9")
        ax3.set_title("Waterverbruik per dag (liter)")
        canvas3 = FigureCanvasTkAgg(fig3, lower)
        canvas3.draw()
        canvas3.get_tk_widget().pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Activiteit
        fig4, ax4 = plt.subplots()
        ax4.bar(activity_data.keys(), activity_data.values(), color="#4C6EB1")
        ax4.set_title("Activiteit per periode")
        canvas4 = FigureCanvasTkAgg(fig4, lower)
        canvas4.draw()
        canvas4.get_tk_widget().pack(side="left", fill="both", expand=True, padx=5, pady=5)

    # ---------------- Apparaten functies ----------------
    def toggle_device(self, name):
        info = self.devices[name]
        info["status"] = not info["status"]
        self.animate_toggle(name)

    def animate_toggle(self, name):
        info = self.devices[name]
        target_color = COLOR_ON if info["status"] else COLOR_OFF
        info["label"].configure(text=f"{info['icon']} {name}: {'Aan' if info['status'] else 'Uit'}")
        # Eenvoudige directe update, kan uitgebreid met echte fade
        info["btn"].configure(fg_color=target_color)

    def on_hover(self, name, enter):
        info = self.devices[name]
        if info["status"]:
            info["btn"].configure(fg_color=COLOR_HOVER_ON if enter else COLOR_ON)
        else:
            info["btn"].configure(fg_color=COLOR_HOVER_OFF if enter else COLOR_OFF)

    # ---------------- Live temperatuur ----------------
    def update_temperature(self):
        temp = get_utc_temperature()
        if temp is not None:
            self.temp_label.configure(text=f"Actuele temperatuur Utrecht: {temp}°C")
        else:
            self.temp_label.configure(text="Actuele temperatuur: Niet beschikbaar")
        self.after(300000, self.update_temperature)  # update elke 5 minuten

    # ---------------- Realtime grafiek update ----------------
    def update_electricity_chart(self):
        # voorbeeld: hier kun je echte data updaten
        self.ax2.clear()
        self.ax2.plot(list(electricity_data.keys()), list(electricity_data.values()), marker='o', color="#5C7FBF")
        self.ax2.set_title("Elektriciteitsverbruik per dag (kWh)", color=COLOR_TEXT)
        self.canvas2.draw()
        self.after(60000, self.update_electricity_chart)  # update elke minuut
