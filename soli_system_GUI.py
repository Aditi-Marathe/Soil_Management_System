import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import random
from faker import Faker

# Database setup
def setup_database():
    conn = sqlite3.connect("soil_management.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS soil_data (
                      id INTEGER PRIMARY KEY,
                      location TEXT,
                      soil_type TEXT,
                      ph_level REAL,
                      moisture REAL,
                      nitrogen REAL,
                      phosphorus REAL,
                      potassium REAL
                      )''')
    conn.commit()
    conn.close()

# Insert single record
def insert_record():
    location = entry_location.get()
    soil_type = combo_type.get()
    ph = entry_ph.get()
    moisture = entry_moisture.get()
    nitrogen = entry_nitrogen.get()
    phosphorus = entry_phosphorus.get()
    potassium = entry_potassium.get()

    if not location or not soil_type:
        messagebox.showwarning("Input Error", "Please fill all fields!")
        return

    conn = sqlite3.connect("soil_management.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO soil_data (location, soil_type, ph_level, moisture, nitrogen, phosphorus, potassium) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (location, soil_type, ph, moisture, nitrogen, phosphorus, potassium))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Record inserted successfully! 🌱")

# Bulk Insert
def bulk_insert():
    num_records = int(combo_bulk.get())
    fake = Faker()
    conn = sqlite3.connect("soil_management.db")
    cursor = conn.cursor()
    
    for _ in range(num_records):
        location = fake.city()
        soil_type = random.choice(["Clay", "Sandy", "Loamy", "Peaty", "Chalky", "Silty"])
        ph = round(random.uniform(4.5, 8.5), 2)
        moisture = round(random.uniform(5, 50), 2)
        nitrogen = round(random.uniform(0.1, 5.0), 2)
        phosphorus = round(random.uniform(0.1, 5.0), 2)
        potassium = round(random.uniform(0.1, 5.0), 2)
        cursor.execute("INSERT INTO soil_data (location, soil_type, ph_level, moisture, nitrogen, phosphorus, potassium) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (location, soil_type, ph, moisture, nitrogen, phosphorus, potassium))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", f"{num_records} records inserted! 🌍")

# Display Records
def display_records():
    conn = sqlite3.connect("soil_management.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM soil_data")
    rows = cursor.fetchall()
    conn.close()

    for row in tree.get_children():
        tree.delete(row)

    for row in rows:
        tree.insert("", "end", values=row)

# GUI Setup
setup_database()
root = tk.Tk()
root.title("🌾 Soil Management System 🌍")
root.geometry("800x600")
root.configure(bg="#f5f5dc")

# Labels & Inputs
tk.Label(root, text="Soil Location", bg="#f5f5dc").grid(row=0, column=0)
entry_location = tk.Entry(root)
entry_location.grid(row=0, column=1)

tk.Label(root, text="Soil Type", bg="#f5f5dc").grid(row=1, column=0)
combo_type = ttk.Combobox(root, values=["Clay", "Sandy", "Loamy", "Peaty", "Chalky", "Silty"])
combo_type.grid(row=1, column=1)

tk.Label(root, text="pH Level", bg="#f5f5dc").grid(row=2, column=0)
entry_ph = tk.Entry(root)
entry_ph.grid(row=2, column=1)

tk.Label(root, text="Moisture %", bg="#f5f5dc").grid(row=3, column=0)
entry_moisture = tk.Entry(root)
entry_moisture.grid(row=3, column=1)

tk.Label(root, text="Nitrogen (mg/kg)", bg="#f5f5dc").grid(row=4, column=0)
entry_nitrogen = tk.Entry(root)
entry_nitrogen.grid(row=4, column=1)

tk.Label(root, text="Phosphorus (mg/kg)", bg="#f5f5dc").grid(row=5, column=0)
entry_phosphorus = tk.Entry(root)
entry_phosphorus.grid(row=5, column=1)

tk.Label(root, text="Potassium (mg/kg)", bg="#f5f5dc").grid(row=6, column=0)
entry_potassium = tk.Entry(root)
entry_potassium.grid(row=6, column=1)

# Buttons
tk.Button(root, text="Insert Record 🌿", command=insert_record, bg="#4CAF50", fg="white").grid(row=7, column=0, pady=10)

tk.Label(root, text="Insert Bulk Records", bg="#f5f5dc").grid(row=8, column=0)
combo_bulk = ttk.Combobox(root, values=["10", "100", "500", "1000", "10000", "100000", "1000000"])
combo_bulk.grid(row=8, column=1)
tk.Button(root, text="Insert Bulk 🌾", command=bulk_insert, bg="#FFA500", fg="white").grid(row=9, column=0, pady=10)

tk.Button(root, text="Display Records 📊", command=display_records, bg="#1E90FF", fg="white").grid(row=10, column=0, pady=10)

# Table to Display Data
tree = ttk.Treeview(root, columns=("ID", "Location", "Type", "pH", "Moisture", "N", "P", "K"), show='headings')
for col in ("ID", "Location", "Type", "pH", "Moisture", "N", "P", "K"):
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.grid(row=11, column=0, columnspan=3)

root.mainloop()
