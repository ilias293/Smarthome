import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import psycopg2
from weather import get_utc_temperature

DEVICE_NAMES = {1: "Lampen", 2: "Oven", 3: "Verwarming", 4: "Magnetron", 5: "TV"}
DEVICE_COLORS = {"Lampen":"#FFD700","Oven":"#FF8C00","Verwarming":"#FF4500","Magnetron":"#1E90FF","TV":"#800080"}
COLOR_BG="#0F172A"
COLOR_CARD="#1E293B"
COLOR_TEXT="#FFFFFF"
COLOR_ON="#22C55E"
COLOR_OFF="#EF4444"
POPUP_APPARATEN=3

conn = psycopg2.connect(
    host="csc-ilias-smarthome.postgres.database.azure.com",
    port="5432",
    database="postgres",
    user="IliasOuk",
    password="Test1234"
)
cursor = conn.cursor()
cursor.execute("SELECT device_id, usage_kwh FROM energy_usage ORDER BY measured_at ASC;")
rows = cursor.fetchall()
cursor.close()
conn.close()

history = {name: [] for name in DEVICE_NAMES.values()}
for device_id, usage_kwh in rows:
    if device_id in DEVICE_NAMES:
        device_name = DEVICE_NAMES[device_id]
        history[device_name].append(float(usage_kwh))
for key in history:
    history[key] = history[key][-30:]

class Dashboard(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_BG)
        self.pack(fill="both", expand=True)
        self.device_states = {device: False for device in DEVICE_NAMES.values()}
        self.device_buttons = {}
        self.chart_canvas = None
        self.create_title()
        self.create_weather()
        self.create_layout()
        self.create_graph_buttons()

    def create_title(self):
        ctk.CTkLabel(self, text="Senior Smart Home Dashboard", font=("Arial",26,"bold"), text_color=COLOR_TEXT).pack(pady=10)

    def create_weather(self):
        temp = get_utc_temperature()
        temp_text = f"Actuele temperatuur Utrecht: {temp}°C" if temp else "Temperatuur niet beschikbaar"
        ctk.CTkLabel(self, text=temp_text, font=("Arial",16,"bold"), text_color=COLOR_TEXT).pack(pady=5)

    def create_layout(self):
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=20)
        self.left = ctk.CTkFrame(main, fg_color=COLOR_CARD, corner_radius=10)
        self.left.pack(side="left", fill="y", padx=10)
        self.right = ctk.CTkFrame(main, fg_color=COLOR_CARD, corner_radius=10)
        self.right.pack(side="right", fill="both", expand=True, padx=10)
        self.create_device_buttons()
        self.create_exit_button()

    def create_device_buttons(self):
        ctk.CTkLabel(self.left, text="Apparaten", font=("Arial",18,"bold"), text_color=COLOR_TEXT).pack(pady=10)
        grid = ctk.CTkFrame(self.left, fg_color="transparent")
        grid.pack()
        devices = list(DEVICE_NAMES.values())
        for i, device in enumerate(devices):
            btn = ctk.CTkButton(grid, text=f"{device} uit", fg_color=COLOR_OFF, width=140,
                                command=lambda d=device: self.toggle_device(d))
            btn.grid(row=i//2, column=i%2, padx=8, pady=8)
            self.device_buttons[device] = btn

    def toggle_device(self, device):
        self.device_states[device] = not self.device_states[device]
        btn = self.device_buttons[device]
        if self.device_states[device]:
            btn.configure(text=f"{device} aan", fg_color=COLOR_ON)
        else:
            btn.configure(text=f"{device} uit", fg_color=COLOR_OFF)
        if sum(self.device_states.values()) >= POPUP_APPARATEN:
            self.show_energy_popup()

    def create_graph_buttons(self):
        ctk.CTkLabel(self.right, text="Data van de laatste 30 dagen", font=("Arial",18,"bold"), text_color=COLOR_TEXT).pack(pady=10)
        btn_frame = ctk.CTkFrame(self.right, fg_color="transparent")
        btn_frame.pack(pady=5)
        for i, (name, values) in enumerate(history.items()):
            btn = ctk.CTkButton(btn_frame, text=name, command=lambda n=name, v=values[-30:]: self.show_chart(n,v))
            btn.grid(row=0, column=i, padx=5)

    def show_chart(self, title, values):
        if self.chart_canvas:
            self.chart_canvas.get_tk_widget().destroy()
        fig, ax = plt.subplots(figsize=(6,4))
        ax.plot(range(1,len(values)+1), values, marker='o', color="#22C55E")
        ax.set_title(f"kWh verbruik van de/het {title} ")
        ax.set_xlabel("Meting")
        ax.set_ylabel("kWh")
        ax.set_xticks(range(1,len(values)+1))
        self.chart_canvas = FigureCanvasTkAgg(fig, self.right)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)

    def show_energy_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Energie waarschuwing")
        popup.geometry("320x180")
        ctk.CTkLabel(popup, text="⚠ Hoog energieverbruik", font=("Arial",18,"bold"), text_color=COLOR_OFF).pack(pady=10)
        ctk.CTkLabel(popup, text="3 of meer apparaten zijn aan.\nLet op energieverbruik!", justify="center").pack(pady=10)
        ctk.CTkButton(popup, text="OK", command=popup.destroy).pack()

    def create_exit_button(self):
        ctk.CTkButton(self.left, text="Afsluiten", fg_color=COLOR_OFF, command=self.master.destroy).pack(side="bottom", pady=15)

if __name__=="__main__":
    ctk.set_appearance_mode("dark")
    app = ctk.CTk()
    app.title("Smart Home Dashboard")
    app.geometry("1200x800")
    Dashboard(app)
    app.mainloop()
