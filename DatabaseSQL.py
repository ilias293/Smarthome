import psycopg2

# Verbinding maken met de database
conn = psycopg2.connect(
    host="csc-ilias-smarthome.postgres.database.azure.com",
    port="5432",
    database="postgres",
    user="IliasOuk",
    password="Test1234"
)

cursor = conn.cursor()


cursor.execute("SELECT * FROM devices;")
rows = cursor.fetchall()

cursor.execute("SELECT * FROM energy_usage;")
rows = cursor.fetchall()

cursor.execute("SELECT * FROM total_energy_usage;")
rows = cursor.fetchall()

column_names = [desc[0] for desc in cursor.description]

data = {col: [] for col in column_names}

for row in rows:
    for col_name, value in zip(column_names, row):
        data[col_name].append(value)

cursor.close()
conn.close()

for col, values in data.items():
    print(f"{col}: {values}")

import csv

with open("devices_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow(data.keys())

    rows = zip(*data.values())
    for row in rows:
        writer.writerow(row)


