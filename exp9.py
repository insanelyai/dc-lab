import time
print("Hasan Sayyed 232P003 32")
# ----------------------------------------
# Shared Object (Represents Shared Memory Block)
# ----------------------------------------


class SharedObject:
    def __init__(self, address, data, owner):
        self.address = address
        self.data = data
        self.owner = owner


# ----------------------------------------
# Memory Mapping Manager
# ----------------------------------------

class MappingManager:
    def __init__(self):
        # Shared virtual address -> Owner Node
        self.shared_map = {}

    def register(self, obj):
        self.shared_map[obj.address] = obj.owner

    def get_owner(self, address):
        return self.shared_map.get(address)

    def update_owner(self, address, new_owner):
        self.shared_map[address] = new_owner


# ----------------------------------------
# Node in Distributed System
# ----------------------------------------

class Node:

    def __init__(self, node_id, manager):
        self.node_id = node_id
        self.local_memory = {}   # Local cache
        self.manager = manager

    # Create shared object
    def create_object(self, address, data):
        obj = SharedObject(address, data, self)
        self.local_memory[address] = obj
        self.manager.register(obj)
        print(f"Node {self.node_id} created object at {address}")

    # Read operation
    def read(self, address):

        owner = self.manager.get_owner(address)

        if owner == self:
            print(f"Node {self.node_id} reading local object {address}")
            return self.local_memory[address].data

        else:
            print(f"Node {self.node_id} requesting remote read of {address}")
            return self.fetch_from_remote(owner, address)

    # Write operation
    def write(self, address, new_data):

        owner = self.manager.get_owner(address)

        if owner != self:
            print(f"Node {self.node_id} requesting ownership of {address}")
            self.fetch_from_remote(owner, address)

        print(f"Node {self.node_id} writing to {address}")
        self.local_memory[address].data = new_data

    # Simulate data migration
    def fetch_from_remote(self, owner, address):

        print(f"Transferring {address} from Node {owner.node_id}...")
        time.sleep(1)   # simulate network delay

        obj = owner.local_memory.pop(address)

        # Transfer ownership
        obj.owner = self
        self.local_memory[address] = obj
        self.manager.update_owner(address, self)

        print(f"Ownership of {address} moved to Node {self.node_id}")

        return obj.data


# ----------------------------------------
# DSM Simulation
# ----------------------------------------

if __name__ == "__main__":

    manager = MappingManager()

    # Create 5 nodes
    node1 = Node(1, manager)
    node2 = Node(2, manager)
    node3 = Node(3, manager)
    node4 = Node(4, manager)
    node5 = Node(5, manager)

    print("\n--- Creating Shared Resources ---\n")

    # Two shared memory blocks
    node1.create_object("0x100", "Resource A - Original")
    node2.create_object("0x200", "Resource B - Original")

    print("\n--- Operations on Resource 0x100 ---\n")

    print("Read Result:", node3.read("0x100"))
    node4.write("0x100", "Resource A - Modified by Node4")
    print("Read Result:", node5.read("0x100"))

    print("\n--- Operations on Resource 0x200 ---\n")

    print("Read Result:", node1.read("0x200"))
    node3.write("0x200", "Resource B - Modified by Node3")
    print("Read Result:", node5.read("0x200"))

    print("\nDSM Simulation Completed Successfully")
