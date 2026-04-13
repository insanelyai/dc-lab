import time
import random

print("Hasan Sayyed 232P003 32")


class Process:
   def __init__(self, pid, offset):
       self.pid = pid
       self.offset = offset  # clock offset in seconds

   def get_time(self):
       return time.time() + self.offset

   def adjust_clock(self, adjustment):
       self.offset += adjustment


class BerkeleyMaster:
   def __init__(self, master, slaves):
       self.master = master
       self.slaves = slaves

   def poll_slaves(self):
       times = []
       print("\nPolling slaves...\n")
       master_time = self.master.get_time()
       times.append(master_time)
       print(f"Master time: {master_time:.4f}")

       for slave in self.slaves:
           start = time.time()
           delay = random.uniform(0.01, 0.1)
           time.sleep(delay)
           slave_time = slave.get_time()
           end = time.time()

           rtt = end - start
           estimated_slave_time = slave_time + rtt / 2
           times.append(estimated_slave_time)

           print(f"Slave {slave.pid}:")
           print(f"  RTT = {rtt:.4f} sec")
           print(f"  Estimated time = {estimated_slave_time:.4f}")
       return times

   def synchronize(self):
       times = self.poll_slaves()
       avg_time = sum(times) / len(times)
       print(f"\nAverage synchronized time: {avg_time:.4f}\n")

       master_adjustment = avg_time - self.master.get_time()
       self.master.adjust_clock(master_adjustment)

       for slave in self.slaves:
           adjustment = avg_time - slave.get_time()
           slave.adjust_clock(adjustment)

       print("Clocks synchronized successfully!\n")
       print("Final clock values:")
       print(f"Master: {self.master.get_time():.4f}")
       for slave in self.slaves:
           print(f"Slave {slave.pid}: {slave.get_time():.4f}")


if __name__ == "__main__":
   master = Process(pid=0, offset=0)
   slaves = [
       Process(pid=1, offset=random.uniform(-5, 5)),
       Process(pid=2, offset=random.uniform(-5, 5)),
       Process(pid=3, offset=random.uniform(-5, 5)),
       Process(pid=4, offset=random.uniform(-5, 5))
   ]

   print("Initial clock values:")
   print(f"Master: {master.get_time():.4f}")
   for slave in slaves:
       print(f"Slave {slave.pid}: {slave.get_time():.4f}")

   berkeley = BerkeleyMaster(master, slaves)
   berkeley.synchronize()
