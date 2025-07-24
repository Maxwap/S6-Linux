import tkinter as tk
from tkinter import ttk, filedialog
import time
import psutil
import json
import csv

def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def get_system_info():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    return f"CPU: {cpu}% | RAM: {ram}% | Réseau: {current_net_speed:.2f} Mo/s"

def update_dashboard():
    time_var.set(get_time())
    system_var.set(get_system_info())
    root.after(1000, update_dashboard)

def read_logs(file_path, filter_text=""):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            if filter_text:
                lines = [line for line in lines if filter_text in line]
            return lines[-50:]
    except:
        return ["Impossible de lire le fichier."]

def refresh_logs():
    pam_logs = read_logs("/var/log/auth.log", pam_filter.get())
    postfix_logs = read_logs("/var/log/mail.log", postfix_filter.get())
    pam_text.delete(1.0, tk.END)
    postfix_text.delete(1.0, tk.END)
    pam_text.insert(tk.END, "".join(pam_logs))
    postfix_text.insert(tk.END, "".join(postfix_logs))

def export_logs(format_):
    logs = {
        "pam": read_logs("/var/log/auth.log", pam_filter.get()),
        "postfix": read_logs("/var/log/mail.log", postfix_filter.get())
    }
    path = filedialog.asksaveasfilename(defaultextension=f".{format_}")
    if not path:
        return
    with open(path, 'w') as f:
        if format_ == "json":
            json.dump(logs, f, indent=4)
        else:
            writer = csv.writer(f)
            for key, lines in logs.items():
                writer.writerow([f"### {key.upper()} ###"])
                for line in lines:
                    writer.writerow([line.strip()])

# Initialisation interface
root = tk.Tk()
root.title("Tableau de bord système")

time_var = tk.StringVar()
system_var = tk.StringVar()
pam_filter = tk.StringVar()
postfix_filter = tk.StringVar()

tk.Label(root, textvariable=time_var, font=("Arial", 14)).pack()
tk.Label(root, textvariable=system_var, font=("Arial", 12)).pack()

frame = tk.Frame(root)
frame.pack(pady=5)

tk.Label(frame, text="Filtre PAM:").grid(row=0, column=0)
tk.Entry(frame, textvariable=pam_filter).grid(row=0, column=1)
tk.Label(frame, text="Filtre Postfix:").grid(row=0, column=2)
tk.Entry(frame, textvariable=postfix_filter).grid(row=0, column=3)

tk.Button(frame, text="Actualiser les logs", command=refresh_logs).grid(row=1, column=0, columnspan=2)
tk.Button(frame, text="Exporter en CSV", command=lambda: export_logs("csv")).grid(row=1, column=2)
tk.Button(frame, text="Exporter en JSON", command=lambda: export_logs("json")).grid(row=1, column=3)

pam_text = tk.Text(root, height=10, width=100)
pam_text.pack(pady=5)
postfix_text = tk.Text(root, height=10, width=100)
postfix_text.pack(pady=5)

graph_canvas = tk.Canvas(root, width=800, height=250, bg="white")
graph_canvas.pack(pady=10)

legend = tk.Label(root, text="CPU (rouge, %), RAM (bleu, %), Réseau (vert, x3 zoom, Mo/s)", font=("Arial", 10))
legend.pack()

# Historique des données système
cpu_history = []
ram_history = []
net_history = []

last_net_bytes = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
current_net_speed = 0.0  # Mo/s

def update_graph():
    global last_net_bytes, current_net_speed

    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    total_now = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
    current_net_speed = (total_now - last_net_bytes) / 1024 / 1024  # en Mo/s
    last_net_bytes = total_now

    cpu_history.append(cpu)
    ram_history.append(ram)
    net_history.append(current_net_speed)
    if len(cpu_history) > 100:
        cpu_history.pop(0)
        ram_history.pop(0)
        net_history.pop(0)

    graph_canvas.delete("all")

    net_max = max(1, max(net_history, default=1))
    net_zoom_factor = 3.0

    width = int(graph_canvas['width'])
    height = int(graph_canvas['height'])
    step = width / 100

    # Axes Y CPU/RAM
    for val in [0, 25, 50, 75, 100]:
        y = height - (val / 100) * height
        graph_canvas.create_line(0, y, width, y, fill="#eee")
        graph_canvas.create_text(10, y, anchor="nw", text=f"{val}%", font=("Arial", 8), fill="gray")

    # Axes Y réseau (échelle après zoom)
    for val in range(1, int(net_max) + 1):
        y = height - ((val * net_zoom_factor) / net_max) * height
        graph_canvas.create_line(0, y, width, y, fill="#f0f0f0")
        graph_canvas.create_text(width - 50, y, anchor="nw", text=f"{val} Mo/s", font=("Arial", 8), fill="gray")

    def draw_line(data, color, max_val, zoom=1.0):
        for i in range(1, len(data)):
            x1 = (i - 1) * step
            x2 = i * step
            y1 = height - ((data[i - 1] * zoom) / max_val) * height
            y2 = height - ((data[i] * zoom) / max_val) * height
            graph_canvas.create_line(x1, y1, x2, y2, fill=color, width=2)

    draw_line(cpu_history, "red", 100)
    draw_line(ram_history, "blue", 100)
    draw_line(net_history, "green", net_max, zoom=net_zoom_factor)

    root.after(1000, update_graph)

# Lancer les mises à jour
update_dashboard()
update_graph()
root.mainloop()
