import algcalendar
import sincro
import threading

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

def readfilelines(filepath):

    list_process = []

    with open(filepath, "r") as file:
        for line in file:
            dummy_arr = line.split(",")
            if len(dummy_arr) < 4:
                print("ERROR EL PROCESO NO TIENE ALGUNOS ATRIBUTOS")
                continue  # skip invalid lines
            else:
                list_process.append(  Process( dummy_arr[0].strip(), int(dummy_arr[1]), int(dummy_arr[2]), int(dummy_arr[3]) )  )
    

    return list_process




resources = sincro.load_resources_resource("resources.txt",False)
processes = readfilelines("process.txt")
actions = sincro.load_actions("accion.txt", processes, list(resources.values()))


import time

def simulate_action(process, actions, resources):
    for action in actions:
        if action.pid != process.pid:
            continue

        resource = resources.get(action.resource_name)
        if not resource:
            print(f"{process.pid}: Recurso {action.resource_name} no encontrado")
            continue

        print(f"{process.pid} esperando para {action.operation} en {resource.name} en ciclo {action.cycle}")
        
        # Simula que estamos esperando al ciclo correcto (en la vida real esto sería parte de un sistema más complejo)
        time.sleep(action.cycle * 0.1)

        # Accede al recurso
        print(f"{process.pid} intenta {action.operation} en {resource.name}")
        resource.control.acquire()
        print(f"{process.pid} ACCEDIÓ a {resource.name} ({action.operation})")

        # Simula tiempo de uso
        time.sleep(0.5)

        # Libera el recurso
        print(f"{process.pid} LIBERA {resource.name}")
        resource.control.release()


threads = []

for process in processes:
    t = threading.Thread(target=simulate_action, args=(process, actions, resources))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Simulación terminada.")
# So

# 1st window is the choose options and in there you can tune it 

# once tune lets create a new window which has three tabs, first tab is simulation and button to restart and then other tab is check data again  


# how to make in tkinter 

# Línea de tiempo con bloques representando cada proceso ejecutado en el
# orden correspondiente según el algoritmo de calendarización seleccionado.
# (Diagrama de Gantt)