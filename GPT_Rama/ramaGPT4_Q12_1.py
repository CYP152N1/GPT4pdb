import tkinter as tk
from tkinter import ttk
from io import StringIO
import csv

# ここに、以前に提供したfetch_pdb、extract_phi_psi、およびwrite_to_csv関数を含めます。

def run_analysis():
    pdb_id = pdb_id_entry.get()
    chain_id = chain_id_entry.get()

    try:
        filename = fetch_pdb(pdb_id)
        phi_psi_data = extract_phi_psi(pdb_id, chain_id, filename)

        pdb_text.delete('1.0', tk.END)
        with open(filename, "r") as f:
            pdb_text.insert(tk.END, f.read())

        csv_output = StringIO()
        csv_writer = csv.writer(csv_output)
        csv_writer.writerow(["Residue", "Residue_ID", "Phi (degrees)", "Psi (degrees)"])
        for row in phi_psi_data:
            csv_writer.writerow(row)

        csv_text.delete('1.0', tk.END)
        csv_text.insert(tk.END, csv_output.getvalue())

    except Exception as e:
        error_label.config(text=f"Error: {str(e)}")

app = tk.Tk()
app.title("PDB Phi-Psi Analyzer")

frame = ttk.Frame(app, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

pdb_id_label = ttk.Label(frame, text="PDB ID:")
pdb_id_label.grid(row=0, column=0, sticky=tk.W)
pdb_id_entry = ttk.Entry(frame, width=10)
pdb_id_entry.grid(row=0, column=1, sticky=tk.W)

chain_id_label = ttk.Label(frame, text="Chain ID:")
chain_id_label.grid(row=1, column=0, sticky=tk.W)
chain_id_entry = ttk.Entry(frame, width=10)
chain_id_entry.grid(row=1, column=1, sticky=tk.W)

analyze_button = ttk.Button(frame, text="Analyze", command=run_analysis)
analyze_button.grid(row=2, column=0, columnspan=2, pady=10)

pdb_text = tk.Text(app, wrap=tk.NONE, width=80, height=20)
pdb_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

csv_text = tk.Text(app, wrap=tk.NONE, width=80, height=20)
csv_text.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

error_label = ttk.Label(app, text="", foreground="red")
error_label.grid(row=2, column=0, columnspan=2, pady=10)

app.columnconfigure(0, weight=1)
app.columnconfigure(1, weight=1)
app.rowconfigure(1, weight=1)

app.mainloop()
