import time
import random
print("Hasan Sayyed 232P003 32")


class Process:
   def __init__(self, pid):
       self.pid = pid
       self.request_cs = False

   def request_critical_section(self):
       # Randomly decide if process wants CS
       self.request_cs = random.choice([True, False])

   def enter_critical_section(self):
       print(f"--> Process {self.pid} ENTERING Critical Section")
       time.sleep(1)
       print(f"<-- Process {self.pid} EXITING Critical Section")


def token_ring_simulation(num_processes, max_cycles):
   processes = [Process(i) for i in range(num_processes)]
   token_holder = 0  # Process 0 starts with token
   for cycle in range(max_cycles):
       print(f"\n--- Token Cycle {cycle + 1} ---")
       current_process = processes[token_holder]
       print(f"Process {current_process.pid} has the token")
       current_process.request_critical_section()
       if current_process.request_cs:
           current_process.enter_critical_section()
       else:
           print(
               f"Process {current_process.pid} does not need Critical Section")

       # Pass token to next process
       token_holder = (token_holder + 1) % num_processes
       time.sleep(1)

   print("\nSimulation Completed Successfully!")


if __name__ == "__main__":
   token_ring_simulation(num_processes=5, max_cycles=10)
