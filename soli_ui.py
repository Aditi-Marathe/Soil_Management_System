import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import random

# Database Setup
conn = sqlite3.connect("soil_management.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS SoilData (
                    id INTEGER PRIMARY KEY,
                    location TEXT,
                    type TEXT,
                    pH REAL,
                    nitrogen REAL,
                    phosphorus REAL,
                    potassium REAL
                )''')
conn.commit()

# UI Setup
root = tk.Tk()
root.title("🌱 Soil Management System 🌱")
root.geometry("700x600")
root.configure(bg="#e1f5fe")

# Styling
heading_font = ("Arial", 18, "bold")
label_font = ("Arial", 12)
button_font = ("Arial", 12, "bold")

# Heading
heading = tk.Label(root, text="🌾 Soil Management System 🌾", font=heading_font, bg="#e1f5fe", fg="black")
heading.pack(pady=10)

# Input Box
frame = tk.Frame(root, bg="#b3e5fc", bd=5, relief=tk.RIDGE)
frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

# Labels and Dropdowns
labels = ["Farm Location", "Soil Type", "pH Level", "Nitrogen (mg/kg)", "Phosphorus (mg/kg)", "Potassium (mg/kg)"]
options = {
    "Farm Location": ["Farm A", "Farm B", "Farm C", "Farm D"],
    "Soil Type": ["Loamy", "Sandy", "Clayey", "Silty"],
    "pH Level": [str(round(i, 1)) for i in range(4, 9)],
    "Nitrogen (mg/kg)": [str(i) for i in range(1, 6)],
    "Phosphorus (mg/kg)": [str(i) for i in range(1, 6)],
    "Potassium (mg/kg)": [str(i) for i in range(1, 6)]
}

entries = {}

for i, label_text in enumerate(labels):
    lbl = tk.Label(frame, text=f"{label_text} 🌍", font=label_font, bg="#b3e5fc")
    lbl.grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
    
    var = tk.StringVar()
    dropdown = ttk.Combobox(frame, textvariable=var, values=options[label_text], state="readonly", font=label_font)
    dropdown.grid(row=i, column=1, padx=10, pady=5)
    dropdown.current(0)  # Set default selection
    entries[label_text] = var

# Insert Function
def insert_data():
    values = [entries[label].get() for label in labels]
    cursor.execute("INSERT INTO SoilData (location, type, pH, nitrogen, phosphorus, potassium) VALUES (?, ?, ?, ?, ?, ?)", values)
    conn.commit()
    messagebox.showinfo("Success", "Record Inserted Successfully! 🌿")

insert_btn = tk.Button(frame, text="Insert Data ✅", font=button_font, bg="#0288d1", fg="white", command=insert_data)
insert_btn.grid(row=len(labels), columnspan=2, pady=10)

# Bulk Insert Function
bulk_options = [100, 500, 1000, 10000]
bulk_var = tk.IntVar()
bulk_var.set(100)

bulk_label = tk.Label(frame, text="Select Bulk Insert Count:", font=label_font, bg="#b3e5fc")
bulk_label.grid(row=len(labels) + 1, column=0, padx=10, pady=5, sticky=tk.W)

bulk_dropdown = ttk.Combobox(frame, textvariable=bulk_var, values=bulk_options, state="readonly", font=label_font)
bulk_dropdown.grid(row=len(labels) + 1, column=1, padx=10, pady=5)
bulk_dropdown.current(0)

def bulk_insert():
    count = bulk_var.get()
    for _ in range(count):
        cursor.execute("INSERT INTO SoilData (location, type, pH, nitrogen, phosphorus, potassium) VALUES (?, ?, ?, ?, ?, ?)", 
                       (random.choice(options["Farm Location"]),
                        random.choice(options["Soil Type"]),
                        random.choice(options["pH Level"]),
                        random.choice(options["Nitrogen (mg/kg)"]),
                        random.choice(options["Phosphorus (mg/kg)"]),
                        random.choice(options["Potassium (mg/kg)"])))
    conn.commit()
    messagebox.showinfo("Success", f"{count} Records Inserted Automatically! 🚜")

bulk_insert_btn = tk.Button(frame, text="Insert Bulk Data 📦", font=button_font, bg="#0288d1", fg="white", command=bulk_insert)
bulk_insert_btn.grid(row=len(labels) + 2, columnspan=2, pady=10)

# Display Function
def display_data():
    top = tk.Toplevel(root)
    top.title("📊 Soil Data Records 📊")
    top.geometry("700x500")
    top.configure(bg="#e1f5fe")

    cursor.execute("SELECT * FROM SoilData ORDER BY id DESC LIMIT 1000")  # Show last 1000 records
    records = cursor.fetchall()

    text = tk.Text(top, font=("Arial", 12), bg="#ffffff", wrap=tk.WORD)
    text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    if not records:
        text.insert(tk.END, "No records found in the database!")
    else:
        for record in records:
            text.insert(tk.END, f"ID: {record[0]}, Location: {record[1]}, Type: {record[2]}, pH: {record[3]}, "
                                f"N: {record[4]}, P: {record[5]}, K: {record[6]}\n")

    text.config(state=tk.DISABLED)

display_btn = tk.Button(root, text="Display Data 📋", font=button_font, bg="#0288d1", fg="white", command=display_data)
display_btn.pack(pady=10)

# Run Application
root.mainloop()
