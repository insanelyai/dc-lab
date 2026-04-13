from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import threading
import time

# ---------- Remote Methods ----------


def add(a, b):
   return a + b


def subtract(a, b):
   return a - b

# ---------- Server Code ----------


def start_server():
   server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
   server.register_function(add, "add")
   server.register_function(subtract, "subtract")
   print("RMI Server started on port 8000...")
   print("Hasan Sayyed 232P003 32")
   server.serve_forever()

# ---------- Client Code ----------


def start_client():
   time.sleep(1)  # wait for server
   proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

   a = int(input("Enter the value of a: "))
   b = int(input("Enter the value of b: "))

   print("Remote Addition:", proxy.add(a, b))
   print("Remote Subtraction:", proxy.subtract(a, b))


# ---------- Main ----------
if __name__ == "__main__":
   server_thread = threading.Thread(target=start_server)
   server_thread.daemon = True
   server_thread.start()

   start_client()
