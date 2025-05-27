class SimpleQueue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)  # Add to the end

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)  # Remove from front
        else:
            return None

    def is_empty(self):
        return len(self.items) == 0

    def __len__(self):
        return len(self.items)


def fcfs_scheduling(process_list):
    # Ordenar procesos por Arrival Time (AT)
    process_list.sort(key=lambda p: p.at)
    
    current_time = 0
    for p in process_list:
        # Espera a que el proceso llegue si la CPU está idle
        if current_time < p.at:
            current_time = p.at
        p.start_time = current_time
        p.completed_time = current_time + p.bt
        p.completed = True
        
        current_time += p.bt
        
    return process_list


def sjf_scheduling(process_list):
    n = len(process_list)
    completed = 0
    current_time = 0
    is_completed = [False] * n
    
    # Para ordenar procesos por llegada (Arrival Time)
    process_list.sort(key=lambda p: p.at)
    
    while completed < n:
        # Buscar procesos que han llegado y no están completados
        ready_queue = [p for p in process_list if p.at <= current_time and not p.completed]
        
        if not ready_queue:
            # Si no hay procesos listos, avanzar el tiempo
            current_time += 1
            continue
        
        # Elegir proceso con el burst time más corto
        current_process = min(ready_queue, key=lambda p: p.bt)
        
        # Ejecutar proceso hasta completarlo
        current_process.start_time = current_time
        current_process.completed_time = current_time + current_process.bt
        current_process.completed = True
        
        # Avanzar el tiempo actual
        current_time += current_process.bt
        completed += 1
        
    return process_list


def round_robin_scheduling(process_list, quantum):
    n = len(process_list)
    current_time = 0
    completed = 0
    queue = SimpleQueue()
    process_list.sort(key=lambda p: p.at)
    i = 0

    while i < n and process_list[i].at <= current_time:
        queue.enqueue(process_list[i])
        i += 1

    while completed < n:
        if queue.is_empty():
            current_time = process_list[i].at
            queue.enqueue(process_list[i])
            i += 1

        current_process = queue.dequeue()

        if current_process.start_time is None:
            current_process.start_time = current_time

        exec_time = min(quantum, current_process.remaining_time)
        current_process.remaining_time -= exec_time
        current_time += exec_time

        while i < n and process_list[i].at <= current_time:
            queue.enqueue(process_list[i])
            i += 1

        if current_process.remaining_time == 0:
            current_process.completed = True
            current_process.completed_time = current_time
            completed += 1
        else:
            queue.enqueue(current_process)

    return process_list



def priority_scheduling(process_list):
    n = len(process_list)
    completed = 0
    current_time = 0

    # Ordenar inicialmente por tiempo de llegada
    process_list.sort(key=lambda p: p.at)

    while completed < n:
        # Filtrar procesos listos
        ready_queue = [p for p in process_list if p.at <= current_time and not p.completed]
        
        if not ready_queue:
            current_time += 1
            continue

        # Elegir el de mayor prioridad (número más bajo)
        current_process = min(ready_queue, key=lambda p: p.priority)

        # Ejecutar el proceso
        if current_process.start_time is None:
            current_process.start_time = current_time
        current_process.completed_time = current_time + current_process.bt
        current_process.completed = True
        current_time += current_process.bt
        completed += 1

    return process_list



def srtf(process_list):
    current_time = 0
    completed = 0
    n = len(process_list)
    execution_sequence = []

    process_list.sort(key=lambda p: p.at)

    while completed < n:
        ready_queue = [p for p in process_list if p.at <= current_time and not p.completed]

        if not ready_queue:
            execution_sequence.append(None)  # or some special object to indicate idle
            current_time += 1
            continue

        current_process = min(ready_queue, key=lambda p: p.remaining_time)

        if current_process.start_time is None:
            current_process.start_time = current_time

        # Run process for 1 unit time
        current_process.remaining_time -= 1
        execution_sequence.append(current_process)  # Append the actual Process object
        current_time += 1

        if current_process.remaining_time == 0:
            current_process.completed_time = current_time
            current_process.completed = True
            completed += 1

    return execution_sequence
