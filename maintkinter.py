import tkinter as tk
from tkinter import filedialog, ttk, Canvas, Scrollbar
from tkinter import messagebox
import os
import random
import time
import threading
import algcalendar
import sincro

class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.at = arrival_time        # Arrival Time
        self.bt = burst_time          # Burst Time (total CPU time needed)
        self.priority = priority      # Priority (default 0 if unused)
        
        self.start_time = None        # When process first starts running
        self.completed_time = None    
        self.remaining_time = burst_time  # Algoritmos para (preemptive)
        self.completed = False        

list_process = []


def readfilelines(filepath):
    global list_process
    list_process = []  # Asegúrate de inicializar la lista aquí
    try:
        with open(filepath, "r") as file:
            for line in file:
                dummy_arr = line.strip().split(",")
                if len(dummy_arr) < 4:
                    print("ERROR: EL PROCESO NO TIENE ALGUNOS ATRIBUTOS")
                    continue
                try:
                    # Aquí invertimos el orden BT y AT para que coincida con la clase Process
                    pid = dummy_arr[0].strip()
                    bt = int(dummy_arr[1])
                    at = int(dummy_arr[2])
                    priority = int(dummy_arr[3])
                    p = Process(pid, at, bt, priority)
                    list_process.append(p)
                except ValueError:
                    print(f"ERROR: Datos inválidos en la línea: {line.strip()}")
    except FileNotFoundError:
        print("ERROR: Archivo no encontrado.")
    return list_process



def upload_file():
    global list_process
    file_path = filedialog.askopenfilename(
        title="Selecciona un archivo de texto",
        filetypes=[("Text files", "*.txt")]
    )
    if file_path:
        uploaded_file_label.config(text=f"Archivo cargado: {os.path.basename(file_path)}")

        # Clear previous process labels
        for label in process_labels:
            label.config(text="")
            

        # Read and display processes
        processes = readfilelines(file_path)
        for i in range(min(3, len(processes))):
            p = processes[i]
            process_labels[i].config(
                text=f"PID: {p.pid}, BT: {p.bt}, AT: {p.at}, Priority: {p.priority}",
                fg="black"
            )



def upload_file2():
    global list_process
    file_path = filedialog.askopenfilename(
        title="Selecciona un archivo de texto",
        filetypes=[("Text files", "*.txt")]
    )
    if file_path:
        uploaded_file_label.config(text=f"Archivo cargado: {os.path.basename(file_path)}")

        # Clear previous process labels
        for label in process_labels2:
            label.config(text="")
            

        # Read and display processes
        processes = readfilelines(file_path)
        for i in range(min(3, len(processes))):
            p = processes[i]
            process_labels2[i].config(
                text=f"PID: {p.pid}, BT: {p.bt}, AT: {p.at}, Priority: {p.priority}",
                fg="black"
            )
    



# Create the main window
root = tk.Tk()
root.title("Simulador de algoritmos. final")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set desired margins (e.g., 50 pixels on each edge)
margin = 70
window_width = int(screen_width/2) - 2 * margin
window_height = int(screen_height) - int(1.2* margin)

# Position the window centered with margin
x_pos = 0
y_pos = 0

root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")
#GEOMETRY ONLY DIMENSIONS NOW LETS WORK TO IT


notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Create individual tabs (frames)
tab1 = tk.Frame(notebook, bg="white")
tab2 = tk.Frame(notebook, bg="white")


# Add tabs to the notebook
notebook.add(tab1, text="Simulador de Algoritmos de Calendarización")
notebook.add(tab2, text="Simulador de Mecanismos de Sincronización")



# Add content to tabs
tk.Label(tab1, text="Algoritmos de Calendarización",background="white", font=("Arial", 16)).pack(pady=20)
upload_btn = tk.Button(tab1, text="Cargar Archivo de procesos .txt", command=upload_file)
upload_btn.pack(pady=10)

process_labels = []
for _ in range(3):
    lb2 = tk.Label(tab1, text="", bg="white", font=("Courier", 12))
    lb2.pack(pady=2)
    process_labels.append(lb2)

