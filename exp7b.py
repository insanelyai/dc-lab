from collections import defaultdict

print("Hasan Sayyed 232P003 32")


class Process:
   def __init__(self, pid, site):
       self.pid = pid
       self.site = site
       self.waiting_for = []   # processes this process is waiting for
       self.blocked = False
       self.dependent = defaultdict(bool)


class DistributedDeadlockDetector:
   def __init__(self):
       self.processes = {}  # pid -> Process
       self.message_count = 0

   def add_process(self, pid, site):
       self.processes[pid] = Process(pid, site)

   def add_dependency(self, from_pid, to_pid):
       """from_pid is waiting on to_pid"""
       self.processes[from_pid].waiting_for.append(to_pid)
       self.processes[from_pid].blocked = True

   def reset_state(self):
       """Reset dependent flags before new detection"""
       self.message_count = 0
       for process in self.processes.values():
           process.dependent = defaultdict(bool)

   def send_probe(self, i, j, k):
       """Send probe (i, j, k)"""
       self.message_count += 1
       print(f"Probe sent: ({i}, {j}, {k})")

       pk = self.processes[k]

       # On receiving probe at process k
       if pk.blocked and not pk.dependent[i]:
           pk.dependent[i] = True

           # Deadlock condition
           if k == i:
               print(f"\nDeadlock detected involving process {i}")
               return True

           # Forward probe further
           for next_proc in pk.waiting_for:
               if pk.site != self.processes[next_proc].site:
                   if self.send_probe(i, k, next_proc):
                       return True
       return False

   def initiate_detection(self):
       """Initiate deadlock detection"""
       self.reset_state()

       for pid, process in self.processes.items():
           if process.blocked:
               i = pid

               # Self-dependency check
               if pid in process.waiting_for:
                   print(
                       f"\nDeadlock detected: Process {pid} waiting on itself")
                   return

               # Send probes
               for j in process.waiting_for:
                   if process.site != self.processes[j].site:
                       if self.send_probe(i, pid, j):
                           print(
                               f"Total messages exchanged: {self.message_count}")
                           return

       print("\nNo deadlock detected.")
       print(f"Total messages exchanged: {self.message_count}")


# -------------------------
# Example Usage
# -------------------------

detector = DistributedDeadlockDetector()

# Create processes (pid, site)
detector.add_process(1, 1)
detector.add_process(2, 2)
detector.add_process(3, 3)

# Create circular wait (deadlock)
detector.add_dependency(1, 2)
detector.add_dependency(2, 3)
detector.add_dependency(3, 1)

# Start detection
detector.initiate_detection()
