import random
import csv

# aantal dagen data
dagen = 60

# lijsten voor alle variabelen
douche_minuten = []
oven_minuten = []
lamp_minuten = []
verwarming_minuten = []
kraan_minuten = []
magnetron_minuten = []
tv_minuten = []
energie_totaal = []

for _ in range(dagen):

    # Realistische ranges
    douche = random.randint(0, 30)               # douche: 0–30 min
    oven = random.randint(0, 90)                 # oven: 0–90 min
    lampen = random.randint(200, 800)            # lampen: 200–800 min
    verwarming = random.randint(0, 600)          # verwarming: 0–600 min
    kraan = random.randint(0, 20)                # kraan: 0–20 min warm water
    magnetron = random.randint(0, 20)            # magnetron: 0–20 min
    tv = random.randint(0, 240)                  # tv: 0–240 min

    # Energieverbruik (kWh) – realistisch model
    energie = (
        3.0 +                        # basisverbruik
        douche * 0.15 +              # douche kost veel energie
        oven * 0.10 +                # oven kost veel energie
        lampen * 0.003 +             # lampen kosten weinig
        verwarming * 0.02 +          # verwarming kost veel
        kraan * 0.05 +               # warm water
        magnetron * 0.08 +           # magnetron
        tv * 0.005 +                 # tv kost weinig
        random.uniform(-1, 1)        # ruis
    )

    # opslaan
    douche_minuten.append(douche)
    oven_minuten.append(oven)
    lamp_minuten.append(lampen)
    verwarming_minuten.append(verwarming)
    kraan_minuten.append(kraan)
    magnetron_minuten.append(magnetron)
    tv_minuten.append(tv)
    energie_totaal.append(energie)

# dataset opslaan als CSV
with open("smarthome_dataset.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "douche_minuten",
        "oven_minuten",
        "lamp_minuten",
        "verwarming_minuten",
        "kraan_minuten",
        "magnetron_minuten",
        "tv_minuten",
        "energie_totaal"
    ])

    for i in range(dagen):
        writer.writerow([
            douche_minuten[i],
            oven_minuten[i],
            lamp_minuten[i],
            verwarming_minuten[i],
            kraan_minuten[i],
            magnetron_minuten[i],
            tv_minuten[i],
            energie_totaal[i]
        ])

print("Dataset succesvol gegenereerd!")