uploaded_file_label = tk.Label(tab1, text="", bg="white", fg="blue", wraplength=500)
uploaded_file_label.pack(pady=5)




selected_algorithms = {}
quantum_value = tk.StringVar(value="1")  # default quantum

# Function to enable/disable quantum entry
def on_algorithm_change():
    if selected_algorithms["Round Robin"].get():
        quantum_entry.config(state="normal")
    else:
        quantum_entry.config(state="disabled")

    if not start_button.winfo_ismapped():
        start_button.pack(pady=40)



# Frame to group radio buttons
algos_frame = tk.Frame(tab1, bg="white")
algos_frame.pack()

algorithms = [
    ("First In First Out", "FIFO"),
    ("Shortest Job First", "SJF"),
    ("Shortest Remaining Time", "SRT"),
    ("Priority", "Priority"),
    ("Round Robin", "Round Robin")
    
]

for text, value in algorithms:
    var = tk.BooleanVar()
    selected_algorithms[value] = var

    chk = tk.Checkbutton(
        algos_frame,
        text=text,
        variable=var,
        bg="white",
        font=("Arial", 11),
        command=on_algorithm_change
    )
    chk.pack(anchor='w', padx=5)

# Quantum input (only visible if Round Robin is selected)
quantum_frame = tk.Frame(tab1, bg="white")
quantum_frame.pack(pady=(5, 10))

tk.Label(quantum_frame, text="Quantum:", bg="white").pack(side="left", padx=5)

quantum_entry = tk.Entry(quantum_frame, textvariable=quantum_value, width=5, state="disabled")
quantum_entry.pack(side="left")

def start_simulation():
    global list_process
    if not list_process:
        error_label.config(text="Error: No hay datos cargados. Por favor, cargue un archivo primero.")
        return

    error_label.config(text="")

    for algo, var in selected_algorithms.items():
        if var.get():
            q = quantum_value.get() if algo == "Round Robin" else None
            open_simulation_window(algo, q)  

start_button = tk.Button(
    tab1,
    text="Iniciar Simulación",
    font=("Arial", 12, "bold"),
    bg="#4CAF50", fg="white",
    command=start_simulation
)

def generate_color():
    """Returns a random color in hex format."""
    return f'#{random.randint(50, 200):02x}{random.randint(50, 200):02x}{random.randint(50, 200):02x}'

