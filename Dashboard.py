import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv

# ======================
# STYLING
# ======================
COLOR_BG = "#0F172A"
COLOR_CARD = "#1E293B"
COLOR_TEXT = "#FFFFFF"
COLOR_ON = "#22C55E"
COLOR_OFF = "#EF4444"

DEVICE_COLORS = {
    "Lampen": "#FFD700",
    "Oven": "#FF8C00",
    "Verwarming": "#FF4500",
    "Magnetron": "#1E90FF",
    "TV": "#800080",
    "Douchen": "#00CED1"
}

ENERGIE_DREMPEL_APPARATEN = 5  # pop-up als 5 of meer apparaten aan staan

# ======================
# DATA INLEZEN (HISTORIE)
# ======================
history = {
    "Lampen": [],
    "Oven": [],
    "Verwarming": [],
    "Magnetron": [],
    "TV": [],
    "Douchen": [],
    "Energie": []
}

with open("smarthome_dataset.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        history["Lampen"].append(float(row["lamp_minuten"]) * 0.003)  # minuten -> kWh
        history["Oven"].append(float(row["oven_minuten"]) * 0.10)
        history["Verwarming"].append(float(row["verwarming_minuten"]) * 0.02)
        history["Magnetron"].append(float(row["magnetron_minuten"]) * 0.08)
        history["TV"].append(float(row["tv_minuten"]) * 0.005)
        history["Douchen"].append(float(row["douche_minuten"]) * 0.15)
        history["Energie"].append(float(row["energie_totaal"]))  # totale energie in dataset

# ======================
# DASHBOARD
# ======================
class Dashboard(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_BG)
        self.pack(fill="both", expand=True)

        # status apparaten
        self.device_states = {}
        self.device_buttons = {}

        # huidige verbruik apparaten (aan/uit)
        self.current_usage = {device: 0 for device in DEVICE_COLORS.keys()}

        self.usage_canvas = None
        self.chart_canvas = None

        self.create_title()
        self.create_layout()
        self.create_usage_chart()

    # ------------------
    # TITEL
    # ------------------
    def create_title(self):
        ctk.CTkLabel(
            self,
            text="Senior Smart Home Dashboard",
            font=("Arial", 26, "bold"),
            text_color=COLOR_TEXT
        ).pack(pady=10)

    # ------------------
    # LAYOUT
    # ------------------
    def create_layout(self):
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=20)

        # LINKS: knoppen + huidig verbruik
        self.left = ctk.CTkFrame(main, fg_color=COLOR_CARD, corner_radius=10)
        self.left.pack(side="left", fill="y", padx=10)

        # RECHTS: historische grafieken
        self.right = ctk.CTkFrame(main, fg_color=COLOR_CARD, corner_radius=10)
        self.right.pack(side="right", fill="both", expand=True, padx=10)

        self.create_device_buttons()
        self.create_exit_button()
        self.create_graph_buttons()

    # ------------------
    # APPARAAT KNOPPEN
    # ------------------
    def create_device_buttons(self):
        ctk.CTkLabel(
            self.left,
            text="Apparaten",
            font=("Arial", 18, "bold"),
            text_color=COLOR_TEXT
        ).pack(pady=10)

        grid = ctk.CTkFrame(self.left, fg_color="transparent")
        grid.pack()

        devices = list(DEVICE_COLORS.keys())
        for i, device in enumerate(devices):
            self.device_states[device] = False

            btn = ctk.CTkButton(
                grid,
                text=f"{device} uit",
                fg_color=COLOR_OFF,
                width=140,
                command=lambda d=device: self.toggle_device(d)
            )
            btn.grid(row=i // 2, column=i % 2, padx=8, pady=8)
            self.device_buttons[device] = btn

    def toggle_device(self, device):
        self.device_states[device] = not self.device_states[device]
        btn = self.device_buttons[device]

        if self.device_states[device]:
            btn.configure(text=f"{device} aan", fg_color=COLOR_ON)
            # gebruik = laatste waarde van dataset in kWh
            self.current_usage[device] = history[device][-1]
        else:
            btn.configure(text=f"{device} uit", fg_color=COLOR_OFF)
            self.current_usage[device] = 0

        # pop-up alleen als 5 of meer apparaten aan
        if sum(self.device_states.values()) >= ENERGIE_DREMPEL_APPARATEN:
            self.show_energy_popup()

        self.create_usage_chart()

    # ------------------
    # HUIDIG VERBRUIK (lijn, totale energie afgelopen 7 dagen)
    # ------------------
    def create_usage_chart(self):
        if self.usage_canvas:
            self.usage_canvas.get_tk_widget().destroy()

        fig, ax = plt.subplots(figsize=(5, 3))
        # totaal energie per dag van de afgelopen 7 dagen
        last_7_days = list(zip(*[history[dev][-7:] for dev in DEVICE_COLORS.keys()]))
        total_per_day = [sum(day) for day in last_7_days]

        ax.plot(range(1, len(total_per_day)+1), total_per_day, marker='o', color="#22C55E")
        ax.set_title("Totale energie afgelopen 7 dagen (kWh)")
        ax.set_xlabel("Dag")
        ax.set_ylabel("kWh")
        ax.set_xticks(range(1, len(total_per_day)+1))

        self.usage_canvas = FigureCanvasTkAgg(fig, self.left)
        self.usage_canvas.draw()
        self.usage_canvas.get_tk_widget().pack(pady=10)

    # ------------------
    # HISTORISCHE GRAFIEKEN (30 dagen)
    # ------------------
    def create_graph_buttons(self):
        ctk.CTkLabel(
            self.right,
            text="Historische data (laatste 30 dagen)",
            font=("Arial", 18, "bold"),
            text_color=COLOR_TEXT
        ).pack(pady=10)

        btn_frame = ctk.CTkFrame(self.right, fg_color="transparent")
        btn_frame.pack()

        for name, values in history.items():
            ctk.CTkButton(
                btn_frame,
                text=name,
                command=lambda n=name, v=values[-30:]: self.show_chart(n, v)
            ).pack(side="left", padx=5)

    def show_chart(self, title, values):
        if self.chart_canvas:
            self.chart_canvas.get_tk_widget().destroy()

        fig, ax = plt.subplots(figsize=(6, 4))
        values = values[-30:]  # laatste 30 dagen
        ax.bar(range(1, len(values)+1), values, color="#22C55E")
        ax.set_title(f"{title} per dag")
        ax.set_xlabel("Dag")
        ax.set_ylabel("kWh")
        ax.set_xticks(range(1, len(values)+1))

        self.chart_canvas = FigureCanvasTkAgg(fig, self.right)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)

    # ------------------
    # POP-UP WAARSCHUWING
    # ------------------
    def show_energy_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Energie waarschuwing")
        popup.geometry("320x180")

        ctk.CTkLabel(
            popup,
            text="⚠ Hoog energieverbruik",
            font=("Arial", 18, "bold"),
            text_color=COLOR_OFF
        ).pack(pady=10)

        ctk.CTkLabel(
            popup,
            text="5 of meer apparaten zijn aan.\nLet op energieverbruik!",
            justify="center"
        ).pack(pady=10)

        ctk.CTkButton(
            popup,
            text="OK",
            command=popup.destroy
        ).pack()

    # ------------------
    # AFSLUITKNOP
    # ------------------
    def create_exit_button(self):
        ctk.CTkButton(
            self.left,
            text="Afsluiten",
            fg_color=COLOR_OFF,
            command=self.master.destroy
        ).pack(side="bottom", pady=15)


# ======================
# APP START
# ======================
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")

    app = ctk.CTk()
    app.title("Smart Home Dashboard")
    app.geometry("1200x800")

    Dashboard(app)

    app.mainloop()
