import threading


class Resource:
    def __init__(self, name, count, use_semaphore=True):
        self.name = name
        self.count = count
        self.use_semaphore = use_semaphore

        if use_semaphore:
            self.control = threading.Semaphore(count)
        else:
            self.control = threading.Lock()

    def acquire(self):
        self.control.acquire()

    def release(self):
        self.control.release()


#Reads the resources like name and how much 
def load_resources_resource(filepath, use_semaphore):
    resources = {}
    try:
        with open(filepath, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) != 2:
                    print(f"Skipping invalid line: {line.strip()}")
                    continue
                name = parts[0].strip()
                try:
                    count = int(parts[1].strip())
                    resources[name] = Resource(name, count,use_semaphore)
                except ValueError:
                    print(f"Invalid count for resource '{name}': {parts[1]}")
    except FileNotFoundError:
        print("ERROR: Archivo de recursos no encontrado.")
    return resources





class Action:
    def __init__(self, pid, operation, resource_name, cycle):
        self.pid = pid.strip()                   # e.g., "P1"
        self.operation = operation.strip()       # e.g., "READ", "WRITE", "RELEASE"
        self.resource_name = resource_name.strip()  # e.g., "R1"
        self.cycle = int(cycle)                  # e.g., 0


def load_actions(filename, process_list, resource_list):
    actions = []
    try:
        with open(filename, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) != 4:
                    print(f"ERROR: Línea inválida: {line.strip()}")
                    continue

                pid, action_type, resource_name, cycle = [p.strip() for p in parts]

                if not pid_exists(process_list, pid):
                    print(f"ERROR: PID '{pid}' no existe en la lista de procesos.")
                    continue

                if not resource_exist(resource_list, resource_name):
                    print(f"ERROR: Recurso '{resource_name}' no existe.")
                    continue

                try:
                    actions.append(Action(pid, action_type, resource_name, int(cycle)))
                except ValueError:
                    print(f"ERROR: Ciclo inválido en línea: {line.strip()}")
    except FileNotFoundError:
        print("ERROR: Archivo no encontrado:", filename)

    return actions



def pid_exists(obj_list, pid):
    return any(obj.pid == pid for obj in obj_list)

def resource_exist(resourcelist, name):
    return any(obj.name == name for obj in resourcelist)



