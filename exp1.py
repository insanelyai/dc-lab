import socket

BUFFER_SIZE = 1024
SERVER_PORT = 9000
CLIENT_PORT = 9001
LOCALHOST = "127.0.0.1"


def run_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((LOCALHOST, SERVER_PORT))

    print("Server is running...")

    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        message = data.decode()

        if message == "STOP":
            print("Terminated...")
            break

        print("Client:", message)

        reply = input("Server: ")
        sock.sendto(reply.encode(), (LOCALHOST, CLIENT_PORT))

    sock.close()


def run_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((LOCALHOST, CLIENT_PORT))

    print("Client is running... Type STOP to quit")

    while True:
        message = input("Client: ")
        sock.sendto(message.encode(), (LOCALHOST, SERVER_PORT))

        if message == "STOP":
            print("Terminated...")
            break

        data, addr = sock.recvfrom(BUFFER_SIZE)
        print("Server:", data.decode())

    sock.close()


choice = input("Enter mode [server/client]: ").lower()

if choice == "server":
    run_server()
elif choice == "client":
    run_client()
else:
    print("Invalid choice!")