def draw_gantt_chart_dynamic(canvas, execution_sequence, time_unit=60):
    # Clear previous drawings
    canvas.delete("all")

    # Map each PID to a y-coordinate
    pid_list = list({p.pid if p else "Idle" for p in execution_sequence})
    pid_list.sort()
    pid_y = {pid: 80 + i * 60 for i, pid in enumerate(pid_list)}  # vertical space for each row

    colors = {}

    # Draw timeline header
    start_x = 100
    canvas.create_text(10, 40, text="Tiempo (Ciclo)", anchor='w', font=('Arial', 10, 'bold'))

    for t in range(len(execution_sequence)):
        x = start_x + t * time_unit
        y = 40
        text_str = str(t)
        font = ('Arial', 15)
        
        # Create the text temporarily to get its bounding box
        temp_text_id = canvas.create_text(x + time_unit // 2, y, text=text_str, font=font)
        bbox = canvas.bbox(temp_text_id)  # returns (x1, y1, x2, y2)
        canvas.delete(temp_text_id)
        
        padding_x = 5
        padding_y = 3
        
        # Draw rectangle behind text as border
        canvas.create_rectangle(
            bbox[0] - padding_x,
            bbox[1] - padding_y,
            bbox[2] + padding_x,
            bbox[3] + padding_y,
            outline='black', fill='white'
        )
        
        # Draw the actual text on top of rectangle
        canvas.create_text(x + time_unit // 2, y, text=text_str, font=font)


    # Draw process labels
    for pid, y in pid_y.items():
        canvas.create_text(10, y + 20, text=f"{pid} :", anchor='w', font=('Arial', 12, 'bold'))

    # Animate execution
    canvas.xview_moveto(0)  # start from beginning horizontally
    for t, process in enumerate(execution_sequence):
        pid = process.pid if process else "Idle"

        if pid not in colors:
            colors[pid] = generate_color()

        x = start_x + t * time_unit
        y = pid_y[pid]

        canvas.create_rectangle(x, y, x + time_unit, y + 40, fill=colors[pid], outline='black')
        canvas.create_text(x + time_unit // 2, y + 20, text=pid, fill='white')

        canvas.update()
        time.sleep(0.3)
        canvas.configure(scrollregion=canvas.bbox("all"))



def open_simulation_window(algorithm, quantum):
    win = tk.Toplevel(root)
    win.title("Simulación")

    window_width = 900
    window_height = int(screen_height) -  int(1.2*margin)
    sep = int(screen_width/2) - 2 * margin
    win.geometry(f"{window_width}x{window_height}+{sep}+0")

    tk.Label(win, text=f"Algoritmo seleccionado: {algorithm}", font=("Arial", 14)).pack(pady=10)

    if algorithm == "Round Robin":
        tk.Label(win, text=f"Quantum: {quantum}", font=("Arial", 12)).pack()

    frame = tk.Frame(win)
    frame.pack(fill='both', expand=True)

    canvas = Canvas(frame, bg="white", height=200)
    canvas.pack(side='left', fill='both', expand=True)

    x_scrollbar = Scrollbar(canvas, orient='horizontal', command=canvas.xview)
    y_scrollbar = Scrollbar(canvas, orient='vertical', command=canvas.yview)

    canvas.configure(xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)

    # Empaquetar canvas y scrollbars
    canvas.pack(side='left', fill='both', expand=True)
    x_scrollbar.pack(side='bottom', fill='x')
    y_scrollbar.pack(side='right', fill='y')

    # Región de scroll: define el tamaño máximo del contenido (ajusta si necesitas más espacio)
    canvas.configure(scrollregion=(0, 0, 5000, 2000))  # ancho x alto del contenido del canvas

    def run_simulation():
        canvas.delete("all")  # Clear previous drawing
        canvas.xview_moveto(0)  # Reset scroll to start
        canvas.configure(scrollregion=(0, 0, 0, 0))  # Reset scrollregion

        local_processes = readfilelines("process.txt")  # Reload fresh data
        if algorithm == "FIFO":
            scheduled, timeline = algcalendar.fcfs_scheduling(local_processes)
            avg_wt = calculate_avg_waiting_time(scheduled)
            scheduled = timeline
        elif algorithm == "SJF":
            scheduled, timeline = algcalendar.sjf_scheduling(local_processes)
            avg_wt = calculate_avg_waiting_time(scheduled)
            scheduled = timeline
        elif algorithm == "Priority":
            scheduled, timeline = algcalendar.priority_scheduling(local_processes)
            avg_wt = calculate_avg_waiting_time(scheduled)
            scheduled = timeline
        elif algorithm == "Round Robin":
            scheduled, timeline = algcalendar.round_robin_scheduling(local_processes, int(quantum))
            avg_wt = calculate_avg_waiting_time(scheduled)
            scheduled = timeline
        elif algorithm == "SRT":
            scheduled = algcalendar.srtf(local_processes)
            avg_wt = calculate_avg_waiting_time(scheduled)
        else:
            avg_wt = 0
            scheduled = []

        draw_gantt_chart_dynamic(canvas, scheduled)
        tk.Label(win, text=f"Tiempo promedio de espera: {avg_wt:.2f} ciclos", font=("Arial", 12, "bold"), fg="blue").pack(pady=5)

    # First run
    run_simulation()

    # Restart button
    restart_btn = tk.Button(win, text="Reiniciar Simulación", command=run_simulation)
    restart_btn.pack(pady=10)


def calculate_avg_waiting_time(processes):
    total_waiting_time = 0
    for p in processes:
        turnaround_time = p.completed_time - p.at
        waiting_time = turnaround_time - p.bt
        total_waiting_time += waiting_time
    return total_waiting_time / len(processes)

error_label = tk.Label(tab1, text="", fg="red", font=("Arial", 11), bg="white")
error_label.pack(pady=5)






#tab 2 que se encuentra los mecanismos de sincronización
tk.Label(tab2, text="Mecanismos de Sincronización.", background="white" ,font=("Arial", 16)).pack(pady=20)



loaded_resources = {}
def upload_resources_file():
    global resources_file_path, loaded_resources
    file_path = filedialog.askopenfilename(
        title="Selecciona archivo de Recursos",
        filetypes=[("Archivos de texto", "*.txt")]
    )
    if file_path:
        resources_file_path = file_path

        # Determine synchronization type from radio buttons
        use_semaphore = sync_mode.get() == "semaphore"

        loaded_resources = sincro.load_resources_resource(file_path, use_semaphore)
        label_resources.config(text=f"Archivo recursos: {file_path.split('/')[-1]}")

        resource_display.delete("1.0", tk.END)
        if loaded_resources:
            for i, (name, resource) in enumerate(loaded_resources.items()):
                if i >= 3:
                    break
                resource_display.insert(tk.END, f"Recurso: {name}, Cantidad: {resource.count}\n")
        else:
            resource_display.insert(tk.END, "No se cargaron recursos válidos.")


actions_list = []

def upload_actions_file():
    global actions_file_path, actions_list
    file_path = filedialog.askopenfilename(
        title="Selecciona archivo de Acciones",
        filetypes=[("Archivos de texto", "*.txt")]
    )
    if file_path:
        actions_file_path = file_path

        # Cargar acciones
        actions_list = sincro.load_actions(file_path, list_process, list(loaded_resources.values()))

        # Mostrar primeras 3 acciones (si existen)
        if actions_list:
            for i in range(min(3, len(actions_list))):
                action = actions_list[i]
                action_labels[i].config(
                    text=f"{action.pid} {action.operation} {action.resource_name} ciclo {action.cycle}",
                    fg="black"
                )



sync_mode = tk.StringVar(value="semaphore")  

sync_frame = tk.Frame(tab2)
sync_frame.pack(pady=5)

sync_label = tk.Label(sync_frame, text="Modo de sincronización:" )
sync_label.pack(side=tk.LEFT)

radio_semaphore = tk.Radiobutton(sync_frame, text="Semaphore", variable=sync_mode, background="white" ,value="semaphore")
radio_semaphore.pack(side=tk.LEFT)

radio_mutex = tk.Radiobutton(sync_frame, text="Mutex", variable=sync_mode, value="mutex")
radio_mutex.pack(side=tk.LEFT)


     
# Dentro de tu ventana o tab actual
upload_btn_process = tk.Button(tab2, text="Cargar Archivo Procesos .txt", command=upload_file2)
upload_btn_process.pack(pady=5)

uploaded_file_label = tk.Label(tab2, text="", bg="white", fg="blue", wraplength=500)
uploaded_file_label.pack(pady=5)

process_labels2 = []
for _ in range(3):
    lb2 = tk.Label(tab2, text="", bg="white", font=("Courier", 12))
    lb2.pack(pady=2)
    process_labels2.append(lb2)



class GanttEntry:
    def __init__(self, pid, resource, operation, status, cycle):
        self.pid = pid
        self.resource = resource
        self.operation = operation
        self.status = status  # "waiting" or "accessed"
        self.cycle = cycle    # simulated cycle at which this happened

    def __repr__(self):
        return f"<{self.pid} {self.operation} {self.resource} {self.status} @ cycle {self.cycle}>"

def simulate_action(process, actions, resources, gantt_log):
    for action in actions:
        if action.pid != process.pid:
            continue

        resource = resources.get(action.resource_name)
        if not resource:
            print(f"{process.pid}: Recurso {action.resource_name} no encontrado")
            continue

        print(f"{process.pid} esperando para {action.operation} en {resource.name} en ciclo {action.cycle}")
        
        # Agrega estado "WAITING"
        gantt_log.append(GanttEntry(process.pid, resource.name, action.operation , "WAITING", action.cycle))

        time.sleep(action.cycle * 0.1)

        # Intenta acceder al recurso
        print(f"{process.pid} intenta {action.operation} en {resource.name}")
        resource.control.acquire()
        print(f"{process.pid} ACCEDIÓ a {resource.name} ({action.operation})")

        # Agrega estado "ACCESED" justo después del ciclo
        gantt_log.append(GanttEntry(process.pid, resource.name, action.operation , "ACCESED", action.cycle))

        time.sleep(0.5)

        print(f"{process.pid} LIBERA {resource.name}")
        resource.control.release()




def open_simulation_window_for_mutex():
    win = tk.Toplevel(root)
    win.title("Simulación Mutex/Semáforo")

    window_width = 1000
    window_height = int(screen_height) - int(1.2* margin)
    sep = int(screen_width/2) - 2 * margin
    win.geometry(f"{window_width}x{window_height}+{sep}+0")

    tk.Label(win, text=f"Simulación de Acciones sobre Recursos", font=("Arial", 14)).pack(pady=10)

    frame = tk.Frame(win)
    frame.pack(fill='both', expand=True)

    canvas = Canvas(frame, bg="white", height=200)
    canvas.pack(side='left', fill='both', expand=True)

    x_scrollbar = Scrollbar(canvas, orient='horizontal', command=canvas.xview)
    y_scrollbar = Scrollbar(canvas, orient='vertical', command=canvas.yview)

    canvas.configure(xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)
    canvas.pack(side='left', fill='both', expand=True)
    x_scrollbar.pack(side='bottom', fill='x')
    y_scrollbar.pack(side='right', fill='y')

    canvas.configure(scrollregion=(0, 0, 5000, 2000))

    def run_mutex_simulation():
        canvas.delete("all")
        canvas.xview_moveto(0)
        canvas.configure(scrollregion=(0, 0, 0, 0))

        gantt_log = start_simulation_mut_sem()
        if gantt_log:
            draw_gantt_from_log_animated(canvas, gantt_log, time_unit=60, delay=500)
        else:
            messagebox.showerror("Error", "Something went wrong!")        

    run_mutex_simulation()

    restart_btn = tk.Button(win, text="Reiniciar Simulación", command=run_mutex_simulation)
    restart_btn.pack(pady=10)


def draw_gantt_from_log_animated(canvas, gantt_log, time_unit=60, delay=500):
    """
    Animate drawing the Gantt chart one block at a time.

    :param canvas: Tkinter Canvas to draw on.
    :param gantt_log: List of log entries with pid, cycle, status, resource.
    :param time_unit: Width of each time block in pixels.
    :param delay: Delay in milliseconds between drawing each block.
    """
    canvas.delete("all")

    pids = sorted(set(entry.pid for entry in gantt_log))
    pid_y = {pid: 80 + i * 60 for i, pid in enumerate(pids)}

    status_colors = {"WAITING": "orange", "ACCESED": "green"}
    start_x = 100

    # Draw timeline header once
    max_cycle = max(entry.cycle for entry in gantt_log) + 1
    for t in range(max_cycle):
        x = start_x + t * time_unit
        canvas.create_text(x + time_unit // 2, 40, text=str(t), font=('Arial', 12, 'bold'))
        canvas.create_line(x, 60, x, 60 + len(pids) * 60, fill="#ccc")

    # Draw process labels once
    for pid, y in pid_y.items():
        canvas.create_text(10, y + 20, text=f"{pid}:", anchor='w', font=('Arial', 12, 'bold'))

    # Animation variables
    index = 0

    def draw_next_block():
        nonlocal index
        if index >= len(gantt_log):
            return  # Done drawing all blocks

        entry = gantt_log[index]
        x = start_x + entry.cycle * time_unit
        y = pid_y[entry.pid]
        fill = status_colors.get(entry.status.upper(), "gray")

        canvas.create_rectangle(x, y, x + time_unit, y + 40, fill=fill, outline='black')
        canvas.create_text(x + time_unit // 2, y + 20, text=f"{entry.resource}, {entry.operation}\n{entry.status}", font=('Arial', 8), fill='white')

        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.xview_moveto(max(0, (x - 300) / (max_cycle * time_unit)))  # Scroll so current block is visible

        index += 1
        canvas.after(delay, draw_next_block)

    # Start animation
    draw_next_block()



def start_simulation_mut_sem():
    global list_process, actions_list, loaded_resources

    text = ""

    # Verificaciones de archivos cargados
    if not list_process:
        text += "Error: No hay procesos cargados. Por favor, cargue un archivo primero.\n"
    if not actions_list:
        text += "Error: No hay acciones cargadas. Por favor, cargue el archivo de acciones.\n"
    if not loaded_resources:
        text += "Error: No hay recursos cargados. Por favor, cargue el archivo de recursos.\n"

    error_labelsem.config(text=text)

    if text != "":
        return None  # Stop simulation on error

    # Convert list of resources to dictionary for easy access

    resources_dict = loaded_resources
    
    # List to store all Gantt chart entries
    gantt_log = []

    threads = []

    for process in list_process:
        t = threading.Thread(target=simulate_action, args=(process, actions_list, resources_dict, gantt_log))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("Simulación completada.")

    # Return the Gantt log to use it for plotting
    return gantt_log


def open_simulation_window_for_mutex():
    win = tk.Toplevel(root)
    win.title("Simulación Mutex/Semáforo")

    window_width = 1000
    window_height = window_height = int(screen_height) - margin
    sep = int(screen_width/2) - 2 * margin
    win.geometry(f"{window_width}x{window_height}+{sep}+0")

    tk.Label(win, text=f"Simulación de Acciones sobre Recursos", font=("Arial", 14)).pack(pady=10)

    frame = tk.Frame(win)
    frame.pack(fill='both', expand=True)

    canvas = Canvas(frame, bg="white", height=200)
    canvas.pack(side='left', fill='both', expand=True)

    x_scrollbar = Scrollbar(canvas, orient='horizontal', command=canvas.xview)
    y_scrollbar = Scrollbar(canvas, orient='vertical', command=canvas.yview)

    canvas.configure(xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)
    canvas.pack(side='left', fill='both', expand=True)
    x_scrollbar.pack(side='bottom', fill='x')
    y_scrollbar.pack(side='right', fill='y')

    canvas.configure(scrollregion=(0, 0, 5000, 2000))

    def run_mutex_simulation():
        canvas.delete("all")
        canvas.xview_moveto(0)
        canvas.configure(scrollregion=(0, 0, 0, 0))

        gantt_log = start_simulation_mut_sem()
        if gantt_log:
            draw_gantt_from_log_animated(canvas, gantt_log, time_unit=60, delay=500)
        else:
            tk.Label(win, text="Error en la simulación", fg="red").pack(pady=5)

    run_mutex_simulation()

    restart_btn = tk.Button(win, text="Reiniciar Simulación", command=run_mutex_simulation)
    restart_btn.pack(pady=10)



upload_resources_btn = tk.Button(tab2, text="Cargar Archivo de Recursos", command=upload_resources_file)
upload_resources_btn.pack(pady=5)
label_resources = tk.Label(tab2, text="Archivo recursos: Ninguno", bg="white")
label_resources.pack(pady=5)
resource_display = tk.Text(tab2, height=4, bg="white",width=50)
resource_display.pack(pady=5)


upload_btn_actions = tk.Button(tab2, text="Cargar Archivo Acciones .txt", command=upload_actions_file)
upload_btn_actions.pack(pady=5)

action_labels = [
    tk.Label(tab2, text="", bg="white"),
    tk.Label(tab2, text="", bg="white"),
    tk.Label(tab2, text="", bg="white")
]
for lbl in action_labels:
    lbl.pack()

start_buttonsem = tk.Button(
    tab2,
    text="Iniciar Simulación",
    font=("Arial", 12, "bold"),
    bg="#4CAF50", fg="white",
    command=open_simulation_window_for_mutex  
)
start_buttonsem.pack(pady=5)


error_labelsem = tk.Label(tab2, text="", fg="red", font=("Arial", 11), bg="white")
error_labelsem.pack(pady=5)


# Start the GUI event loop
root.mainloop()



