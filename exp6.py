print("Hasan Sayyed 232P003 32")


class BullyElection:
    def __init__(self, processes):
        self.processes = processes                   # List of process IDs
        # Highest ID is coordinator
        self.coordinator = max(processes)
        self.alive = {p: True for p in processes}

    def crash(self, process):
        self.alive[process] = False
        print(f"\nProcess {process} has crashed!")

    def election(self, initiator):
        print(f"\nProcess {initiator} starts an election")
        higher_processes = [
            p for p in self.processes
            if p > initiator and self.alive[p]
        ]

        if not higher_processes:
            self.coordinator = initiator
            print(f"Process {initiator} becomes the new Coordinator")
        else:
            print(
                f"Process {initiator} sends ELECTION message to {higher_processes}")
            for p in higher_processes:
                print(f"Process {p} responds OK")
            self.election(max(higher_processes))

    def show_status(self):
        print("\nProcess Status:")
        for p in self.processes:
            state = "Alive" if self.alive[p] else "Crashed"
            print(f"Process {p}: {state}")
        print(f"Current Coordinator: {self.coordinator}")


processes = [1, 2, 3, 4, 5, 6, 7]
bully = BullyElection(processes)

bully.show_status()

bully.crash(5)

bully.election(2)

bully.show_status()
