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
    timeline = []

    for p in process_list:
        # CPU idle time if process hasn't arrived yet
        while current_time < p.at:
            timeline.append(None)
            current_time += 1

        p.start_time = current_time

        # Ejecutar el proceso (uno por uno)
        for _ in range(p.bt):
            timeline.append(p)
            current_time += 1

        p.completed_time = current_time
        p.completed = True

    return process_list, timeline



def sjf_scheduling(process_list):
    n = len(process_list)
    completed = 0
    current_time = 0
    timeline = []

    process_list.sort(key=lambda p: p.at)

    while completed < n:
        # Get ready processes that have arrived
        ready_queue = [p for p in process_list if p.at <= current_time and not p.completed]

        if not ready_queue:
            timeline.append(None)  # CPU is idle
            current_time += 1
            continue

        # Select process with the shortest burst time
        current_process = min(ready_queue, key=lambda p: p.bt)

        if current_process.start_time is None:
            current_process.start_time = current_time

        # Execute the process to completion
        for _ in range(current_process.bt):
            timeline.append(current_process)
            current_time += 1

        current_process.completed_time = current_time
        current_process.completed = True
        completed += 1

    return process_list, timeline


def round_robin_scheduling(process_list, quantum):
    n = len(process_list)
    current_time = 0
    completed = 0
    timeline = []

    queue = SimpleQueue()
    process_list.sort(key=lambda p: p.at)
    i = 0

    # Enqueue initially available processes
    while i < n and process_list[i].at <= current_time:
        queue.enqueue(process_list[i])
        i += 1

    while completed < n:
        if queue.is_empty():
            timeline.append(None)  # Idle
            current_time += 1

            # Check for newly arrived processes
            while i < n and process_list[i].at <= current_time:
                queue.enqueue(process_list[i])
                i += 1
            continue

        current_process = queue.dequeue()

        if current_process.start_time is None:
            current_process.start_time = current_time

        # Execute process in quantum-sized chunks
        exec_time = min(quantum, current_process.remaining_time)

        for _ in range(exec_time):
            timeline.append(current_process)
            current_process.remaining_time -= 1
            current_time += 1

            # Enqueue newly arrived processes while current process is executing
            while i < n and process_list[i].at <= current_time:
                queue.enqueue(process_list[i])
                i += 1

            # If the current process finishes during this slice
            if current_process.remaining_time == 0:
                break

        if current_process.remaining_time == 0:
            current_process.completed = True
            current_process.completed_time = current_time
            completed += 1
        else:
            queue.enqueue(current_process)

    return process_list, timeline


def priority_scheduling(process_list):
    n = len(process_list)
    completed = 0
    current_time = 0
    execution_sequence = []  # Per time unit

    # Sort processes by arrival time initially
    process_list.sort(key=lambda p: p.at)

    while completed < n:
        # Get processes that have arrived and are not yet completed
        ready_queue = [p for p in process_list if p.at <= current_time and not p.completed]

        if not ready_queue:
            execution_sequence.append(None)  # None represents "Idle"
            current_time += 1
            continue

        # Select process with highest priority (lowest priority number)
        current_process = min(ready_queue, key=lambda p: p.priority)

        # If this is the first time the process is running, record the start time
        if current_process.start_time is None:
            current_process.start_time = current_time

        # Run for full burst time (non-preemptive), record each time unit
        for _ in range(current_process.bt):
            execution_sequence.append(current_process)
            current_time += 1

        current_process.completed_time = current_time
        current_process.completed = True
        completed += 1

    return process_list, execution_sequence




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
